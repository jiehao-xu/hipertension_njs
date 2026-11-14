
import logging
import subprocess
import sys
import os
from datetime import date

DEFAULT_HU_FOLDER = "src/extraction"



# Configuración de la librería logging
LOG_FILE = "log/njs_hipertension_"
logging.basicConfig(filename=f"{LOG_FILE}{date.today()}.log", level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def ejecutar_proceso(script_name):
    logging.info(f"[*] Iniciando ejecución de: {script_name}")
    result = subprocess.run([sys.executable, script_name], capture_output=True, text=True)
    if result.returncode == 0:
        logging.info(f"[+] Éxito al ejecutar {script_name}")
    else:
        logging.error(f"[-] Error en {script_name}: {result.stderr}")
        raise Exception(f"Fallo crítico en {script_name}")

if __name__ == "__main__":
    scripts = [
        DEFAULT_HU_FOLDER+"/hu-1/rest_api.py", 
        DEFAULT_HU_FOLDER+"/hu-2/scrapping.py",
        DEFAULT_HU_FOLDER+"/hu-3/csv_extractor.py",
        DEFAULT_HU_FOLDER+"/hu-4/clean.py",
        DEFAULT_HU_FOLDER+"/hu-5/predict.py",
        DEFAULT_HU_FOLDER+"/hu-6/sql.py"
    ]
    for script in scripts:
        try:
            ejecutar_proceso(script)
        except Exception as e:
            logging.critical("Flujo interrumpido.")
            sys.exit(1)