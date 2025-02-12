-- =========================
-- CREACIÓN DE TABLAS
-- =========================

-- 4️⃣ Tabla de Permisos (definiendo permisos básicos)
CREATE TABLE permissions (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL -- 'read', 'write', 'delete', 'admin'
);


-- 1️⃣ Tabla de Usuarios (con contraseñas hasheadas)
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    hashed_password TEXT NOT NULL,
    mail TEXT NOT NULL,
    birthday TEXT NULL,
    default_role INTEGER NULL REFERENCES permissions(id) ON DELETE SET NULL DEFERRABLE INITIALLY DEFERRED
);


-- 2️⃣ Tabla de Carpetas (con soporte para jerarquía)
CREATE TABLE folders (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    parent_id INT REFERENCES folders(id) ON DELETE CASCADE,
    CONSTRAINT unique_folder_name_per_level UNIQUE (name, parent_id) -- Garantiza que no haya carpetas duplicadas en el mismo nivel
);

-- 3️⃣ Tabla de Archivos (cada archivo pertenece a una carpeta)
CREATE TABLE files (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    folder_id INT REFERENCES folders(id) ON DELETE CASCADE,
    CONSTRAINT unique_file_name_per_folder UNIQUE (name, folder_id) -- Garantiza que no haya archivos duplicados en la misma carpeta
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

-- 🔹 Insertar permisos (lectura, escritura y eliminación)
INSERT INTO permissions (name) VALUES 
    ('read'),
    ('write'),
    ('delete'),
    ('admin');

-- 🔹 Insertar usuarios
INSERT INTO users (username, hashed_password, mail, birthday, default_role) VALUES
    ('root', '$2a$12$KtuGa2uRanipD.mlCAIRqORc7QQhX6WK6WYvSLlUDFBDx/DGGpMYO', 'root@mail.com', '1970-01-01', 4),
    ('reader_user', '$2a$12$QiRkXYbTX1gi4W/b80V8ZuOgIvEpjSJoT1kGk4w1OE1i2zeQPa.7K', 'reader@mail.com', '1995-03-21', 1),
    ('writer_user', '$2a$12$QiRkXYbTX1gi4W/b80V8ZuOgIvEpjSJoT1kGk4w1OE1i2zeQPa.7K', 'writer@mail.com', '1992-07-10', 2);


-- 🔹 Insertar carpetas con jerarquía
INSERT INTO folders (name, parent_id) VALUES 
    ('Departamento A', NULL),
    ('Proyecto X', 1),
    ('Documentos', 2),
    ('Proyecto Y', 1);

-- 🔹 Insertar archivos en carpetas
INSERT INTO files (name, folder_id) VALUES 
    ('archivo1.txt', 3),
    ('archivo2.txt', 3),
    ('archivo3.txt', 4);

-- 🔹 Asignar permisos a usuarios en carpetas
INSERT INTO folder_acl (folder_id, user_id, permission_id, inherit) VALUES 
    (1, 1, 1, FALSE),
    (2, 1, 1, TRUE),
    (3, 2, 2, FALSE),
    (4, 3, 1, FALSE);

-- 🔹 Asignar permisos específicos a archivos
INSERT INTO file_acl (file_id, user_id, permission_id) VALUES 
    (1, 2, 1),
    (2, 2, 2),
    (3, 3, 1);

