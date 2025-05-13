from flask import Flask, render_template, request
from pymongo import MongoClient
from datetime import date
app = Flask(__name__)
client = MongoClient("mongodb+srv://cgarriv1510:ba8TsQCTKMIWhOk2@flaskmongodb.qcsfafi.mongodb.net/")
app.db = client.Tienda_Gestion

productos = [productos for productos in app.db.productos.find({})]

@app.route('/dashboard', methods=['GET','POST'])

def registro():
    administrador = {"nombre_admin" : "Francisco", "tienda" : "TecnoMarket", "fecha" : date.today()}


    usuarios = [
        {"nombre": "Ana", "email": "Ana@gmail.com", "activo":True, "pedidos": 3},
        {"nombre": "Luis", "email": "Luis@gmail.com", "activo":False, "pedidos": 3},
        {"nombre": "Carmen", "email": "Carmen@gmail.com", "activo":True, "pedidos": 3},
        {"nombre": "Pedro", "email": "Pedro@gmail.com", "activo":True, "pedidos": 0}
    ]

    pedidos_recientes = [
        {"cliente": "Ana", "total":299.00, "fecha":"2025-05-14"},
        {"cliente": "Ana", "total": 35.00, "fecha": "2025-05-24"},
        {"cliente": "Ana", "total": 80.00, "fecha": "2025-04-13"},


        {"cliente": "Luis", "total":15.00, "fecha":"2025-04-13"},
        {"cliente": "Luis", "total": 5.00, "fecha": "2025-04-14"},
        {"cliente": "Luis", "total": 10.00, "fecha": "2025-05-24"},

        {"cliente": "Carmen", "total":50.00, "fecha":"2025-05-21"},
        {"cliente": "Carmen", "total": 80.00, "fecha": "2025-05-14"},
        {"cliente": "Carmen", "total": 10.00, "fecha": "2025-06-11"},
    ]

    if request.method == "POST":
        p_nombre = request.form.get("nombre")
        p_precio = request.form.get("precio")
        p_stock = request.form.get("stock")
        p_categoria = request.form.get("categoria")
        producto_nuevo ={"nombre": p_nombre, "precio": p_precio, "stock": p_stock, "categoria": p_categoria}
        productos.append(producto_nuevo)
        app.db.productos.insert_one(producto_nuevo)


    suma_total = 0.0

    suma_total = sum(pedido["total"] for pedido in pedidos_recientes[:-1])

    return render_template("dashboard.html", productos=productos, usuarios=usuarios, pedidos=pedidos_recientes,total=suma_total , **administrador)

if __name__ == '__main__':
    app.run()
