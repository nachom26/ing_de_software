from flask import Blueprint, g, request, jsonify, render_template, redirect, url_for, flash
from .login import login_required
from datetime import datetime
from .db import get_db
from flask import logging

bp = Blueprint('carrito', __name__, url_prefix='/carrito')

@bp.route('/add_to_cart/<int:id_producto>')
@login_required
def add_to_cart(id_producto):
    product_id = id_producto

    get_db()
    db = g.get("db")
    with db.cursor() as cursor:
        # Revisar si el usuario ya tiene una orden "abierta" (estado = 1)
        cursor.execute(
            "SELECT id FROM ordenes WHERE id_usuario = %s AND id_estado = %s",
            (g.user, 1)  # Asumiendo que el estado 1 es "abierto"
        )
        order = cursor.fetchone()

        if not order:
            # Crear una nueva orden si no existe una "abierta"
            cursor.execute(
                "INSERT INTO ordenes (id_usuario, fecha_hora, id_estado) VALUES (%s, NOW(), %s) RETURNING id",
                (g.user, 1)  # Estado 1 como "abierto"
            )
            order_id = cursor.fetchone()[0]
        else:
            order_id = order[0]

        # Verificar si el producto ya está en lineas_orden de esta orden
        cursor.execute(
            "SELECT id FROM lineas_orden WHERE id_orden = %s AND id_forma_producto = %s",
            (order_id, product_id)
        )
        item = cursor.fetchone()

        if item:
            # Si el producto ya está en el carrito, retornar un mensaje
            flash("Producto ya estaba en el carrito")
            return redirect(url_for("carrito.view_cart"))
        else:
            # Si no está, insertarlo
            cursor.execute(
                "INSERT INTO lineas_orden (id_orden, id_forma_producto) VALUES (%s, %s)",
                (order_id, product_id)
            )
        db.commit()
    flash("Producto añadido al carrito")
    return redirect(url_for("carrito.view_cart"))


@bp.route('')
@login_required
def view_cart():
    get_db()
    db = g.get("db")
    with db.cursor() as cursor:
        # Obtener la orden abierta del usuario
        cursor.execute(
            "SELECT o.id, p.nombre, fp.precio, fp.ruta_imagen FROM ordenes o "
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

    get_db()
    db = g.get("db")
    with db.cursor() as cursor:
        # Obtener la orden abierta del usuario
        cursor.execute(
            "SELECT id FROM ordenes WHERE id_usuario = %s AND id_estado = %s",
            (g.user, 1)
        )
        order = cursor.fetchone()

        if order:
            cursor.execute(
                "DELETE FROM lineas_orden WHERE id_orden = %s AND id_forma_producto = %s",
                (order[0], product_id)
            )
            db.commit()

    return jsonify({"message": "Producto eliminado del carrito"})


@bp.route('/checkout')
@login_required
def checkout():
    get_db()
    db = g.get("db")
    with db.cursor() as cursor:
        # Obtener la orden abierta del usuario
        cursor.execute(
            "SELECT id FROM ordenes WHERE id_usuario = %s AND id_estado = %s",
            (g.user, 1)
        )
        order = cursor.fetchone()

        if order:
            # Cambiar el estado de la orden a "completada" (suponiendo que el estado 2 es completada)
            cursor.execute(
                "UPDATE ordenes SET id_estado = %s WHERE id = %s",
                (2, order[0])
            )
            db.commit()
    flash("Compra exitosa")
    return redirect(url_for("carrito.view_cart"))
