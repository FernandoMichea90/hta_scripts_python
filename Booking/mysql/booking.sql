CREATE TABLE booking_reservas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    numero_reserva VARCHAR(20) NOT NULL,
    reservado_por VARCHAR(255) ,
    nombre_cliente VARCHAR(255),
    entrada DATE,
    salida DATE,
    fecha_reserva DATETIME,
    estado VARCHAR(50) ,
    habitaciones INT ,
    personas INT,
    adultos INT,
    ninos INT,
    edades_ninos VARCHAR(255),
    precio DECIMAL(10, 2),
    comision_porcentaje DECIMAL(5, 2),
    importe_comision DECIMAL(10, 2),
    estado_pago VARCHAR(50),
    forma_pago VARCHAR(50),
    comentarios TEXT,
    grupo_reserva VARCHAR(255),
    booker_country VARCHAR(2),
    motivo_viaje VARCHAR(50),
    dispositivo VARCHAR(50),
    tipo_unidad VARCHAR(250),
    duracion_noches INT,
    fecha_cancelacion DATE,
    direccion TEXT,
    telefono VARCHAR(20)
);

DROP table  booking_reservas ;

describe booking_reservas ;

ALTER table booking_reservas  add column nacionalidad VARCHAR(250);

UPDATE booking_reservas 
set nacionalidad = CASE 
when booker_country ='cl' then 'Nacional' else 'Extranjero'
END

