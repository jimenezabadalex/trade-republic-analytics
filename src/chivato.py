import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
archivos_csv = list((BASE_DIR / "data" / "input").glob("*.csv"))

if archivos_csv:
    df = pd.read_csv(archivos_csv[0])
    
    # Esta es la lista de todo lo que nuestro programa ya controla
    eventos_controlados = [
        'BUY', 'SAVINGS_PLAN', 'SELL', 'SPLIT', 'REVERSE_SPLIT', 
        'REVERSE_STOCK_SPLIT', 'SPIN_OFF', 'MIGRATION', 'STOCKPERK', 
        'TRANSFER_INSTANT_INBOUND', 'CUSTOMER_INPAYMENT', 'TRANSFER_INBOUND', 
        'TRANSFER_INSTANT_OUTBOUND', 'TRANSFER_OUTBOUND', 'TAX_OPTIMIZATION', 
        'INTEREST_PAYMENT', 'DIVIDEND'
    ]
    
    # Filtramos para ver qué líneas del CSV NO están en esa lista
    df_ignorados = df[~df['type'].isin(eventos_controlados)]
    
    print("\n🚨 EVENTOS QUE EL PROGRAMA ESTÁ IGNORANDO:")
    if df_ignorados.empty:
        print("   ¡Ninguno! El programa está leyendo el 100% de tus movimientos.")
    else:
        print(df_ignorados['type'].value_counts())
else:
    print("No se encontró el CSV.")