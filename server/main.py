from fastapi.staticfiles import StaticFiles  # ✅ ADDED
import os  # ✅ ADDED
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import database
from routers import (
    auth,
    products,
    orders,
    payment,
    settings,
    notifications,
    analytics,
    builder,
)

app = FastAPI(title="BikeHub API", version="1.0.0")

# ✅ ADDED — Serve uploaded images as static files
os.makedirs("uploads/products", exist_ok=True)
os.makedirs("uploads/payments", exist_ok=True)
os.makedirs("uploads/qr", exist_ok=True)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(products.router)
app.include_router(orders.router)
app.include_router(payment.router)
app.include_router(settings.router)
app.include_router(notifications.router)
app.include_router(analytics.router)
app.include_router(builder.router)


@app.on_event("startup")
async def startup():
    await database.connect()
    print("✅ Database connected!")


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
    print("❌ Database disconnected!")


@app.get("/")
async def root():
    return {"message": "BikeHub backend is running!"}


@app.get("/test-db")
async def test_db():
    query = (
        "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'"
    )
    rows = await database.fetch_all(query)
    tables = [row["table_name"] for row in rows]
    return {"tables": tables}
