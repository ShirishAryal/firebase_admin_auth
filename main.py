from fastapi import FastAPI, HTTPException
import firebase_admin
from firebase_admin import credentials
import firebase_admin.app_check
from pydantic import BaseModel

app = FastAPI()

class ServiceAccount(BaseModel):
    auth_provider_x509_cert_url: str
    auth_uri: str
    client_email: str
    client_id: str
    client_x509_cert_url: str
    private_key: str
    private_key_id: str
    project_id: str
    token_uri: str
    type: str
    universe_domain: str

@app.get("/")
def read_root():
    return {'message': 'Hello World'}

@app.post("/generate_token")
def get_token(service_account: ServiceAccount):
    try:
        service_account_dict = service_account.model_dump()
        if not firebase_admin._apps:
            cred = credentials.Certificate(service_account_dict)
            firebase_admin.initialize_app(cred)
        cred = credentials.Certificate(service_account_dict)
        access_token = cred.get_access_token()
        firebase_admin.delete_app(firebase_admin.get_app())
        return {"access_token": access_token.access_token, "token_expiry": access_token.expiry}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))