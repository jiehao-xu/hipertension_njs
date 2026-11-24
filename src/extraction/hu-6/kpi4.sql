CREATE VIEW kpi4 AS
SELECT
    `record_id`,
    `Precio venta al público con IVA` - `Precio de referencia` AS diferencia_precio
FROM medicamentos_hu5;
