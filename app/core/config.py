from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Scheduling API"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = "your-secret-key-here"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8

    # Stripe configs
    STRIPE_SECRET_KEY: str = "sk_test_51IgJQaGmo0gTo4AA8L35rnAF7g0KqGdriQeRcyacZPgxPq4bljd6dai5ICxOE2eGmrShclSWRlTVGemQrN9AgWkd00fcK6RKPP"
    STRIPE_PUBLISHABLE_KEY: str = "pk_test_51IgJQaGmo0gTo4AAnwJocurJYvxwUkOfQNMwBtXwn8mbYjZEBflx8DW7ntMsycNGjfX0HcC0Sj1MH26U3vlzOCm000N8fRcowG"
    STRIPE_WEBHOOK_SECRET: str = "seu_stripe_webhook_secret"
    
    # Price IDs dos seus produtos no Stripe
    STRIPE_PRICE_ID_MONTHLY: str = "price_id_do_plano_mensal"
    STRIPE_PRICE_ID_YEARLY: str = "price_id_do_plano_anual"

    class Config:
        case_sensitive = True

settings = Settings()