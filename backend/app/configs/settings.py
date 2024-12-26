import logging

from pydantic.v1 import BaseSettings
from dotenv import load_dotenv

log = logging.getLogger(__name__)
if not load_dotenv():
    log.error(".env file not found.")

class ApplicationSettings(BaseSettings):
    """Define application configuration model.

    Constructor will attempt to determine the values of any fields not passed
    as keyword arguments by reading from the environment. Default values will
    still be used if the matching environment variable is not set.
    """

    DEBUG: bool = True
    PROJECT_NAME: str = "Project"
    DOCS_URL: str = "/"
   
    JWT_SECRET_KEY: str = "default"
    JWT_EXPIRE_TIME_MIN: int = 3000
   
    MONGODB_HOST: str = "localhost"
    MONGODB_DATABASE: str = "qsight"
    MONGODB_PORT: int= None

    SENDER_EMAIL: str = ""
    SENDER_PASSWORD: str = ""
    
    S3_BUCKET_NAME: str = "qsight-documents"
    
    AWS_REGION: str = "us-east-1"
    AWS_ACCESS_ID: str = ""
    AWS_SECRET_KEY: str = ""
    AWS_SESSION_TOKEN: str = ""

    SNS_TOPIC_ARN: str = ""
    SNS_POWER_ROLE_ARN: str = ""
    
    class Config:
        case_sensitive = True


settings = ApplicationSettings()
