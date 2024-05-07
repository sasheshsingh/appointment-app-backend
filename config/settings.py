

import os
from dotenv import load_dotenv


load_dotenv()

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

print(SQLALCHEMY_DATABASE_URL)

AZURE_AD_TENANT_ID = os.getenv("AZURE_AD_TENANT_ID")

AZURE_CLIENT_ID = os.getenv("AZURE_CLIENT_ID")

AZURE_CLIENT_SECRET_KEY = os.getenv("AZURE_CLIENT_SECRET_KEY")

AZURE_CLIENT_SECRET_VALUE = os.getenv("AZURE_CLIENT_SECRET_VALUE")