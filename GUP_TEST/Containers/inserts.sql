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
