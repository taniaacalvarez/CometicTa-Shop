from flask import Flask, render_template, session, redirect, url_for, request
import json
from pathlib import Path

app = Flask(__name__)
app.secret_key = 'clave_secreta_segura'

DATA_FILE = Path(__file__).parent / "productos.json"

def load_products():
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

@app.route('/')
def index():
    productos = load_products()
    session.setdefault('cart', {})
    session.setdefault('cart_count', sum(session['cart'].values()) if session['cart'] else 0)
    return render_template('index.html', productos=productos, session=session)

@app.route('/agregar_carrito/<int:producto_id>', methods=['POST'])
def add_to_cart(producto_id):
    cart = session.get('cart', {})
    cart[str(producto_id)] = cart.get(str(producto_id), 0) + 1
    session['cart'] = cart
    session['cart_count'] = sum(cart.values())
    return redirect(url_for('index'))

@app.route('/carrito')
def cart():
    productos = load_products()
    cart = session.get('cart', {})
    productos_en_carrito = []

    total_general = 0
    for producto in productos:
        pid = str(producto['id'])
        if pid in cart:
            cantidad = cart[pid]
            subtotal = producto['precio'] * cantidad
            total_general += subtotal
            productos_en_carrito.append({
                **producto,
                "cantidad": cantidad,
                "subtotal": subtotal
            })

    return render_template('carrito.html', productos_en_carrito=productos_en_carrito, total_general=total_general)
@app.route('/eliminar/<int:producto_id>', methods=['POST'])
def eliminar_del_carrito(producto_id):
    cart = session.get('cart', {})
    pid = str(producto_id)
    if pid in cart:
        del cart[pid]
    session['cart'] = cart
    session['cart_count'] = sum(cart.values())
    return redirect(url_for('cart'))

@app.route('/admin')
def admin():
    return "Panel admin (por implementar)"

@app.route('/confirmar_compra')
def confirmar_compra():
    # Vacía el carrito después de confirmar la compra
    session['cart'] = {}
    session['cart_count'] = 0
    return render_template('confirmacion.html')


if __name__ == '__main__':
    app.run(debug=True)
