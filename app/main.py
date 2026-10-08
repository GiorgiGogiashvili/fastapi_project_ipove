from fastapi import FastAPI

from app.api.routes.requests import router as requests_router
from app.api.routes.specialists import router as specialists_router
from app.api.routes.auth import router as auth_router
from app.api.routes.bookings import router as bookings_router
from app.api.routes.payments import router as payments_router


app = FastAPI(
    title="Smart Service Marketplace",
    description="Multilingual specialist search platform",
    version="0.4.0",
)


app.include_router(requests_router)
app.include_router(specialists_router)
app.include_router(auth_router)
app.include_router(bookings_router)
app.include_router(payments_router)


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "message": "Backend is running",
    }