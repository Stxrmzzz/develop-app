from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import engine, Base, SessionLocal
from models import Categoria, Producto
from schemas import CategoriaCreate, ProductoCreate, ProductoResponse, ProductoUpdate
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

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# HOME
@app.get("/home", response_model=List[ProductoResponse])
def home(db: Session = Depends(get_db)):
    return db.query(Producto).all()

# CATEGORIAS
@app.post("/categorias")
def crear_categoria(datos: CategoriaCreate, db: Session = Depends(get_db)):
    categoria = Categoria(nombre=datos.nombre)
    db.add(categoria)
    db.commit()
    db.refresh(categoria)
    return categoria

@app.get("/categorias")
def listar_categorias(db: Session = Depends(get_db)):
    return db.query(Categoria).all()

@app.get("/categorias/{categoria_id}/productos")
def productos_por_categoria(categoria_id: int, db: Session = Depends(get_db)):
    return db.query(Producto).filter(Producto.categoria_id == categoria_id).all()

@app.put("/categorias/{categoria_id}")
def editar_categoria(categoria_id: int, datos: CategoriaCreate, db: Session = Depends(get_db)):
    categoria = db.query(Categoria).filter(Categoria.id == categoria_id).first()
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    categoria.nombre = datos.nombre
    db.commit()
    db.refresh(categoria)
    return categoria

@app.delete("/categorias/{categoria_id}")
def eliminar_categoria(categoria_id: int, db: Session = Depends(get_db)):
    categoria = db.query(Categoria).filter(Categoria.id == categoria_id).first()
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    
    productos = db.query(Producto).filter(Producto.categoria_id == categoria_id).first()
    if productos:
        raise HTTPException(status_code=400, detail="No puedes eliminar una categoría que tiene productos asociados")
    
    db.delete(categoria)
    db.commit()
    return {"message": "Categoría eliminada"}

# PRODUCTOS
@app.post("/productos")
def crear_producto(producto: ProductoCreate, db: Session = Depends(get_db)):
    nuevo = Producto(**producto.dict())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

@app.get("/productos", response_model=List[ProductoResponse])
def listar_productos(db: Session = Depends(get_db)):
    return db.query(Producto).all()

@app.get("/productos/{producto_id}")
def obtener_producto(producto_id: int, db: Session = Depends(get_db)):
    producto = db.query(Producto).filter(Producto.id == producto_id).first()
    
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    return producto

@app.put("/productos/{producto_id}")
def actualizar_producto(producto_id: int, datos: ProductoUpdate, db: Session = Depends(get_db)):
    producto = db.query(Producto).filter(Producto.id == producto_id).first()
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    for key, value in datos.dict().items():
        setattr(producto, key, value)
    db.commit()
    db.refresh(producto)
    return producto


@app.delete("/productos/{producto_id}")
def eliminar_producto(producto_id: int, db: Session = Depends(get_db)):
    producto = db.query(Producto).filter(Producto.id == producto_id).first()
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    db.delete(producto)
    db.commit()
    return {"message": "Producto eliminado"}