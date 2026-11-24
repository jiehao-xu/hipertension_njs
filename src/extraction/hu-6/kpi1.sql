CREATE VIEW kpi1 AS SELECT `record_id`, ((`Precio venta al público con IVA` - `Precio de referencia`)/(`Precio de referencia`))*100 AS porcentaje_diferencia_precio  FROM medicamentos_hu5;
