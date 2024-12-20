import matplotlib.pyplot as plt

# Parámetros del sistema
input = 2.4  # Voltaje asociado al valor nominal de temperatura deseado a percibir de 24 °C
tiempo_total = 200  # Número de intervalos de tiempo para la simulación
t_ambiente_inicial = 28  # Temperatura ambiente inicial

# Definición de los niveles de velocidad y sus efectos sobre la temperatura percibida
def ventilador(nivel_de_velocidad):
    # Distribución lineal de velocidades y su efecto
    velocidades = {0: 0.0, 1: 0.4, 3: 1.3, 5: 2.6, 7: 5.2, 8: 6.3}
    k = 5 / 6.3  # Coeficiente de proporcionalidad (reducción máxima de 5°C a 6.3 m/s)
    
    V = velocidades.get(nivel_de_velocidad, 0)  # Velocidad del aire (m/s)
    reduccion = k * V  # Reducción lineal de temperatura
    return reduccion


def controlador(error):
    if error > 0.1:
        return 0
    elif error >= -0.1 and error <= 0.1:
        return 1
    elif -0.2 <= error < -0.1:
        return 3
    elif -0.3 <= error < -0.2:
        return 5
    elif -0.5 <= error < -0.3:
        return 7
    elif error < -0.5:
        return 8

def termohigrometro(temp):
    return (temp * 5) / 50  # Simula salida de voltaje entre 0 a 5V relacionados a la temperatura mínima (0°C) y máxima (50°C) que es capaz de medir 


# Simulación
ambient_temp = t_ambiente_inicial
T_ambient = []
T_perceived = []
nivel_de_velocidades = []
t_abrir = 50     # Tiempo en el que se abre la ventana
t_cerrar = 80   # Tiempo en el que se cierra la ventana
rate = 0.1      # Tasa de cambio de temperatura (gradual)

for t in range(tiempo_total):

    # Simula apertura y cierre de ventana con cambio gradual
    if t_abrir <= t < t_cerrar:  # Ventana abierta, temperatura disminuye
            ambient_temp -= rate  # Reducir temperatura gradualmente
    elif t >= (t_cerrar + 20):  # Ventana cerrada, temperatura aumenta gradualmente
        if ambient_temp < t_ambiente_inicial:
            ambient_temp += rate * 0.5  # Aumentar temperatura gradualmente

    # Realimentación del termohigrómetro
    realimentacion = termohigrometro(ambient_temp)
    
    # Cálculo del error 
    error = round(input - realimentacion, 4)  # Redondea en 4 decimales
    
    # Controlador proporcional
    nivel_de_velocidad = controlador(error)
    
    # Corrección de la temperatura percibida por medio del ventilador (Actuador)
    reduccion = ventilador(nivel_de_velocidad)
    temp_percibida = ambient_temp - reduccion
    

    # Almacenar datos para los gráficos
    T_ambient.append(ambient_temp)
    T_perceived.append(temp_percibida)
    nivel_de_velocidades.append(nivel_de_velocidad)



# GRAFICOS

# Cálculo de los umbrales de error en el rango de tolerancia 
errores_tolerancia = [-0.1, 0.1]  # Rango de tolerancia en el controlador
umbrales_temp_tolerancia = [(input - e) * 50 / 5 for e in errores_tolerancia]  # Conversión a temperatura


# --- Figura 1: Gráfico de Temperaturas ---
plt.figure(figsize=(10, 6)) 

plt.plot(T_ambient, label='Temperatura Ambiente (°C)')
plt.plot(T_perceived, label='Temperatura Percibida (°C)', linestyle='--')
plt.axhline(input * 10, color='r', linestyle=':', label='Temperatura Deseada (24°C)')

# Agrega los umbrales del rango de tolerancia 
colores_umbrales = ['orange', 'purple']
for i, umbral in enumerate(umbrales_temp_tolerancia):
    plt.axhline(umbral, color=colores_umbrales[i], linestyle='--', 
                label=f'Umbral de Tolerancia ({umbrales_temp_tolerancia[i]:.2f}°C)')

plt.title('Temperaturas Ambiente y Percibida')
plt.xlabel('Tiempo')
plt.ylabel('Temperatura (°C)')
plt.legend()
plt.grid(True)  # Agrega cuadrícula para mejor visualización
plt.show()

# --- Figura 2: Gráfico de Niveles de Velocidad ---
plt.figure(figsize=(10, 6))  

plt.plot(nivel_de_velocidades, label='Nivel de Velocidad', color='g')
plt.title('Niveles de Velocidad del Ventilador')
plt.xlabel('Tiempo')
plt.ylabel('Nivel de Velocidad')
plt.yticks([0, 1, 3, 5, 7, 8], ['Apagado', 'Nivel 1', 'Nivel 3', 'Nivel 5', 'Nivel 7', 'Nivel 8'])
plt.legend()
plt.grid(True)  # Agrega cuadrícula
plt.show()





