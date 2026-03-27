from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from jose import jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from database import engine, Base, SessionLocal
from models import Usuario
from schemas import LoginRequest
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
Base.metadata.create_all(bind=engine)

SECRET_KEY = "clave_secreta_123"
ALGORITHM = "HS256"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.on_event("startup")
def crear_usuario_default():
    db = SessionLocal()
    existe = db.query(Usuario).filter(Usuario.username == "admin").first()
    if not existe:
        hashed = pwd_context.hash("admin123")
        usuario = Usuario(username="admin", password=hashed)
        db.add(usuario)
        db.commit()
    db.close()

@app.post("/login")
def login(datos: LoginRequest, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.username == datos.username).first()
    if not usuario or not pwd_context.verify(datos.password, usuario.password):
        raise HTTPException(status_code=401, detail="Usuario o contraseña incorrectos")
    token = jwt.encode(
        {"sub": usuario.username, "exp": datetime.utcnow() + timedelta(hours=8)},
        SECRET_KEY,
        algorithm=ALGORITHM
    )
    return {"access_token": token, "token_type": "bearer"}