import sqlite3

# Conectar a la base de datos (esto creará el archivo si no existe)
conn = sqlite3.connect('animales.db')

# Crear un objeto cursor para interactuar con la base de datos
cursor = conn.cursor()

# Crear la tabla animales si no existe
cursor.execute('''
CREATE TABLE IF NOT EXISTS animales (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    tipo INTEGER NOT NULL
)
''')

# Diccionario de animales para insertar en la base de datos
animal_dict = {
    'gallina': 0, 
    'huevo': 1, 
    'elefante': 2, 
    'leon': 3, 
    'tigre': 4, 
    'jirafa': 5
}

# Preparar los datos para inserción, convertidos en una lista de tuplas
datos_a_insertar = [(nombre, tipo) for nombre, tipo in animal_dict.items()]

# Insertar datos en la tabla animales
# Usamos IGNORE para evitar insertar duplicados en caso de que el script se ejecute múltiples veces
cursor.executemany('''
INSERT OR IGNORE INTO animales (nombre, tipo) VALUES (?,?)
''', datos_a_insertar)

# Guardar (commit) los cambios
conn.commit()

# Seleccionar y mostrar todos los registros de la tabla animales
cursor.execute('SELECT * FROM animales')
rows = cursor.fetchall()

for row in rows:
    print(row)

# Cerrar la conexión a la base de datos
conn.close()
