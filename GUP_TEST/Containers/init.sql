-- =========================
-- CREACIÓN DE TABLAS
-- =========================

-- 1️⃣ Tabla de Usuarios
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL
);

-- 2️⃣ Tabla de Carpetas (con soporte para jerarquía)
CREATE TABLE folders (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    parent_id INT REFERENCES folders(id) ON DELETE CASCADE
);

-- 3️⃣ Tabla de Archivos (cada archivo pertenece a una carpeta)
CREATE TABLE files (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    folder_id INT REFERENCES folders(id) ON DELETE CASCADE
);

-- 4️⃣ Tabla de Permisos (definiendo permisos básicos)
CREATE TABLE permissions (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL -- 'read', 'write', 'delete'
);

-- 5️⃣ Tabla de ACL para Carpetas (herencia de permisos)
CREATE TABLE folder_acl (
    id SERIAL PRIMARY KEY,
    folder_id INT REFERENCES folders(id) ON DELETE CASCADE,
    user_id INT REFERENCES users(id) ON DELETE CASCADE,
    permission_id INT REFERENCES permissions(id) ON DELETE CASCADE,
    inherit BOOLEAN DEFAULT TRUE
);

-- 6️⃣ Tabla de ACL para Archivos (permite reglas específicas en archivos)
CREATE TABLE file_acl (
    id SERIAL PRIMARY KEY,
    file_id INT REFERENCES files(id) ON DELETE CASCADE,
    user_id INT REFERENCES users(id) ON DELETE CASCADE,
    permission_id INT REFERENCES permissions(id) ON DELETE CASCADE
);

-- =========================
-- INSERCIÓN DE DATOS DE PRUEBA
-- =========================

-- 🔹 Insertar usuarios
INSERT INTO users (username) VALUES 
    ('alice'),
    ('bob'),
    ('charlie');

-- 🔹 Insertar permisos (lectura, escritura y eliminación)
INSERT INTO permissions (name) VALUES 
    ('read'),
    ('write'),
    ('delete'),
    ('admin');

-- 🔹 Insertar carpetas con jerarquía
INSERT INTO folders (name, parent_id) VALUES 
    ('Departamento A', NULL), -- Carpeta raíz
    ('Proyecto X', 1),  -- Subcarpeta de Departamento A
    ('Documentos', 2),  -- Subcarpeta de Proyecto X
    ('Proyecto Y', 1);  -- Subcarpeta de Departamento A

-- 🔹 Insertar archivos en carpetas
INSERT INTO files (name, folder_id) VALUES 
    ('archivo1.txt', 3), -- En "Documentos"
    ('archivo2.txt', 3), -- En "Documentos"
    ('archivo3.txt', 4); -- En "Proyecto Y"

-- 🔹 Asignar permisos a usuarios en carpetas
INSERT INTO folder_acl (folder_id, user_id, permission_id, inherit) VALUES 
    (1, 1, 1, FALSE),  -- Alice tiene read en "Departamento A"
    (2, 1, 1, TRUE),   -- Alice hereda permisos en "Proyecto X"
    (3, 2, 2, FALSE),  -- Bob tiene write en "Documentos"
    (4, 3, 1, FALSE);  -- Charlie tiene read en "Proyecto Y"

-- 🔹 Asignar permisos específicos a archivos
INSERT INTO file_acl (file_id, user_id, permission_id) VALUES 
    (1, 2, 1),  -- Bob puede leer "archivo1.txt"
    (2, 2, 2),  -- Bob puede escribir en "archivo2.txt"
    (3, 3, 1);  -- Charlie puede leer "archivo3.txt"
