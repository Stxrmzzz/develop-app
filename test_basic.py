def test_producto_precio():
    producto = {
        "nombre": "PC",
        "precio": 1000
    }

    assert producto["precio"] > 0


def test_carrito_cantidad():
    item = {
        "producto_id": 1,
        "cantidad": 2
    }

    assert item["cantidad"] > 0


def test_total_pedido():
    precio = 100
    cantidad = 3
    total = precio * cantidad

    assert total == 300