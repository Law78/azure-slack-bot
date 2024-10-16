import subprocess
import os
from dotenv import load_dotenv

load_dotenv()

try:
    print("Esecuzione Operazione di Delete...")
    subprocess.run([os.getenv('python_path'), os.getenv('delete_path')])
    print("Esecuzione di DELETE completata.")
except Exception as e:
    print(f"Errore durante l'esecuzione di DELETE: {e}")

try:
    print("Esecuzione Operazione di Add...")
    subprocess.run([os.getenv('python_path'), os.getenv('add_path')])
    print("Esecuzione di ADD completata.")
except Exception as e:
    print(f"Errore durante l'esecuzione di ADD: {e}")