import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
DIR_INPUT = BASE_DIR / "data" / "input"

def investigar_activo():
    archivos = list(DIR_INPUT.glob("*.csv"))
    if not archivos:
        return
    
    df = pd.read_csv(archivos[0])
    # Ordenamos de antiguo a nuevo
    df['datetime'] = pd.to_datetime(df['datetime'])
    df = df.sort_values('datetime')

    # Preguntamos qué activo investigar
    nombre_activo = input("🔍 Escribe el nombre del activo fantasma (o parte de él): ")
    
    # Filtramos ignorando mayúsculas y minúsculas
    filtro = df[df['name'].str.contains(nombre_activo, case=False, na=False)]
    
    if filtro.empty:
        print("❌ No se ha encontrado ningún activo con ese nombre. ¡Revisa cómo está escrito en la tabla!")
        return
        
    print(f"\n--- HISTORIAL FORENSE DE: {nombre_activo.upper()} ---")
    
    # Mostramos solo las columnas clave para entender qué pasó
    columnas_ver = ['datetime', 'type', 'name', 'shares', 'price', 'amount']
    pd.set_option('display.max_rows', None)
    pd.set_option('display.width', 1000)
    
    print(filtro[columnas_ver].to_string(index=False))

if __name__ == "__main__":
    investigar_activo()