import yfinance as yf
import requests
from datos import cargar_datos
from calculadora import calcular_metricas

def isin_a_ticker(isin):
    """Consulta oculta a Yahoo Finance para traducir ISIN a Tícker"""
    url = f"https://query2.finance.yahoo.com/v1/finance/search?q={isin}"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    try:
        response = requests.get(url, headers=headers)
        data = response.json()
        if 'quotes' in data and len(data['quotes']) > 0:
            return data['quotes'][0]['symbol']
    except Exception as e:
        pass
    return None

def obtener_tasa_usd_eur():
    """Obtiene el tipo de cambio en tiempo real: 1 USD = X EUR"""
    try:
        ticker = yf.Ticker("USDEUR=X")
        tasa = ticker.history(period="1d")['Close'].iloc[-1]
        return tasa
    except Exception:
        # Si falla internet, ponemos un valor de seguridad aproximado
        return 0.92 

def probar_precios_cartera_abierta():
    df, _ = cargar_datos()
    if df is None:
        print("❌ No se encontró CSV.")
        return

    metricas = calcular_metricas(df)
    df_cartera = metricas['df_cartera']
    
    if df_cartera.empty:
        print("❌ No hay activos en la cartera abierta actualmente.")
        return
        
    activos_vivos = df_cartera.index.tolist()

    df_compras = df[df['type'].isin(['BUY', 'SAVINGS_PLAN'])].dropna(subset=['symbol', 'name'])
    mapa_activos = df_compras.drop_duplicates(subset=['name']).set_index('name')['symbol'].to_dict()
    
    print("="*60)
    print(f" 📡 BUSCANDO PRECIOS EN DIRECTO (Solo los {len(activos_vivos)} activos vivos)")
    print("="*60)
    
    # Obtenemos la tasa de cambio una sola vez para no saturar internet
    print("💱 Obteniendo tipo de cambio actual...")
    tasa_cambio = obtener_tasa_usd_eur()
    print(f"   => 1 USD = {tasa_cambio:.4f} EUR\n")
    
    for nombre in activos_vivos:
        isin = mapa_activos.get(nombre)
        print(f"🏢 {nombre} (ISIN: {isin})")
        
        if not isin:
            print("   ❌ No se encontró el ISIN.")
            continue
            
        ticker = isin_a_ticker(isin)
        
        if ticker:
            print(f"   ✅ Tícker: {ticker}")
            try:
                stock = yf.Ticker(ticker)
                precio = stock.history(period="1d")['Close'].iloc[-1]
                moneda = stock.info.get('currency', '???')
                
                # --- LA MAGIA DE LA CONVERSIÓN ---
                if moneda == 'USD':
                    precio_eur = precio * tasa_cambio
                    print(f"   💵 Precio: {precio:.2f} USD  ==>  {precio_eur:.2f} € (Euros)")
                elif moneda == 'EUR':
                    print(f"   💵 Precio: {precio:.2f} €")
                else:
                    print(f"   💵 Precio: {precio:.2f} {moneda}")
                print("-" * 40)
                    
            except Exception as e:
                print(f"   ❌ Error al obtener precio: {e}")
        else:
            print("   ❌ No se encontró Tícker en Yahoo.")

if __name__ == "__main__":
    probar_precios_cartera_abierta()