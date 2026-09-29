import yfinance as yf
import requests

def isin_a_ticker(isin):
    url = f"https://query2.finance.yahoo.com/v1/finance/search?q={isin}"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    try:
        response = requests.get(url, headers=headers)
        data = response.json()
        if 'quotes' in data and len(data['quotes']) > 0:
            return data['quotes'][0]['symbol']
    except Exception:
        pass
    return None

def obtener_tasa_usd_eur():
    try:
        ticker = yf.Ticker("USDEUR=X")
        return ticker.history(period="1d")['Close'].iloc[-1]
    except Exception:
        return 0.92  # Valor de seguridad por si falla internet

def enriquecer_cartera(df_cartera, mapa_activos):
    """Recibe la cartera, busca los precios en directo y añade las columnas de Latente"""
    if df_cartera.empty:
        return df_cartera
        
    print("\n📡 Conectando con el mercado para valorar tu cartera en tiempo real...")
    tasa_cambio = obtener_tasa_usd_eur()
    
    precios_actuales = {}
    for nombre in df_cartera.index:
        isin = mapa_activos.get(nombre)
        if not isin:
            precios_actuales[nombre] = 0.0
            continue
            
        ticker = isin_a_ticker(isin)
        if ticker:
            try:
                stock = yf.Ticker(ticker)
                precio = stock.history(period="1d")['Close'].iloc[-1]
                moneda = stock.info.get('currency', 'EUR')
                if moneda == 'USD':
                    precio *= tasa_cambio
                precios_actuales[nombre] = precio
            except Exception:
                precios_actuales[nombre] = 0.0
        else:
            precios_actuales[nombre] = 0.0

    # Magia de Pandas: Añadimos las nuevas columnas matemáticas a la tabla
    df_cartera['Precio_Actual'] = df_cartera.index.map(precios_actuales).fillna(0.0)
    df_cartera['Valor_Actual'] = df_cartera['Acciones'] * df_cartera['Precio_Actual']
    df_cartera['PnL_Latente'] = df_cartera['Valor_Actual'] - df_cartera['Invertido']
    df_cartera['PnL_%'] = df_cartera.apply(
        lambda row: (row['PnL_Latente'] / row['Invertido'] * 100) if row['Invertido'] > 0 else 0.0, axis=1
    )
    
    return df_cartera