from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import engine, Base, SessionLocal
from models import Carrito, CarritoItem, Producto, Pedido, PedidoItem
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

@app.post("/pedidos")
def crear_pedido(db: Session = Depends(get_db)):
    #Convierte el carrito actual en un pedido
    carrito = db.query(Carrito).filter(Carrito.id == 1).first()
    if not carrito:
        raise HTTPException(status_code=400, detail="El carrito está vacío")

    items = db.query(CarritoItem).filter(CarritoItem.carrito_id == carrito.id).all()
    if not items:
        raise HTTPException(status_code=400, detail="El carrito está vacío")

    total = 0
    pedido = Pedido(usuario_id=1, total=0)
    db.add(pedido)
    db.commit()
    db.refresh(pedido)

    for item in items:
        producto = db.query(Producto).filter(Producto.id == item.producto_id).first()

        precio_final = producto.precio * (1 + producto.iva)
        subtotal = precio_final * item.cantidad
        total += subtotal

        pedido_item = PedidoItem(
            pedido_id=pedido.id,
            producto_id=item.producto_id,
            cantidad=item.cantidad,
            precio_unitario=precio_final
        )

        db.add(pedido_item)

# Limpia carrito 
    db.query(CarritoItem).filter(
        CarritoItem.carrito_id == carrito.id
    ).delete()

    pedido.total = total
    db.commit()

    return {
        "message": "Pedido creado",
        "pedido_id": pedido.id,
        "total": total
    }

@app.get("/pedidos")
def listar_pedidos(db: Session = Depends(get_db)):
    """Vista del administrador — ver todos los pedidos"""
    pedidos = db.query(Pedido).all()
    resultado = []
    for pedido in pedidos:
        items = db.query(PedidoItem).filter(PedidoItem.pedido_id == pedido.id).all()
        detalle = []
        for item in items:
            producto = db.query(Producto).filter(Producto.id == item.producto_id).first()
            detalle.append({
                "producto": producto.nombre,
                "cantidad": item.cantidad,
                "precio_unitario": item.precio_unitario,
                "subtotal": item.precio_unitario * item.cantidad
            })
        resultado.append({
            "pedido_id": pedido.id,
            "total": pedido.total,
            "productos": detalle
        })
    return resultado