from fastapi import FastAPI
from app.api.v1.endpoint import users, auth
from app.db.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Chatbot Management API")

@app.get("/")
def health_check():
    return {
        "status": "System Online"
    }

# connect routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(users.router, prefix="/api/v1/users", tags=["Users"])