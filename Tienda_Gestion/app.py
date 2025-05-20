from flask import Flask, render_template, request, redirect, url_for, abort, flash
from datetime import datetime
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)
app.secret_key = "supersecretkey"  # necesario para mensajes flash

# Conexión MongoDB
client = MongoClient("mongodb+srv://cgarriv1510:ba8TsQCTKMIWhOk2@flaskmongodb.qcsfafi.mongodb.net/")
app.db = client.Tienda_Gestion

# Clase Usuario
class Usuario:
    def __init__(self, nombre, email, contraseña):
        self.nombre = nombre
        self.email = email
        self.contraseña = contraseña
        self.fecha_registro = datetime.now()

# --- RUTAS ---
@app.route('/')
@app.route('/dashboard')
def dashboard():
    productos = list(app.db.productos.find())
    usuarios = list(app.db.usuarios.find())
    pedidos = list(app.db.pedidos.find())

    # Calcular totales y datos importantes:
    total_stock = sum(p['stock'] for p in productos)
    clientes_activos = sum(1 for u in usuarios if u.get('activo', True))
    cliente_mas_pedidos = None
    max_pedidos = 0
    for u in usuarios:
        pedidos_cliente = app.db.pedidos.count_documents({"cliente_email": u['email']})
        if pedidos_cliente > max_pedidos:
            max_pedidos = pedidos_cliente
            cliente_mas_pedidos = u['nombre']
    ingresos_totales = sum(p.get('total', 0) for p in pedidos)

    return render_template('dashboard.html',
                           productos=productos,
                           usuarios=usuarios,
                           pedidos=pedidos,
                           total_stock=total_stock,
                           clientes_activos=clientes_activos,
                           cliente_mas_pedidos=cliente_mas_pedidos,
                           ingresos_totales=ingresos_totales,
                           fecha_actual=datetime.now().strftime("%d/%m/%Y"))

@app.route('/añadir-producto', methods=['GET', 'POST'])
def añadir_producto():
    if request.method == 'POST':
        nombre = request.form['nombre']
        precio = float(request.form['precio'])
        stock = int(request.form['stock'])
        categoria = request.form['categoria']
        app.db.productos.insert_one({
            'nombre': nombre,
            'precio': precio,
            'stock': stock,
            'categoria': categoria
        })
        flash('Producto añadido con éxito!')
        return redirect(url_for('añadir_producto'))

    return render_template('añadir_producto.html')

@app.route('/productos')
def ver_productos():
    productos = list(app.db.productos.find())
    return render_template('lista_productos.html', productos=productos)

@app.route('/productos/<id_producto>')
def detalle_producto(id_producto):
    producto = app.db.productos.find_one({"_id": ObjectId(id_producto)})
    if not producto:
        return render_template('404.html'), 404
    return render_template('detalle_producto.html', producto=producto)

@app.route('/registro-usuario', methods=['GET', 'POST'])
def registro_usuario():
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        contraseña = request.form['contraseña']
        usuario = Usuario(nombre, email, contraseña)
        app.db.usuarios.insert_one({
            'nombre': usuario.nombre,
            'email': usuario.email,
            'contraseña': usuario.contraseña,
            'fecha_registro': usuario.fecha_registro
        })
        flash('Usuario registrado con éxito!')
        return redirect(url_for('registro_usuario'))
    return render_template('registro_usuario.html')

@app.route('/usuarios')
def lista_usuarios():
    usuarios = list(app.db.usuarios.find())
    return render_template('lista_usuarios.html', usuarios=usuarios)

# Página 404 personalizada
@app.errorhandler(404)
def pagina_no_encontrada(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run()
