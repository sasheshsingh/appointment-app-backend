# installation Instructions

## 1. Clone the repository::
### git clone https://github.com/sasheshsingh/appointment-app-backend


## 2. Navigate into the project directory:
### cd appointment-app-backend


## 3. Create a virtual environment (optional but recommended). Ref[https://sasheshsingh.medium.com/a-beginners-guide-of-installing-virtualenvwrapper-on-ubuntu-ce6259e4d609](https://sasheshsingh.medium.com/a-beginners-guide-of-installing-virtualenvwrapper-on-ubuntu-ce6259e4d609):
### workon myenv

## 4. create .env file. Add following variables
### DATABASE_URL=postgresql://postgres:abcdijkl@localhost:5432/appointment_app_db
### AZURE_CLIENT_ID
### AZURE_CLIENT_SECRET_KEY
### AZURE_AD_TENANT_ID
### AZURE_CLIENT_SECRET_VALUE
### GOOGLE_CLIENT_ID
### GOOGLE_CLIENT_SECRET
### STRIPE_SECRET_KEY
### STRIPE_PUBLISHABLE_KEY

## 5. Install the project dependencies:
### pip install -r requirements.txt

## 6. Start the FastAPI server:
## uvicorn main:app --reload

