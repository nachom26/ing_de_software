-- Crear tabla Regiones
CREATE TABLE Regiones (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(30) NOT NULL
);

-- Crear tabla Comunas
CREATE TABLE Comunas (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(30) NOT NULL,
    id_region INT NOT NULL,
    FOREIGN KEY (id_region) REFERENCES Regiones(id)
);

-- Crear tabla Usuarios
CREATE TABLE Usuarios (
    id SERIAL PRIMARY KEY,
    direccion VARCHAR(40) NOT NULL,
    id_comuna INT NOT NULL,
    id_region INT NOT NULL,
    nombre VARCHAR(40) NOT NULL,
    apellido VARCHAR(40) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    FOREIGN KEY (id_comuna) REFERENCES Comunas(id),
    FOREIGN KEY (id_region) REFERENCES Regiones(id)
);

-- Crear tabla Productos
CREATE TABLE Productos (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    descripcion TEXT,
    categoria VARCHAR(40),
    cantidad_valoraciones INT DEFAULT 0,
    valoracion_total INT DEFAULT 0
);

-- Crear tabla Valoraciones
CREATE TABLE Valoraciones (
    id_usuario INT NOT NULL,
    id_producto INT NOT NULL,
    valoracion INT CHECK (valoracion BETWEEN 1 AND 5),
    PRIMARY KEY (id_usuario, id_producto),
    FOREIGN KEY (id_usuario) REFERENCES Usuarios(id),
    FOREIGN KEY (id_producto) REFERENCES Productos(id)
);

-- Crear tabla Formas_producto
CREATE TABLE Formas_producto (
    id SERIAL PRIMARY KEY,
    id_producto INT NOT NULL,
    nombre VARCHAR(50),
    precio INT NOT NULL,
    inventario INT NOT NULL,
    ruta_imagen TEXT,
    medidas TEXT,
    color VARCHAR(40),
    FOREIGN KEY (id_producto) REFERENCES Productos(id)
);

-- Crear tabla Estados
CREATE TABLE Estados (
    id SERIAL PRIMARY KEY,
    estado VARCHAR(15) NOT NULL
);

-- Crear tabla Ordenes
CREATE TABLE Ordenes (
    id SERIAL PRIMARY KEY,
    id_usuario INT NOT NULL,
    fecha_hora TIMESTAMP NOT NULL,
    id_estado INT NOT NULL,
    FOREIGN KEY (id_usuario) REFERENCES Usuarios(id),
    FOREIGN KEY (id_estado) REFERENCES Estados(id)
);

-- Crear tabla Lineas_orden
CREATE TABLE Lineas_orden (
    id SERIAL PRIMARY KEY,
    id_orden INT NOT NULL,
    id_forma_producto INT NOT NULL,
    FOREIGN KEY (id_orden) REFERENCES Ordenes(id),
    FOREIGN KEY (id_forma_producto) REFERENCES Formas_producto(id)
);