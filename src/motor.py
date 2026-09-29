import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
DIR_INPUT = BASE_DIR / "data" / "input"

def procesar_csv():
    archivos_csv = list(DIR_INPUT.glob("*.csv"))
    if not archivos_csv:
        print("❌ No se encontró ningún CSV en data/input/")
        return
    
    archivo = archivos_csv[0]
    print(f"📄 Analizando cartera desde: {archivo.name}...\n")
    
    df = pd.read_csv(archivo)
    
    # 0. LIMPIEZA Y PREPARACIÓN DE DATOS
    for col in ['amount', 'fee', 'tax', 'shares', 'price']:
        if col in df.columns:
            df[col] = df[col].fillna(0.0)
            
    # CRUCIAL: Ordenamos cronológicamente (del más antiguo al más nuevo)
    # Trade Republic los da del más nuevo al más antiguo, si no le damos la vuelta, las mates fallan.
    df['datetime'] = pd.to_datetime(df['datetime'])
    df = df.sort_values('datetime', ascending=True).reset_index(drop=True)

    # Variables Pilares 1 y 2
    tipos_ingreso = ['TRANSFER_INSTANT_INBOUND', 'CUSTOMER_INPAYMENT']
    tipos_retirada = ['TRANSFER_INSTANT_OUTBOUND']
    total_ingresado = df[df['type'].isin(tipos_ingreso)]['amount'].sum()
    total_retirado = df[df['type'].isin(tipos_retirada)]['amount'].sum()
    capital_neto = total_ingresado + total_retirado
    coste_friccion = df['fee'].sum() + df['tax'].sum()
    total_intereses = df[df['type'] == 'INTEREST_PAYMENT']['amount'].sum()

    # ---------------------------------------------------------
    # PILAR 3: CARTERA VIVA Y PRECIO MEDIO (Average Cost Basis)
    # ---------------------------------------------------------
    cartera = {}
    
    for index, row in df.iterrows():
        tipo = row['type']
        activo = row['name']
        acciones = row['shares']
        precio = row['price']
        
        # Solo procesamos compras y ventas de activos válidos
        if pd.isna(activo) or acciones == 0 or tipo not in ['BUY', 'SELL']:
            continue
            
        if activo not in cartera:
            cartera[activo] = {'Acciones': 0.0, 'Precio_Medio': 0.0, 'Invertido': 0.0}
            
        pos = cartera[activo]
        
        if tipo == 'BUY':
            nuevo_total = pos['Acciones'] + acciones
            coste_compra = acciones * precio
            pos['Invertido'] += coste_compra
            pos['Acciones'] = nuevo_total
            if pos['Acciones'] > 0:
                pos['Precio_Medio'] = pos['Invertido'] / pos['Acciones']
                
        elif tipo == 'SELL':
            pos['Acciones'] -= acciones
            # Reducimos el capital invertido proporcionalmente
            pos['Invertido'] -= (acciones * pos['Precio_Medio'])
            
            # Limpieza por errores de redondeo de decimales (ej. 0.000000001 acciones)
            if pos['Acciones'] <= 1e-6:
                pos['Acciones'] = 0.0
                pos['Invertido'] = 0.0
                pos['Precio_Medio'] = 0.0

    # Convertimos el diccionario en un DataFrame para mostrarlo bonito
    df_cartera = pd.DataFrame.from_dict(cartera, orient='index')
    # Filtramos para mostrar solo las posiciones que aún tienes abiertas (>0)
    df_cartera = df_cartera[df_cartera['Acciones'] > 0]
    # Ordenamos de mayor a menor capital invertido
    df_cartera = df_cartera.sort_values('Invertido', ascending=False)


    # --- IMPRESIÓN DEL INFORME PATRIMONIAL ---
    print("="*60)
    print(" 🏛️  PANEL DE GESTIÓN PATRIMONIAL - TRADE REPUBLIC")
    print("="*60)
    
    print("\n💰 1. FLUJO DE CAJA (NET INFLOWS)")
    print(f"   => CAPITAL NETO EN RIESGO: {capital_neto:,.2f} €")
    
    print("\n🩸 2. COSTES DE FRICCIÓN (EFICIENCIA)")
    print(f"   => Comisiones e Impuestos: {coste_friccion:,.2f} €")
    
    print("\n💸 3. RENDIMIENTO PASIVO")
    print(f"   => Intereses de la cuenta: {total_intereses:,.2f} €")
    
    print("\n" + "="*60)
    print(" 📊 4. CARTERA ABIERTA (POSICIONES ACTUALES)")
    print("="*60)
    
    if df_cartera.empty:
        print("   No hay posiciones abiertas actualmente.")
    else:
        # Formateamos los números para que se vean como moneda y con 2/4 decimales
        df_mostrar = df_cartera.copy()
        df_mostrar['Acciones'] = df_mostrar['Acciones'].apply(lambda x: f"{x:,.4f}")
        df_mostrar['Precio_Medio'] = df_mostrar['Precio_Medio'].apply(lambda x: f"{x:,.2f} €")
        df_mostrar['Invertido'] = df_mostrar['Invertido'].apply(lambda x: f"{x:,.2f} €")
        
        # Ajustamos para que Pandas imprima todas las filas en la consola
        pd.set_option('display.max_rows', None)
        print(df_mostrar.to_string())

if __name__ == "__main__":
    procesar_csv()
    