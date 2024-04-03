import numpy as np
import sqlite3
from tensorflow import keras
from tensorflow.keras import layers

# Conexión a la base de datos
conn = sqlite3.connect('animales.db')
cursor = conn.cursor()

# Consulta para obtener todos los registros de la tabla animales
cursor.execute('SELECT nombre, tipo FROM animales')
animales_registros = cursor.fetchall()

# Cerrar la conexión a la base de datos
conn.close()

# Convertir los registros en un diccionario
animales_dict = dict(animales_registros)

# Método de entrada para cambiar los valores
animal_1 = input("Ingrese el nombre del primer animal: ").lower()
animal_2 = input("Ingrese el nombre del segundo animal: ").lower()

if animal_1 in animales_dict:
    entrada = animales_dict[animal_1]
else:
    raise ValueError("Animal no reconocido.")

if animal_2 in animales_dict:
    entrada_2 = animales_dict[animal_2]
else:
    raise ValueError("Animal no reconocido.")

# Probabilidades a priori (hipotéticas) de que sea una gallina o un huevo
p_gallina = 0.5
p_huevo = 1 - p_gallina

# Crear una red neuronal simple
model = keras.Sequential([
    layers.Dense(64, activation='relu', input_shape=(1,)),
    layers.Dense(64, activation='relu'),
    layers.Dense(1, activation='sigmoid')
])

# Compilar el modelo
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Datos de entrenamiento (hipotéticos)
X_train = np.array([[0], [1], [0], [1]])  # Datos de entrada
y_train = np.array([[1], [0], [1], [0]])  # Resultados esperados (1 para huevo, 0 para gallina)

# Entrenar la red neuronal
model.fit(X_train, y_train, epochs=10)

# Implementar el teorema de Bayes después del entrenamiento
evidencia = entrada  # Valor correspondiente al primer animal
evidencia_2 = entrada_2  # Valor correspondiente al segundo animal

# Calcular las probabilidades utilizando la fórmula del teorema de Bayes directamente
prob_gallina_dado_evidencia = (model.predict(np.array([[evidencia]]))[0][0] * p_gallina) / \
                              ((model.predict(np.array([[evidencia]]))[0][0] * p_gallina) +
                               ((1 - model.predict(np.array([[evidencia]]))[0][0]) * p_huevo))

prob_gallina_dado_evidencia_2 = (model.predict(np.array([[evidencia_2]]))[0][0] * p_gallina) / \
                                ((model.predict(np.array([[evidencia_2]]))[0][0] * p_gallina) +
                                 ((1 - model.predict(np.array([[evidencia_2]]))[0][0]) * p_huevo))

prob_huevo_dado_evidencia = 1 - prob_gallina_dado_evidencia
prob_huevo_dado_evidencia_2 = 1 - prob_gallina_dado_evidencia_2

print(f'Probabilidad de que el {animal_1} haya venido primero: {prob_gallina_dado_evidencia}')
print(f'Probabilidad de que el {animal_2} haya venido primero: {prob_gallina_dado_evidencia_2}')
