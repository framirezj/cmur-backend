-- Insertar 100 anexos de ejemplo
INSERT INTO
    anexos (
        id,
        anexo,
        ubicacion,
        unidad_servicio,
        funcionarios,
        creado_por_id,
        actualizado_por_id
    )
VALUES
    (
        1,
        101,
        'Segundo Piso, Ala Norte',
        'SECTOR ROJO',
        'Sra. Jefa (Directora)',
        NULL,
        NULL
    ),
    (
        2,
        102,
        'Primer Piso, Pasillo Central',
        'SECTOR VERDE',
        'E.U. Pérez y E.U. Gómez',
        NULL,
        NULL
    ),
    (
        3,
        201,
        'Módulo 3',
        'SECTOR AZUL',
        'Dr. Rojas / Enfermera María',
        NULL,
        NULL
    ),
    (
        4,
        301,
        'Edificio Anexo',
        'SECTOR AMARILLO',
        'Téc. Dentista López',
        NULL,
        NULL
    ),
    (
        5,
        302,
        'Sala multiuso',
        'SECTOR TRANSVERSAL',
        'Administrativos',
        NULL,
        NULL
    ),
    (
        6,
        303,
        'Tercer Piso, Oficina 3B',
        'SECTOR ROJO',
        'Lic. Martínez',
        NULL,
        NULL
    ),
    (
        7,
        401,
        'Planta Baja, Recepción',
        'SECTOR VERDE',
        'Sra. García y Sr. Rodríguez',
        NULL,
        NULL
    ),
    (
        8,
        402,
        'Segundo Piso, Ala Sur',
        'SECTOR AZUL',
        'Dr. Sánchez',
        NULL,
        NULL
    ),
    (
        9,
        403,
        'Módulo 7',
        'SECTOR AMARILLO',
        'E.U. Torres',
        NULL,
        NULL
    ),
    (
        10,
        501,
        'Edificio Principal, Piso 4',
        'SECTOR TRANSVERSAL',
        'Equipo de gestión',
        NULL,
        NULL
    ),
    (
        11,
        502,
        'Primer Piso, Consultorio 5',
        'SECTOR ROJO',
        'Dra. Ramírez',
        NULL,
        NULL
    ),
    (
        12,
        503,
        'Sótano, Archivo',
        'SECTOR VERDE',
        'Personal administrativo',
        NULL,
        NULL
    ),
    (
        13,
        601,
        'Tercer Piso, Ala Este',
        'SECTOR AZUL',
        'Dr. González y E.U. Díaz',
        NULL,
        NULL
    ),
    (
        14,
        602,
        'Módulo 12',
        'SECTOR AMARILLO',
        'Téc. Fernández',
        NULL,
        NULL
    ),
    (
        15,
        603,
        'Planta Baja, Sala de Espera',
        'SECTOR TRANSVERSAL',
        'Sra. Rodríguez',
        NULL,
        NULL
    ),
    (
        16,
        701,
        'Segundo Piso, Consultorio 7',
        'SECTOR ROJO',
        'Dr. Morales',
        NULL,
        NULL
    ),
    (
        17,
        702,
        'Edificio Anexo, Piso 2',
        'SECTOR VERDE',
        'E.U. Castro y Lic. Ruiz',
        NULL,
        NULL
    ),
    (
        18,
        703,
        'Módulo 15',
        'SECTOR AZUL',
        'Dra. Flores',
        NULL,
        NULL
    ),
    (
        19,
        801,
        'Primer Piso, Ala Oeste',
        'SECTOR AMARILLO',
        'Téc. Mendoza',
        NULL,
        NULL
    ),
    (
        20,
        802,
        'Tercer Piso, Oficina 8B',
        'SECTOR TRANSVERSAL',
        'Personal de apoyo',
        NULL,
        NULL
    ),
    (
        21,
        803,
        'Sótano, Bodega',
        'SECTOR ROJO',
        'Sr. Reyes',
        NULL,
        NULL
    ),
    (
        22,
        901,
        'Planta Baja, Consulta General',
        'SECTOR VERDE',
        'Dra. Ortega',
        NULL,
        NULL
    ),
    (
        23,
        902,
        'Segundo Piso, Ala Norte',
        'SECTOR AZUL',
        'E.U. Vargas y E.U. Silva',
        NULL,
        NULL
    ),
    (
        24,
        903,
        'Módulo 21',
        'SECTOR AMARILLO',
        'Dr. Castro',
        NULL,
        NULL
    ),
    (
        25,
        1001,
        'Edificio Principal, Piso 5',
        'SECTOR TRANSVERSAL',
        'Administrativos y asistentes',
        NULL,
        NULL
    ),
    (
        26,
        1002,
        'Primer Piso, Consultorio 10',
        'SECTOR ROJO',
        'Lic. Herrera',
        NULL,
        NULL
    ),
    (
        27,
        1003,
        'Tercer Piso, Ala Norte',
        'SECTOR VERDE',
        'Dra. Rivas',
        NULL,
        NULL
    ),
    (
        28,
        1101,
        'Módulo 25',
        'SECTOR AZUL',
        'E.U. Paredes',
        NULL,
        NULL
    ),
    (
        29,
        1102,
        'Planta Baja, Recepción Principal',
        'SECTOR AMARILLO',
        'Sra. Muñoz y Sr. Araya',
        NULL,
        NULL
    ),
    (
        30,
        1103,
        'Segundo Piso, Oficina 11C',
        'SECTOR TRANSVERSAL',
        'Téc. Soto',
        NULL,
        NULL
    ),
    (
        31,
        1201,
        'Edificio Anexo, Piso 3',
        'SECTOR ROJO',
        'Dr. Miranda',
        NULL,
        NULL
    ),
    (
        32,
        1202,
        'Primer Piso, Pasillo Sur',
        'SECTOR VERDE',
        'E.U. Gutiérrez',
        NULL,
        NULL
    ),
    (
        33,
        1203,
        'Sótano, Almacén',
        'SECTOR AZUL',
        'Personal de logística',
        NULL,
        NULL
    ),
    (
        34,
        1301,
        'Tercer Piso, Consultorio 13',
        'SECTOR AMARILLO',
        'Dra. Villalobos',
        NULL,
        NULL
    ),
    (
        35,
        1302,
        'Módulo 30',
        'SECTOR TRANSVERSAL',
        'Téc. Venegas',
        NULL,
        NULL
    ),
    (
        36,
        1303,
        'Planta Baja, Farmacia',
        'SECTOR ROJO',
        'E.U. Medina',
        NULL,
        NULL
    ),
    (
        37,
        1401,
        'Segundo Piso, Ala Oeste',
        'SECTOR VERDE',
        'Dr. Navarrete y Dra. Bravo',
        NULL,
        NULL
    ),
    (
        38,
        1402,
        'Edificio Principal, Piso 2',
        'SECTOR AZUL',
        'Lic. Reyes',
        NULL,
        NULL
    ),
    (
        39,
        1403,
        'Primer Piso, Consultorio 14',
        'SECTOR AMARILLO',
        'Personal de enfermería',
        NULL,
        NULL
    ),
    (
        40,
        1501,
        'Módulo 35',
        'SECTOR TRANSVERSAL',
        'Sr. Fuentes',
        NULL,
        NULL
    ),
    (
        41,
        1502,
        'Tercer Piso, Sala de Reuniones',
        'SECTOR ROJO',
        'Dra. Mendoza',
        NULL,
        NULL
    ),
    (
        42,
        1503,
        'Planta Baja, Urgencias',
        'SECTOR VERDE',
        'E.U. Valenzuela',
        NULL,
        NULL
    ),
    (
        43,
        1601,
        'Segundo Piso, Oficina 16A',
        'SECTOR AZUL',
        'Dr. Calderón',
        NULL,
        NULL
    ),
    (
        44,
        1602,
        'Edificio Anexo, Piso 4',
        'SECTOR AMARILLO',
        'Téc. Figueroa',
        NULL,
        NULL
    ),
    (
        45,
        1603,
        'Primer Piso, Pasillo Este',
        'SECTOR TRANSVERSAL',
        'Sra. Escobar',
        NULL,
        NULL
    ),
    (
        46,
        1701,
        'Módulo 42',
        'SECTOR ROJO',
        'E.U. Parra',
        NULL,
        NULL
    ),
    (
        47,
        1702,
        'Sótano, Archivo General',
        'SECTOR VERDE',
        'Personal administrativo',
        NULL,
        NULL
    ),
    (
        48,
        1703,
        'Tercer Piso, Consultorio 17',
        'SECTOR AZUL',
        'Dr. Herrera y Dra. Soto',
        NULL,
        NULL
    ),
    (
        49,
        1801,
        'Planta Baja, Laboratorio',
        'SECTOR AMARILLO',
        'Téc. Lagos',
        NULL,
        NULL
    ),
    (
        50,
        1802,
        'Segundo Piso, Ala Este',
        'SECTOR TRANSVERSAL',
        'Lic. Sanhueza',
        NULL,
        NULL
    ),
    (
        51,
        1803,
        'Edificio Principal, Piso 3',
        'SECTOR ROJO',
        'E.U. Quintana',
        NULL,
        NULL
    ),
    (
        52,
        1901,
        'Primer Piso, Consultorio 19',
        'SECTOR VERDE',
        'Dra. Fierro',
        NULL,
        NULL
    ),
    (
        53,
        1902,
        'Módulo 48',
        'SECTOR AZUL',
        'Dr. Olivares',
        NULL,
        NULL
    ),
    (
        54,
        1903,
        'Tercer Piso, Oficina 19C',
        'SECTOR AMARILLO',
        'Téc. Garrido',
        NULL,
        NULL
    ),
    (
        55,
        2001,
        'Planta Baja, Sala de Espera',
        'SECTOR TRANSVERSAL',
        'Sra. Vidal y Sr. Cáceres',
        NULL,
        NULL
    ),
    (
        56,
        2002,
        'Segundo Piso, Consultorio 20',
        'SECTOR ROJO',
        'E.U. Henríquez',
        NULL,
        NULL
    ),
    (
        57,
        2003,
        'Edificio Anexo, Piso 5',
        'SECTOR VERDE',
        'Dra. Acuña',
        NULL,
        NULL
    ),
    (
        58,
        2101,
        'Módulo 52',
        'SECTOR AZUL',
        'Lic. Peña',
        NULL,
        NULL
    ),
    (
        59,
        2102,
        'Primer Piso, Pasillo Norte',
        'SECTOR AMARILLO',
        'Personal de mantención',
        NULL,
        NULL
    ),
    (
        60,
        2103,
        'Sótano, Bodega Insumos',
        'SECTOR TRANSVERSAL',
        'Sr. Espinoza',
        NULL,
        NULL
    ),
    (
        61,
        2201,
        'Tercer Piso, Sala Multiuso',
        'SECTOR ROJO',
        'Dr. Latorre',
        NULL,
        NULL
    ),
    (
        62,
        2202,
        'Planta Baja, Recepción 22',
        'SECTOR VERDE',
        'E.U. Tapia y Lic. Rojas',
        NULL,
        NULL
    ),
    (
        63,
        2203,
        'Segundo Piso, Ala Sur',
        'SECTOR AZUL',
        'Dra. Jara',
        NULL,
        NULL
    ),
    (
        64,
        2301,
        'Edificio Principal, Piso 6',
        'SECTOR AMARILLO',
        'Téc. Salazar',
        NULL,
        NULL
    ),
    (
        65,
        2302,
        'Módulo 58',
        'SECTOR TRANSVERSAL',
        'Sra. Núñez',
        NULL,
        NULL
    ),
    (
        66,
        2303,
        'Primer Piso, Consultorio 23',
        'SECTOR ROJO',
        'Dr. Riveros',
        NULL,
        NULL
    ),
    (
        67,
        2401,
        'Tercer Piso, Ala Oeste',
        'SECTOR VERDE',
        'E.U. Carvajal',
        NULL,
        NULL
    ),
    (
        68,
        2402,
        'Planta Baja, Farmacia Central',
        'SECTOR AZUL',
        'Lic. Delgado',
        NULL,
        NULL
    ),
    (
        69,
        2403,
        'Segundo Piso, Oficina 24B',
        'SECTOR AMARILLO',
        'Dra. Soto',
        NULL,
        NULL
    ),
    (
        70,
        2501,
        'Edificio Anexo, Piso 6',
        'SECTOR TRANSVERSAL',
        'Téc. Araneda',
        NULL,
        NULL
    ),
    (
        71,
        2502,
        'Módulo 63',
        'SECTOR ROJO',
        'Dr. Pino',
        NULL,
        NULL
    ),
    (
        72,
        2503,
        'Primer Piso, Pasillo Central',
        'SECTOR VERDE',
        'E.U. Barrera',
        NULL,
        NULL
    ),
    (
        73,
        2601,
        'Sótano, Laboratorio 26',
        'SECTOR AZUL',
        'Personal de laboratorio',
        NULL,
        NULL
    ),
    (
        74,
        2602,
        'Tercer Piso, Consultorio 26',
        'SECTOR AMARILLO',
        'Dra. Guzmán',
        NULL,
        NULL
    ),
    (
        75,
        2603,
        'Planta Baja, Urgencias Adulto',
        'SECTOR TRANSVERSAL',
        'Dr. Neira y E.U. Campos',
        NULL,
        NULL
    ),
    (
        76,
        2701,
        'Segundo Piso, Ala Norte',
        'SECTOR ROJO',
        'Lic. Muñoz',
        NULL,
        NULL
    ),
    (
        77,
        2702,
        'Edificio Principal, Piso 1',
        'SECTOR VERDE',
        'Téc. Araya',
        NULL,
        NULL
    ),
    (
        78,
        2703,
        'Módulo 68',
        'SECTOR AZUL',
        'Sra. Villanueva',
        NULL,
        NULL
    ),
    (
        79,
        2801,
        'Primer Piso, Consultorio 28',
        'SECTOR AMARILLO',
        'Dr. Córdova',
        NULL,
        NULL
    ),
    (
        80,
        2802,
        'Tercer Piso, Sala de Capacitación',
        'SECTOR TRANSVERSAL',
        'E.U. Cifuentes',
        NULL,
        NULL
    ),
    (
        81,
        2803,
        'Planta Baja, Admisión',
        'SECTOR ROJO',
        'Lic. Rojas',
        NULL,
        NULL
    ),
    (
        82,
        2901,
        'Segundo Piso, Oficina 29A',
        'SECTOR VERDE',
        'Dra. Parada',
        NULL,
        NULL
    ),
    (
        83,
        2902,
        'Edificio Anexo, Piso 7',
        'SECTOR AZUL',
        'Téc. Abarca',
        NULL,
        NULL
    ),
    (
        84,
        2903,
        'Módulo 73',
        'SECTOR AMARILLO',
        'Sr. Segovia',
        NULL,
        NULL
    ),
    (
        85,
        3001,
        'Primer Piso, Pasillo Oeste',
        'SECTOR TRANSVERSAL',
        'E.U. Carrasco',
        NULL,
        NULL
    ),
    (
        86,
        3002,
        'Sótano, Archivo Mortal',
        'SECTOR ROJO',
        'Personal de archivo',
        NULL,
        NULL
    ),
    (
        87,
        3003,
        'Tercer Piso, Consultorio 30',
        'SECTOR VERDE',
        'Dr. Bustamante',
        NULL,
        NULL
    ),
    (
        88,
        3101,
        'Planta Baja, Sala de Procedimientos',
        'SECTOR AZUL',
        'Dra. Lagos y E.U. Marín',
        NULL,
        NULL
    ),
    (
        89,
        3102,
        'Segundo Piso, Ala Este',
        'SECTOR AMARILLO',
        'Téc. Pizarro',
        NULL,
        NULL
    ),
    (
        90,
        3103,
        'Edificio Principal, Piso 7',
        'SECTOR TRANSVERSAL',
        'Lic. Salinas',
        NULL,
        NULL
    ),
    (
        91,
        3201,
        'Módulo 78',
        'SECTOR ROJO',
        'Dr. Figueroa',
        NULL,
        NULL
    ),
    (
        92,
        3202,
        'Primer Piso, Consultorio 32',
        'SECTOR VERDE',
        'Sra. Contreras',
        NULL,
        NULL
    ),
    (
        93,
        3203,
        'Tercer Piso, Oficina 32C',
        'SECTOR AZUL',
        'E.U. Bahamondes',
        NULL,
        NULL
    ),
    (
        94,
        3301,
        'Planta Baja, Farmacia Urgencias',
        'SECTOR AMARILLO',
        'Lic. Leiva',
        NULL,
        NULL
    ),
    (
        95,
        3302,
        'Segundo Piso, Sala de Espera',
        'SECTOR TRANSVERSAL',
        'Dr. Altamirano',
        NULL,
        NULL
    ),
    (
        96,
        3303,
        'Edificio Anexo, Piso 8',
        'SECTOR ROJO',
        'Téc. Rivas',
        NULL,
        NULL
    ),
    (
        97,
        3401,
        'Módulo 82',
        'SECTOR VERDE',
        'Dra. Rivas',
        NULL,
        NULL
    ),
    (
        98,
        3402,
        'Primer Piso, Pasillo Sur',
        'SECTOR AZUL',
        'E.U. Orellana y Lic. Zamora',
        NULL,
        NULL
    ),
    (
        99,
        3403,
        'Sótano, Bodega 34',
        'SECTOR AMARILLO',
        'Sr. Cerda',
        NULL,
        NULL
    ),
    (
        100,
        3501,
        'Tercer Piso, Consultorio 35',
        'SECTOR TRANSVERSAL',
        'Dr. Villegas',
        NULL,
        NULL
    );