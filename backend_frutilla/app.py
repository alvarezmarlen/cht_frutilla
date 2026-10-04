from flask import Flask, jsonify, request
import psycopg2 
from psycopg2.extras import RealDictCursor 
import os

app = Flask(__name__)

# Función para obtener la conexión a la base de datos
def get_db_connection():
    # DATABASE_URL viene definida desde el docker-compose.yml
    db_url = os.environ.get('DATABASE_URL')
    conn = psycopg2.connect(db_url, cursor_factory=RealDictCursor)
    return conn

@app.route('/api/productos', methods=['GET'])
def get_productos():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT * FROM productos;')
        productos = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify(productos), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    
@app.route('/api/productos/<int:id>', methods=['GET'])
def get_productos_id(id):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT * FROM productos WHERE id = %s', (id,))
        producto = cur.fetchone()
        cur.close()
        conn.close()
        
        if producto is None:
            return jsonify({'error': "Producto no encontrado"}), 404
        
        return jsonify(producto), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Ruta 3: Crear un nuevo producto (POST)
@app.route('/api/productos', methods=['POST'])
def create_producto():
    try:
        data = request.get_json()
        
        # Validar campos obligatorios
        if not data or 'nombre' not in data or 'precio' not in data:
            return jsonify({'error': 'Nombre y precio son obligatorios'}), 400

        nombre = data.get('nombre')
        descripcion = data.get('descripcion', '')
        precio = data.get('precio')
        stock = data.get('stock', 0)
        imagen_url = data.get('imagen_url', '')
        categoria = data.get('categoria', '')

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            '''INSERT INTO productos (nombre, descripcion, precio, stock, imagen_url, categoria) 
               VALUES (%s, %s, %s, %s, %s, %s) RETURNING *;''',
            (nombre, descripcion, precio, stock, imagen_url, categoria)
        )
        nuevo_producto = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()

        return jsonify(nuevo_producto), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Ruta 4: MODIFICACIÓN (PUT)
@app.route('/api/productos/<int:id>', methods=['PUT'])
def update_producto(id):
    try:
        data = request.get_json()
        
        if not data: 
            return jsonify({'error': 'No se  proporcionaron datos para actualizar'})
        
        nombre = data.get('nombre')
        descripcion = data.get('descripcion', '')
        precio = data.get('precio')
        stock = data.get('stock', 0)
        imagen_url = data.get('imagen_url', '')
        categoria = data.get('categoria', '')

        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute(
            '''UPDATE productos 
                SET nombre = %s, descripcion = %s, precio = %s, stock = %s, imagen_url = %s, categoria = %s
                WHERE id = %s
                RETURNING *;''',
            (nombre, descripcion, precio, stock, imagen_url, categoria, id)
        )
        
        producto_actualizado = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        
        if producto_actualizado is None:
            return jsonify({'error': 'Producto no encontrado'}), 404

        return jsonify(producto_actualizado), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# 5. BAJA (DELETE)
@app.route('/api/productos/<int:id>', methods=['DELETE'])
def delete_producto(id):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute("DELETE FROM productos WHERE id = %s RETURNING *;", (id,))
        producto_eliminado = cur.fetchone()
        
        conn.commit()
        cur.close()
        conn.close()
        
        # Si no encontró ningún producto con ese ID
        if producto_eliminado is None:
            return jsonify({'error': "Producto no econtrado"}), 404
        
        return jsonify({'message': f'Producto con id {id} eliminado correctamente'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)