# app/main.py
from fastapi import FastAPI

# Importa los modelos SIN usar el nombre 'app' en tu namespace:
from app import models as app_models  # noqa: F401  (solo para registrar mapeos)

from app.api.routes.products import router as products_router
from app.api.routes.inventory import router as inventory_router

app = FastAPI(title="SHSystem API")

app.include_router(products_router)
app.include_router(inventory_router)
