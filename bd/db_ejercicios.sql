-- Creación de la base de datos y selección
CREATE DATABASE IF NOT EXISTS db_ejercicios;
USE db_ejercicios;

-- Tabla Usuarios
CREATE TABLE Usuarios (
    idUsuario INT NOT NULL,
    Nombre VARCHAR(50) NOT NULL,
    Edad INT NOT NULL,
    Genero VARCHAR(50) NOT NULL,
    Fecha_registro DATE NOT NULL,
    Comentarios_medicos VARCHAR(200) NOT NULL,
    PRIMARY KEY (idUsuario)
);

-- Tabla Sesiones
CREATE TABLE Sesiones (
    idSesion INT NOT NULL,
    idUsuario INT NOT NULL,
    Fecha_sesion DATE NOT NULL,
    Duracion INT NOT NULL,
    Tipo_ejercicio VARCHAR(50) NOT NULL,
    PRIMARY KEY (idSesion),
    FOREIGN KEY (idUsuario) REFERENCES Usuarios(idUsuario)
);

-- Tabla Progreso
CREATE TABLE Progreso (
    idProgreso INT NOT NULL,
    idUsuario INT NOT NULL,
    Fecha_calculo DATE NOT NULL,
    Fuerza_promedio FLOAT NOT NULL,
    Movilidad_horizontal INT NOT NULL,
    Movilidad_vertical INT NOT NULL,
    Precision_diagonal INT NOT NULL,
    Mejora_fuerza FLOAT NOT NULL,
    PRIMARY KEY (idProgreso),
    FOREIGN KEY (idUsuario) REFERENCES Usuarios(idUsuario)
);

-- Tabla Lecturas
CREATE TABLE Lecturas (
    idLectura INT NOT NULL,
    idSesion INT NOT NULL,
    Joytstick_numero INT NOT NULL,
    Eje_x INT NOT NULL,
    Eje_y INT NOT NULL,
    Nivel_x INT NOT NULL,
    Nivel_y INT NOT NULL,
    Boton BOOLEAN NOT NULL,
    Direccion VARCHAR(50) NOT NULL,
    Diagonal VARCHAR(150) NOT NULL,
    PRIMARY KEY (idLectura),
    FOREIGN KEY (idSesion) REFERENCES Sesiones(idSesion)
);
