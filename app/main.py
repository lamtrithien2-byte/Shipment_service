from fastapi import FastAPI

from app.api.api_auth import router as auth_router

app = FastAPI(title="Shipment Service")

app.include_router(auth_router)


@app.get("/")
def root():
    return {
        "message": "Shipment Service API",
    }
