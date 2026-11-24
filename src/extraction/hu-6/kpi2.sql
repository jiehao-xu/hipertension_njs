CREATE VIEW kpi2 AS
SELECT
    `record_id`,
    `num_palabras4.4` / `num_tablas` AS palabras_por_tabla
FROM medicamentos_hu5;
