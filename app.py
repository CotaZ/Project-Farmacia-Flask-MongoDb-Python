from flask import Flask, render_template, request, jsonify, redirect, url_for, send_from_directory
import database as dbase
from medicamento import Medicamento, Proveedor
import json
from bson.objectid import ObjectId
import pymongo

db = dbase.dbConnection()

app = Flask(__name__)



@app.route('/')
def home():
    medicamentos = db['medicamentos']
    medicamentosReceived = medicamentos.find()
    return render_template('inicio.html', medicamentos=medicamentosReceived)



@app.route('/medicamentos')
def mostrar_medicamentos():
    medicamentos = db['medicamentos']
    medicamentosReceived = medicamentos.find()
    return render_template('index.html', medicamentos=medicamentosReceived)



# Ruta para mostrar la lista de proveedores
@app.route('/proveedores')
def mostrar_proveedores():
    proveedores = db['proveedores']
    proveedores_received = proveedores.find()
    return render_template('proveedores.html', proveedores=proveedores_received)



# Método POST para crear los datos de medicamentos
@app.route('/medicamentos', methods=['POST'])
def addMedicamento():
    medicamentos = db['medicamentos']

    # Obtener los datos del formulario
    sku = request.form['sku']
    nombre = request.form['nombre']
    laboratorio = request.form['laboratorio']
    principio_activo = request.form['principio_activo']
    accion_terapeutica = request.form['accion_terapeutica']
    presentacion = request.form['presentacion']
    dosis = request.form['dosis']
    bioequivalente = request.form['bioequivalente']
    stock = int(request.form['stock'])
    precio = int(request.form['precio'])  # Convertir el precio a un entero
    proveedor_nombre = request.form['proveedor_nombre']
    proveedor_rut = request.form['proveedor_rut']

    # Verificar que los campos requeridos no estén vacíos
    if sku and nombre and laboratorio and principio_activo and accion_terapeutica and presentacion and dosis and bioequivalente and stock and precio and proveedor_nombre and proveedor_rut:
        # Construir el objeto Medicamento y convertirlo a un diccionario para insertarlo en la base de datos
        medicamento = {
            "sku": sku,
            "nombre": nombre,
            "laboratorio": laboratorio,
            "principio_activo": principio_activo,
            "accion_terapeutica": accion_terapeutica,
            "presentacion": presentacion,
            "dosis": dosis,
            "bioequivalente": bioequivalente,
            "stock": stock,
            "precio": precio,
            "proveedor": [
                {"nombre": proveedor_nombre},
                {"rut": proveedor_rut}
            ]
        }
        medicamentos.insert_one(medicamento)

        return redirect(url_for('home'))
    else:
        return notFound()

@app.route('/delete/<string:medicamento_nombre>')
def delete(medicamento_nombre):
    medicamentos = db['medicamentos']
    medicamentos.delete_one({'nombre': medicamento_nombre})
    return redirect(url_for('mostrar_medicamentos'))

@app.route('/edit/<string:medicamento_name>', methods=['POST'])
def edit(medicamento_name):
    medicamentos = db['medicamentos']

    # Obtener los datos del formulario
    nombre = request.form['nombre']
    laboratorio = request.form['laboratorio']
    principio_activo = request.form['principio_activo']
    accion_terapeutica = request.form['accion_terapeutica']
    presentacion = request.form['presentacion']
    dosis = request.form['dosis']
    bioequivalente = request.form['bioequivalente']
    stock = request.form['stock']
    precio = request.form['precio']
    proveedor_nombre = request.form['proveedor_nombre']
    proveedor_rut = request.form['proveedor_rut']

    # Verificar que los campos requeridos no estén vacíos
    if nombre and laboratorio and principio_activo and accion_terapeutica and presentacion and dosis and bioequivalente and stock and precio:
        # Construir el objeto con los campos a actualizar en la base de datos
        campos_actualizados = {
            'nombre': nombre,
            'laboratorio': laboratorio,
            'principio_activo': principio_activo,
            'accion_terapeutica': accion_terapeutica,
            'presentacion': presentacion,
            'dosis': dosis,
            'bioequivalente': bioequivalente,
            'stock': int(stock),
            'precio': int(precio),
            "proveedor": [
                {"nombre": proveedor_nombre},
                {"rut": proveedor_rut}
            ]
        }

        # Actualizar los campos en la base de datos para el medicamento con el nombre especificado
        medicamentos.update_one({'nombre': medicamento_name}, {'$set': campos_actualizados})

        return redirect(url_for('mostrar_medicamentos'))
    else:
        return "Faltan campos requeridos en el formulario"
    
medicamentos_collection = db['medicamentos']

@app.route('/listar_medicamentos', methods=['GET'])
def listarMedicamentos():
    # Obtener todos los medicamentos desde la base de datos
    medicamentos = list(medicamentos_collection.find())

    return render_template('listar_medicamentos.html', medicamentos=medicamentos)



# Método POST para crear los datos del proveedor
@app.route('/cargar_proveedores', methods=['GET'])
def cargar_proveedores():
    with open('proveedores.json', 'r') as file:
        proveedores = json.load(file)
        db.proveedores.insert_many(proveedores)
    return redirect(url_for('home'))

@app.route('/proveedores', methods=['GET', 'POST'])
def proveedores():
    if request.method == 'POST':
        nombre = request.form['nombre']
        razon_social = request.form['razon_social']
        rut = request.form['rut']
        direccion = request.form['direccion']
        email = request.form['email']
        fono = request.form['fono']
        productos = request.form['productos'].split(',')

        proveedor = {
            "nombre": nombre,
            "razon_social": razon_social,
            "rut": rut,
            "direccion": direccion,
            "email": email,
            "fono": fono,
            "productos": productos
        }

        db.proveedores.insert_one(proveedor)
        return redirect(url_for('proveedores'))

    else:
        proveedores = db.proveedores.find()
        return render_template('proveedores.html', proveedores=proveedores)

#  ruta para editar un proveedor
@app.route('/editar_proveedor/<string:proveedor_id>', methods=['GET', 'POST'])
def editarProveedor(proveedor_id):
    proveedor = db.proveedores.find_one({"_id": ObjectId(proveedor_id)})

    if request.method == 'POST':
        nombre = request.form['nombre']
        razon_social = request.form['razon_social']
        rut = request.form['rut']
        direccion = request.form['direccion']
        email = request.form['email']
        fono = request.form['fono']
        productos = request.form['productos'].split(',')

        db.proveedores.update_one(
            {"_id": ObjectId(proveedor_id)},
            {
                "$set": {
                    "nombre": nombre,
                    "razon_social": razon_social,
                    "rut": rut,
                    "direccion": direccion,
                    "email": email,
                    "fono": fono,
                    "productos": productos
                }
            }
        )
        return redirect(url_for('proveedores'))

    else:
        return render_template('editar_proveedor.html', proveedor=proveedor)



@app.route('/eliminar_proveedor/<string:proveedor_id>', methods=['POST'])
def eliminar_proveedor(proveedor_id):
    # Eliminar el proveedor de la base de datos
    db.proveedores.delete_one({"_id": ObjectId(proveedor_id)})

    return redirect(url_for('proveedores'))

# Ruta para realizar la búsqueda de medicamentos y mostrar los resultados
@app.route('/buscar_medicamento', methods=['GET'])
def buscar_medicamento():
    nombre_medicamento = request.args.get('nombre')
    medicamentos = db.medicamentos.find({'nombre': nombre_medicamento}) if nombre_medicamento else db.medicamentos.find()
    return render_template('resultados_busqueda.html', medicamentos=medicamentos)


# Ruta para realizar la búsqueda de proveedores y mostrar los resultados
@app.route('/buscar_proveedor', methods=['GET'])
def buscarProveedor():
    nombre_proveedor = request.args.get('nombre')
    proveedores = db.proveedores.find({'nombre': nombre_proveedor}) if nombre_proveedor else db.proveedores.find()
    return render_template('buscar_proveedor.html', proveedores=proveedores)

@app.route('/videos/<nombre_del_video>')
def cargar_video(nombre_del_video):
    return send_from_directory('ruta/a/tu/carpeta/de/videos', nombre_del_video)



@app.errorhandler(404)
def notFound(error=None):
    message = {
        'mensaje': 'no encontrado ' + request.url,
        'status': '404 Not Found'
    }
    return jsonify(message), 404

if __name__ == '__main__':
    app.run(debug=True, port=4000)
