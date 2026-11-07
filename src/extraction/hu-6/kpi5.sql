CREATE VIEW kpi5 AS
SELECT
    `record_id`,
    `forma_farmaceutica_simplificada`,
    `Precio venta al público con IVA`,
    `Precio de referencia`,
    ROW_NUMBER() OVER (
        PARTITION BY `forma_farmaceutica_simplificada`
        ORDER BY `Precio venta al público con IVA` DESC
    ) AS ranking_precio_grupo
FROM medicamentos_hu5;