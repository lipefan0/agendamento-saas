from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.user import User, BusinessConfig
from app.schemas.user import UserCreate, UserResponse, BusinessConfig as BusinessConfigSchema, BusinessConfigResponse
from app.core.security import get_password_hash, verify_password, create_access_token, get_current_user
import json

router = APIRouter()

@router.post("/register", response_model=UserResponse)
async def register(user: UserCreate, db: Session = Depends(get_db)):
    # Verificar se o email já existe
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )
    
    # Criar novo usuário
    db_user = User(
        email=user.email,
        company_name=user.company_name,
        business_type=user.business_type,
        country=user.country,
        phone=user.phone,
        hashed_password=get_password_hash(user.password)
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user

@router.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(data={"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/business-config", response_model=BusinessConfigResponse)
async def create_business_config(
    config: BusinessConfigSchema,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Verificar se já existe configuração para este usuário
    existing_config = db.query(BusinessConfig).filter(
        BusinessConfig.user_id == current_user.id
    ).first()
    
    if existing_config:
        raise HTTPException(
            status_code=400,
            detail="Business configuration already exists for this user"
        )
    
    # Criar nova configuração
    db_config = BusinessConfig(
        user_id=current_user.id,
        description=config.description,
        working_days=json.dumps(config.working_days),  # Convertendo lista para JSON string
        opening_time=config.opening_time,
        closing_time=config.closing_time,
        profile_image=config.profile_image
    )
    
    db.add(db_config)
    db.commit()
    db.refresh(db_config)
    
    # Atualizar o status do usuário
    current_user.is_configured = True
    db.commit()
    
    # Converter working_days de volta para lista para a resposta
    response_data = BusinessConfigResponse(
        id=db_config.id,
        user_id=db_config.user_id,
        description=db_config.description,
        working_days=json.loads(db_config.working_days),
        opening_time=db_config.opening_time,
        closing_time=db_config.closing_time,
        profile_image=db_config.profile_image
    )
    
    return response_data

@router.get("/business-config", response_model=BusinessConfigResponse)
async def get_business_config(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    config = db.query(BusinessConfig).filter(
        BusinessConfig.user_id == current_user.id
    ).first()
    
    if not config:
        raise HTTPException(
            status_code=404,
            detail="Business configuration not found"
        )
    
    config.working_days = json.loads(config.working_days)
    return config

@router.put("/business-config", response_model=BusinessConfigResponse)
async def update_business_config(
    config: BusinessConfigSchema,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_config = db.query(BusinessConfig).filter(
        BusinessConfig.user_id == current_user.id
    ).first()
    
    if not db_config:
        raise HTTPException(
            status_code=404,
            detail="Business configuration not found"
        )
    
    # Atualizar campos
    db_config.description = config.description
    db_config.working_days = json.dumps(config.working_days)
    db_config.opening_time = config.opening_time
    db_config.closing_time = config.closing_time
    if config.profile_image:
        db_config.profile_image = config.profile_image
    
    db.commit()
    db.refresh(db_config)
    
    db_config.working_days = json.loads(db_config.working_days)
    return db_config