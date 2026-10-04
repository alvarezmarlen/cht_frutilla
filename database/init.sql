-- 1. Crear tabla de productos para el catálogo
CREATE TABLE IF NOT EXISTS productos (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    precio NUMERIC(10, 2) NOT NULL,
    imagen_url VARCHAR(255),
    categoria VARCHAR(50)
);

-- 2. Crear tabla de mensajes para el formulario de contacto
CREATE TABLE IF NOT EXISTS mensajes (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    telefono VARCHAR(20),
    mensaje TEXT NOT NULL,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3. Insertar productos de prueba reales para cht.frutilla
INSERT INTO productos (nombre, descripcion, precio, imagen_url, categoria) 
VALUES 
('Cartera Tejida Frutilla', 'Cartera artesanal tejida a mano con diseño juvenil', 18.50, 'https://via.placeholder.com/150', 'Carteras'),
('Cintillo Tejido', 'Cintillo elástico para el cabello tejido a crochet', 6.00, 'https://via.placeholder.com/150', 'Accesorios'),
('Llavero Personalizado', 'Llavero tejido a mano ideal para mochilas o llaves', 4.50, 'https://via.placeholder.com/150', 'Llaveros');