from sqlalchemy import Column, Integer, String, Float, ForeignKey
from database import Base

class Categoria(Base):
    __tablename__ = "categorias"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)

class Producto(Base):
    __tablename__ = "productos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100))
    descripcion = Column(String(255))
    precio = Column(Float)
    iva = Column(Float, default=0.19)
    peso = Column(Float, nullable=True)
    categoria_id = Column(Integer, ForeignKey("categorias.id"))