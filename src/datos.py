import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
DIR_INPUT = BASE_DIR / "data" / "input"

def cargar_datos():
    """Busca el CSV, lo carga, limpia y ordena cronológicamente."""
    archivos_csv = list(DIR_INPUT.glob("*.csv"))
    if not archivos_csv:
        return None, None
    
    archivo = archivos_csv[0]
    df = pd.read_csv(archivo)
    
    for col in ['amount', 'fee', 'tax', 'shares', 'price']:
        if col in df.columns:
            df[col] = df[col].fillna(0.0)
            
    df['datetime'] = pd.to_datetime(df['datetime'])
    df = df.sort_values('datetime', ascending=True).reset_index(drop=True)
    
    return df, archivo.name