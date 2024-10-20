import pandas as pd
import mysql.connector
from mysql.connector import Error
import numpy as np

# Función para limpiar valores NaN y convertir strings numéricos
def clean_value(val):
    if pd.isna(val):  # Reemplazar NaN con None
        return None
    if isinstance(val, str) and 'USD' in val:  # Quitar 'USD' y convertir a número
        return float(val.replace(' USD', '').replace(',', ''))
    return val

# Cargar el archivo Excel
excel_file = r"Z:\Hotel_Ecomusic\Hotel Ecomusic\Booking Reservas\Septiembre.xls"  # Cambia el nombre del archivo si es diferente
df = pd.read_excel(excel_file)

# Conectar a la base de datos MySQL
try:
    connection = mysql.connector.connect(
        host='localhost',        # Cambia por el host de tu servidor MySQL
        database='hotel_ecomusic',  # Cambia por el nombre de tu base de datos
        user='root',       # Cambia por tu usuario MySQL
        password='123',  # Cambia por tu contraseña MySQL
        port='3306'
    )

    if connection.is_connected():
        cursor = connection.cursor()

        # Recorrer el DataFrame del Excel
        for index, row in df.iterrows():
            # Limpiar los valores antes de insertarlos
            values = tuple(clean_value(row[col]) for col in [
                'Número de reserva',
                'Reservado por', 
                'Nombre del cliente (o clientes)', 
                'Entrada',
                'Salida',
                "Fecha de reserva", "Estado", "Habitaciones", "Personas", "Adultos", "Niños", "Edades de los niños:",
                "Precio", "Comisión %", "Importe de la comisión", "Estado del pago", "Forma de pago", "Comentarios", "Grupo de reserva", "Booker country",
                "Motivo del viaje", "Dispositivo", "Tipo de unidad", "Duración (noches)", "Fecha de cancelación", "Dirección", "Número de teléfono"
            ])

            numero_reserva = clean_value(row['Número de reserva'])  # Obtener el número de reserva

            # Verificar si el número de reserva ya existe
            check_query = "SELECT COUNT(*) FROM booking_reservas WHERE numero_reserva = %s"
            cursor.execute(check_query, (numero_reserva,))
            exists = cursor.fetchone()[0]  # Obtener el conteo

            if exists > 0:
                print(f"El registro con número de reserva {numero_reserva} ya existe. Omitiendo inserción.")
            else:
                # Preparar la consulta de inserción
                query = """
                INSERT INTO booking_reservas (
                    numero_reserva, reservado_por, nombre_cliente, entrada, salida,
                    fecha_reserva, estado, habitaciones, personas, adultos, 
                    ninos, edades_ninos,
                    precio, comision_porcentaje, importe_comision, estado_pago, forma_pago, comentarios, grupo_reserva, booker_country,
                    motivo_viaje, dispositivo, tipo_unidad, duracion_noches, fecha_cancelacion, direccion, telefono
                ) VALUES (
                    %s,     
                    %s, 
                    %s,
                    %s, 
                    %s,
                    %s,     
                    %s, 
                    %s,
                    %s, 
                    %s,
                    %s,
                    %s,
                    %s,     
                    %s, 
                    %s,
                    %s, 
                    %s,
                    %s,
                    %s,
                    %s,     
                    %s, 
                    %s,
                    %s, 
                    %s,
                    %s,
                    %s
                )
                """

                # Ejecutar la consulta de inserción
                cursor.execute(query, values)
                connection.commit()
                print(f"Registro insertado para número de reserva {numero_reserva}.")

        print("Los datos han sido procesados.")

except Error as e:
    print(f"Error al conectarse a MySQL: {e}")

finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("Conexión a MySQL cerrada.")
