from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    company_name = Column(String)
    business_type = Column(String)
    country = Column(String)
    phone = Column(String)
    hashed_password = Column(String)
    is_configured = Column(Boolean, default=False)
    
    # Relacionamento com a configuração
    business_config = relationship("BusinessConfig", back_populates="user", uselist=False)

class BusinessConfig(Base):
    __tablename__ = "business_configs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    description = Column(String)
    working_days = Column(String)  # Vamos armazenar como JSON string
    opening_time = Column(String)
    closing_time = Column(String)
    profile_image = Column(String, nullable=True)
    
    # Relacionamento com o usuário
    user = relationship("User", back_populates="business_config")