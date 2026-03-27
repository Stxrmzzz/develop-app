from pydantic import BaseModel
from typing import Optional

class CategoriaCreate(BaseModel):
    nombre: str

class ProductoCreate(BaseModel):
    nombre: str
    descripcion: str
    precio: float
    iva: float = 0.19
    peso: Optional[float] = None
    categoria_id: int

class ProductoResponse(BaseModel):
    id: int
    nombre: str
    descripcion: str
    precio: float
    iva: float
    peso: Optional[float]
    categoria_id: int

    class Config:
        from_attributes = True

class ProductoUpdate(BaseModel):
    nombre: str
    descripcion: str
    precio: float
    iva: float = 0.19
    peso: Optional[float] = None
    categoria_id: int