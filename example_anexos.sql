INSERT INTO
    anexos (
        anexo,
        ubicacion,
        unidad_servicio,
        funcionarios,
        creado_por_id,
        actualizado_por_id
    )
SELECT
    generate_series(500, 599) AS anexo,
    'Sin asignar',
    'Sin asignar',
    'Sin asignar',
    NULL,
    NULL;