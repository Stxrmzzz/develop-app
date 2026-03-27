from pydantic import BaseModel

class PedidoResponse(BaseModel):
    pedido_id: int
    total: float