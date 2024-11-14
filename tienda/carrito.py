from flask import Blueprint, g, request, jsonify, render_template
from .login import login_required
from datetime import datetime
from .db import get_db
from flask import logging

bp = Blueprint('carrito', __name__, url_prefix='/carrito')

@bp.route('/add_to_cart', methods=['POST'])
@login_required
def add_to_cart():
    product_id = request.form.get('product_id')
    quantity = int(request.form.get('quantity', 1))

    db = get_db()
    with db.cursor() as cursor:
        # Revisar si el usuario ya tiene una orden "abierta" (estado = 1)
        cursor.execute(
            "SELECT id FROM Ordenes WHERE id_usuario = %s AND id_estado = %s",
            (g.user, 1)  # Asumiendo que el estado 1 es "abierto"
        )
        order = cursor.fetchone()

        if not order:
            # Crear una nueva orden si no existe una "abierta"
            cursor.execute(
                "INSERT INTO Ordenes (id_usuario, fecha_hora, id_estado) VALUES (%s, NOW(), %s) RETURNING id",
                (g.user, 1)  # Estado 1 como "abierto"
            )
            order_id = cursor.fetchone()[0]
        else:
            order_id = order[0]

        # Verificar si el producto ya está en Lineas_orden de esta orden
        cursor.execute(
            "SELECT id, cantidad FROM Lineas_orden WHERE id_orden = %s AND id_forma_producto = %s",
            (order_id, product_id)
        )
        item = cursor.fetchone()

        if item:
            # Si ya está, actualizar la cantidad
            new_quantity = item[1] + quantity
            cursor.execute(
                "UPDATE Lineas_orden SET cantidad = %s WHERE id = %s",
                (new_quantity, item[0])
            )
        else:
            # Si no está, insertarlo
            cursor.execute(
                "INSERT INTO Lineas_orden (id_orden, id_forma_producto, cantidad) VALUES (%s, %s, %s)",
                (order_id, product_id, quantity)
            )
        db.commit()
    
    return jsonify({"message": "Producto agregado al carrito"})


@bp.route('')
@login_required
def view_cart():
    get_db()
    db = g.get("db")
    with db.cursor() as cursor:
        # Obtener la orden abierta del usuario
        cursor.execute(
            "SELECT o.id, p.nombre, fp.precio FROM ordenes o "
            "JOIN lineas_orden lo ON o.id = lo.id_orden "
            "JOIN formas_producto fp ON lo.id_forma_producto = fp.id "
            "JOIN productos p ON fp.id_producto = p.id "
            "WHERE o.id_usuario = %s AND o.id_estado = %s",
            (g.user, 1)  # Estado 1 como "abierto"
        )
        cart_items = cursor.fetchall()
    
    return render_template('carrito.html', cart_items=cart_items)


@bp.route('/remove_from_cart', methods=['POST'])
@login_required
def remove_from_cart():
    product_id = request.form.get('product_id')

    db = get_db()
    with db.cursor() as cursor:
        # Obtener la orden abierta del usuario
        cursor.execute(
            "SELECT id FROM Ordenes WHERE id_usuario = %s AND id_estado = %s",
            (g.user, 1)
        )
        order = cursor.fetchone()

        if order:
            cursor.execute(
                "DELETE FROM Lineas_orden WHERE id_orden = %s AND id_forma_producto = %s",
                (order[0], product_id)
            )
            db.commit()

    return jsonify({"message": "Producto eliminado del carrito"})


@bp.route('/checkout', methods=['POST'])
@login_required
def checkout():
    db = get_db()
    with db.cursor() as cursor:
        # Obtener la orden abierta del usuario
        cursor.execute(
            "SELECT id FROM Ordenes WHERE id_usuario = %s AND id_estado = %s",
            (g.user, 1)
        )
        order = cursor.fetchone()

        if order:
            # Cambiar el estado de la orden a "completada" (suponiendo que el estado 2 es completada)
            cursor.execute(
                "UPDATE Ordenes SET id_estado = %s WHERE id = %s",
                (2, order[0])
            )
            db.commit()

    return jsonify({"message": "Compra completada"})
