from pydantic import BaseModel

class CarritoItemCreate(BaseModel):
    producto_id: int
    cantidad: int

