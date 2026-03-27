from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import engine, Base, SessionLocal
from models import Carrito, CarritoItem, Producto
from schemas import CarritoItemCreate
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel

class CarritoItemResponse(BaseModel):
    id: int
    producto_id: int
    cantidad: int

    class Config:
        from_attributes = True

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/carrito")
def agregar_al_carrito(data: CarritoItemCreate, db: Session = Depends(get_db)):
    carrito = db.query(Carrito).filter(Carrito.id == 1).first()
    if not carrito:
        carrito = Carrito(id=1)
        db.add(carrito)
        db.commit()
        db.refresh(carrito)



    item = db.query(CarritoItem).filter(
        CarritoItem.carrito_id == carrito.id,
        CarritoItem.producto_id == data.producto_id
    ).first()

    if item:
        item.cantidad += data.cantidad
    else:
        item = CarritoItem(carrito_id=carrito.id, producto_id=data.producto_id, cantidad=data.cantidad)
        db.add(item)

    db.commit()
    db.refresh(item)
    return item

@app.get("/carrito", response_model=List[CarritoItemResponse])
def ver_carrito(db: Session = Depends(get_db)):
    return db.query(CarritoItem).all()

@app.put("/carrito/{item_id}")
def editar_cantidad(item_id: int, cantidad: int, db: Session = Depends(get_db)):
    item = db.query(CarritoItem).filter(CarritoItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item no encontrado")
    if cantidad <= 0:
        db.delete(item)
        db.commit()
        return {"message": "Item eliminado del carrito"}
    item.cantidad = cantidad
    db.commit()
    db.refresh(item)
    return item

@app.delete("/carrito/{item_id}")
def eliminar_del_carrito(item_id: int, db: Session = Depends(get_db)):
    item = db.query(CarritoItem).filter(CarritoItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item no encontrado")
    db.delete(item)
    db.commit()
    return {"message": "Producto eliminado del carrito"}