from flask import Flask, render_template
from datetime import date
app = Flask(__name__)


@app.route('/dashboard')
def registro():
    administrador = {"nombre_admin" : "Francisco", "tienda" : "TecnoMarket", "fecha" : date.today()}
    productos = [
        {"nombre": "raton", "precio": 35.00, "stock": 50, "categoria": "Tecnologia"},
        {"nombre": "teclado", "precio": 50.00, "stock": 120, "categoria": "Tecnologia"},
        {"nombre": "monitor", "precio": 299.00, "stock": 0, "categoria": "Tecnologia"},
        {"nombre": "pala", "precio": 10.00, "stock": 30, "categoria": "Jardineria"},
        {"nombre": "mesita", "precio": 80.00, "stock": 15, "categoria": "Muebles"},
        {"nombre": "maceta", "precio": 5.00, "stock": 40, "categoria": "Jardineria"},
        {"nombre": "compost", "precio": 15.00, "stock": 10, "categoria": "Jardineria"}
    ]

    usuarios = [
        {"nombre": "Ana", "email": "Ana@gmail.com", "activo":True, "pedidos": 3},
        {"nombre": "Luis", "email": "Luis@gmail.com", "activo":False, "pedidos": 3},
        {"nombre": "Carmen", "email": "Carmen@gmail.com", "activo":True, "pedidos": 3},
        {"nombre": "Pedro", "email": "Pedro@gmail.com", "activo":True, "pedidos": 0}
    ]

    pedidos_recientes = [
        {"cliente": "Ana", "total":3, "fecha":"2025-05-14"},
        {"cliente": "Ana", "total": 15, "fecha": "2025-05-24"},
        {"cliente": "Ana", "total": 8, "fecha": "2025-04-13"},


        {"cliente": "Luis", "total":1, "fecha":"2025-04-13"},
        {"cliente": "Luis", "total": 5, "fecha": "2025-04-14"},
        {"cliente": "Luis", "total": 13, "fecha": "2025-05-24"},

        {"cliente": "Carmen", "total":7, "fecha":"2025-05-21"},
        {"cliente": "Carmen", "total": 9, "fecha": "2025-05-14"},
        {"cliente": "Carmen", "total": 1, "fecha": "2025-06-11"}
    ]


    return render_template("dashboard.html", productos=productos, usuarios=usuarios, pedidos=pedidos_recientes, **administrador)
if __name__ == '__main__':
    app.run()
