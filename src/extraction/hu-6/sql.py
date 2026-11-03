from pathlib import Path
import os

import mysql.connector
import pandas as pd
from dotenv import load_dotenv
import numpy as np


SCRIPT_DIR = Path(__file__).resolve().parent
CSV_PATH = SCRIPT_DIR.parents[2] / "data" / "raw" / "medicamentosHU5.csv"

create_sql = """
CREATE TABLE IF NOT EXISTS medicamentos_hu5 (
    record_id BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `dosis` DOUBLE NULL,
    `estado_aut` SMALLINT NULL,
    `comercializado` BOOLEAN NULL,
    `requiere_receta` BOOLEAN NULL,
    `generico` BOOLEAN NULL,
    `afecta_conduccion` BOOLEAN NULL,
    `triangulo_negro` BOOLEAN NULL,
    `medicamento_huerfano` BOOLEAN NULL,
    `biosimilar` BOOLEAN NULL,
    `num_principios_activos` INT NULL,
    `num_excipientes` INT NULL,
    `num_palabras4.4` INT NULL,
    `num_tablas` INT NULL,
    `indicador_riesgo_grave` INT NULL,
    `Precio venta al público con IVA` DECIMAL(10, 2) NULL,
    `Tratamiento de larga duración` BOOLEAN NULL,
    `forma_farmaceutica_simplificada_CAPSULA LIBERACION MODIFICADA` BOOLEAN NULL,
    `forma_farmaceutica_simplificada_COLIRIO` BOOLEAN NULL,
    `forma_farmaceutica_simplificada_COLIRIO DE LIBERACION PROLONGADA` BOOLEAN NULL,
    `forma_farmaceutica_simplificada_COMPRIMIDO` BOOLEAN NULL,
    `forma_farmaceutica_simplificada_COMPRIMIDO LIBERACION MODIFICADA` BOOLEAN NULL,
    `vias_administracion_['VÍA ORAL']` BOOLEAN NULL,
    `Estado_BAJA GENERAL` BOOLEAN NULL,
    `Estado_BAJA POR NO COMERCIALIZAR` BOOLEAN NULL,
    `pactivo_QUINAPRIL` BOOLEAN NULL,
    `pactivo_QUINAPRIL HIDROCLORURO` BOOLEAN NULL,
    `pactivo_ESPIRONOLACTONA` BOOLEAN NULL,
    `pactivo_AMLODIPINO BESILATO` BOOLEAN NULL,
    `pactivo_VALSARTAN` BOOLEAN NULL,
    `pactivo_MANIDIPINO HIDROCLORURO` BOOLEAN NULL,
    `pactivo_CARTEOLOL HIDROCLORURO` BOOLEAN NULL,
    `pactivo_OLMESARTAN MEDOXOMILO` BOOLEAN NULL,
    `pactivo_HIDROCLOROTIAZIDA` BOOLEAN NULL,
    `pactivo_BARNIDIPINO HIDROCLORURO` BOOLEAN NULL,
    `pactivo_BISOPROLOL FUMARATO` BOOLEAN NULL,
    `pactivo_ATENOLOL` BOOLEAN NULL,
    `pactivo_BOSENTAN MONOHIDRATO` BOOLEAN NULL,
    `pactivo_BRIMONIDINA TARTRATO` BOOLEAN NULL,
    `pactivo_CANDESARTAN CILEXETILO` BOOLEAN NULL,
    `pactivo_CAPTOPRIL` BOOLEAN NULL,
    `pactivo_DOXAZOSINA MESILATO` BOOLEAN NULL,
    `pactivo_PERINDOPRIL` BOOLEAN NULL,
    `pactivo_DILTIAZEM HIDROCLORURO` BOOLEAN NULL,
    `pactivo_ENALAPRIL MALEATO` BOOLEAN NULL,
    `pactivo_NEBIVOLOL HIDROCLORURO` BOOLEAN NULL,
    `pactivo_IRBESARTAN` BOOLEAN NULL,
    `pactivo_LATANOPROST` BOOLEAN NULL,
    `pactivo_TIMOLOL MALEATO` BOOLEAN NULL,
    `pactivo_LERCANIDIPINO HIDROCLORURO` BOOLEAN NULL,
    `pactivo_LISINOPRIL DIHIDRATO` BOOLEAN NULL,
    `pactivo_LOSARTAN POTASICO` BOOLEAN NULL,
    `pactivo_MANIDIPINO DIHIDROCLORURO` BOOLEAN NULL,
    `pactivo_NIFEDIPINO` BOOLEAN NULL,
    `pactivo_PERINDOPRIL ERBUMINA` BOOLEAN NULL,
    `pactivo_INDAPAMIDA` BOOLEAN NULL,
    `pactivo_LISINOPRIL` BOOLEAN NULL,
    `pactivo_RAMIPRIL` BOOLEAN NULL,
    `pactivo_TAFLUPROST` BOOLEAN NULL,
    `pactivo_TIMOLOL` BOOLEAN NULL,
    `pactivo_TELMISARTAN` BOOLEAN NULL,
    `pactivo_TORASEMIDA` BOOLEAN NULL,
    `pactivo_DORZOLAMIDA HIDROCLORURO` BOOLEAN NULL,
    `pactivo_NICARDIPINO HIDROCLORURO` BOOLEAN NULL,
    `pactivo_PERINDOPRIL  ARGININA` BOOLEAN NULL,
    `pactivo_DELAPRIL HIDROCLORURO` BOOLEAN NULL,
    `labtitular_Laboratorio Stada S.L.` BOOLEAN NULL,
    `labtitular_Laboratorios Cinfa S.A.` BOOLEAN NULL,
    `labtitular_Laboratorios Normon S.A.` BOOLEAN NULL,
    `labtitular_Menarini International Operations Luxembourg S.A.` BOOLEAN NULL,
    `labtitular_Novartis Farmaceutica S.A.` BOOLEAN NULL,
    `labtitular_Sandoz Farmaceutica S.A.` BOOLEAN NULL,
    `labtitular_Tecnimede España Industria Farmaceutica S.A.` BOOLEAN NULL,
    `labtitular_infrequent_sklearn` BOOLEAN NULL,
    `n_cluster` INT NULL,
    `cluster` VARCHAR(255) NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
"""


insert_sql = """
INSERT INTO medicamentos_hu5
    (`dosis`,
    `estado_aut`,
    `comercializado`,
    `requiere_receta`,
    `generico`,
    `afecta_conduccion`,
    `triangulo_negro`,
    `medicamento_huerfano`,
    `biosimilar`,
    `num_principios_activos`,
    `num_excipientes`,
    `num_palabras4.4`,
    `num_tablas`,
    `indicador_riesgo_grave`,
    `Precio venta al público con IVA`,
    `Tratamiento de larga duración`,
    `forma_farmaceutica_simplificada_CAPSULA LIBERACION MODIFICADA`,
    `forma_farmaceutica_simplificada_COLIRIO`,
    `forma_farmaceutica_simplificada_COLIRIO DE LIBERACION PROLONGADA`,
    `forma_farmaceutica_simplificada_COMPRIMIDO`,
    `forma_farmaceutica_simplificada_COMPRIMIDO LIBERACION MODIFICADA`,
    `vias_administracion_['VÍA ORAL']`,
    `Estado_BAJA GENERAL`,
    `Estado_BAJA POR NO COMERCIALIZAR`,
    `pactivo_QUINAPRIL`,
    `pactivo_QUINAPRIL HIDROCLORURO`,
    `pactivo_ESPIRONOLACTONA`,
    `pactivo_AMLODIPINO BESILATO`,
    `pactivo_VALSARTAN`,
    `pactivo_MANIDIPINO HIDROCLORURO`,
    `pactivo_CARTEOLOL HIDROCLORURO`,
    `pactivo_OLMESARTAN MEDOXOMILO`,
    `pactivo_HIDROCLOROTIAZIDA`,
    `pactivo_BARNIDIPINO HIDROCLORURO`,
    `pactivo_BISOPROLOL FUMARATO`,
    `pactivo_ATENOLOL`,
    `pactivo_BOSENTAN MONOHIDRATO`,
    `pactivo_BRIMONIDINA TARTRATO`,
    `pactivo_CANDESARTAN CILEXETILO`,
    `pactivo_CAPTOPRIL`,
    `pactivo_DOXAZOSINA MESILATO`,
    `pactivo_PERINDOPRIL`,
    `pactivo_DILTIAZEM HIDROCLORURO`,
    `pactivo_ENALAPRIL MALEATO`,
    `pactivo_NEBIVOLOL HIDROCLORURO`,
    `pactivo_IRBESARTAN`,
    `pactivo_LATANOPROST`,
    `pactivo_TIMOLOL MALEATO`,
    `pactivo_LERCANIDIPINO HIDROCLORURO`,
    `pactivo_LISINOPRIL DIHIDRATO`,
    `pactivo_LOSARTAN POTASICO`,
    `pactivo_MANIDIPINO DIHIDROCLORURO`,
    `pactivo_NIFEDIPINO`,
    `pactivo_PERINDOPRIL ERBUMINA`,
    `pactivo_INDAPAMIDA`,
    `pactivo_LISINOPRIL`,
    `pactivo_RAMIPRIL`,
    `pactivo_TAFLUPROST`,
    `pactivo_TIMOLOL`,
    `pactivo_TELMISARTAN`,
    `pactivo_TORASEMIDA`,
    `pactivo_DORZOLAMIDA HIDROCLORURO`,
    `pactivo_NICARDIPINO HIDROCLORURO`,
    `pactivo_PERINDOPRIL  ARGININA`,
    `pactivo_DELAPRIL HIDROCLORURO`,
    `labtitular_Laboratorio Stada S.L.`,
    `labtitular_Laboratorios Cinfa S.A.`,
    `labtitular_Laboratorios Normon S.A.`,
    `labtitular_Menarini International Operations Luxembourg S.A.`,
    `labtitular_Novartis Farmaceutica S.A.`,
    `labtitular_Sandoz Farmaceutica S.A.`,
    `labtitular_Tecnimede España Industria Farmaceutica S.A.`,
    `labtitular_infrequent_sklearn`,
    `n_cluster`,
    `cluster`)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""


def to_mysql_value(value):
    if pd.isna(value):
        return None
    if isinstance(value, (bool, np.bool_)):
        return int(value)
    if isinstance(value, np.generic):
        return value.item()
    return value


def main():
    load_dotenv(SCRIPT_DIR / ".env")
    config = {
        "host": os.getenv("DB_HOST", "localhost"),
        "port": int(os.getenv("DB_PORT", "3306")),
        "user": os.getenv("DB_USER"),
        "password": os.getenv("DB_PASSWORD"),
        "database": os.getenv("DB_NAME"),
        "use_pure": True,
        "charset": "utf8mb4",
        "connection_timeout": 10,
        "autocommit": False,
    }

    df = pd.read_csv(CSV_PATH)
   

    rows = []
    for row in df.itertuples(index=False, name=None):
        fila = []
        for value in row:
            fila.append(to_mysql_value(value))
        rows.append(tuple(fila))

    conn = None
    cursor = None

    try:
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()
        cursor.execute("DROP TABLE IF EXISTS medicamentos_hu5")  
        cursor.execute(create_sql)
        cursor.executemany(insert_sql, rows)
        inserted = cursor.rowcount
        if inserted != len(df):
            raise ValueError(f"Filas insertadas: {inserted}; esperadas: {len(df)}")
        conn.commit()
        print(f"Tabla medicamentos_hu5 preparada. Filas insertadas: {inserted}")
    except Exception:
        if conn is not None and conn.is_connected():
            conn.rollback()
        raise
    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None and conn.is_connected():
            conn.close()


if __name__ == "__main__":
    main()
