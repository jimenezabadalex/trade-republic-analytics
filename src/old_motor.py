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
    
    for col in ['amount', 'fee', 'tax', 'shares', 'price']:
        if col in df.columns:
            df[col] = df[col].fillna(0.0)
            
    df['datetime'] = pd.to_datetime(df['datetime'])
    df = df.sort_values('datetime', ascending=True).reset_index(drop=True)

    # PILAR 1 Y 2
    tipos_ingreso = ['TRANSFER_INSTANT_INBOUND', 'CUSTOMER_INPAYMENT', 'TRANSFER_INBOUND']
    tipos_retirada = ['TRANSFER_INSTANT_OUTBOUND', 'TRANSFER_OUTBOUND']
    
    total_ingresado = df[df['type'].isin(tipos_ingreso)]['amount'].sum()
    total_retirado = df[df['type'].isin(tipos_retirada)]['amount'].sum()
    capital_neto = total_ingresado + total_retirado
    
    total_comisiones = df['fee'].sum()
    total_impuestos = df['tax'].sum()
    optimizacion_fiscal = df[df['type'] == 'TAX_OPTIMIZATION']['amount'].sum()
    coste_friccion = total_comisiones + total_impuestos - optimizacion_fiscal
    
    total_intereses = df[df['type'] == 'INTEREST_PAYMENT']['amount'].sum()
    total_dividendos = df[df['type'] == 'DIVIDEND']['amount'].sum()

    # PILAR 3 Y 4
    cartera = {}
    beneficio_realizado = 0.0
    
    # NUEVO: Aquí guardaremos el P&L desglosado por cada empresa
    pnl_por_activo = {}
    
    for index, row in df.iterrows():
        tipo = row['type']
        activo = row['name']
        acciones_raw = row['shares']
        precio = row['price']
        
        if pd.isna(activo) or pd.isna(acciones_raw) or acciones_raw == 0:
            continue
            
        eventos_validos = ['BUY', 'SAVINGS_PLAN', 'SELL', 'SPLIT', 'REVERSE_SPLIT', 'REVERSE_STOCK_SPLIT', 'SPIN_OFF', 'MIGRATION', 'STOCKPERK']
        if tipo not in eventos_validos:
            continue
            
        if activo not in cartera:
            cartera[activo] = {'Acciones': 0.0, 'Precio_Medio': 0.0, 'Invertido': 0.0}
            
        pos = cartera[activo]
        
        if tipo in ['BUY', 'SAVINGS_PLAN']:
            acciones_compradas = abs(acciones_raw)
            coste_compra = acciones_compradas * precio
            pos['Invertido'] += coste_compra
            pos['Acciones'] += acciones_compradas
            
            if pos['Acciones'] > 0:
                pos['Precio_Medio'] = pos['Invertido'] / pos['Acciones']
                
        elif tipo == 'SELL':
            acciones_vendidas = abs(acciones_raw)
            if pos['Precio_Medio'] > 0:
                ganancia_operacion = (precio - pos['Precio_Medio']) * acciones_vendidas
                beneficio_realizado += ganancia_operacion
                
                # NUEVO: Sumamos la ganancia o pérdida al historial de esa empresa en concreto
                if activo not in pnl_por_activo:
                    pnl_por_activo[activo] = 0.0
                pnl_por_activo[activo] += ganancia_operacion

            pos['Acciones'] -= acciones_vendidas
            pos['Invertido'] -= (acciones_vendidas * pos['Precio_Medio'])
            
            if pos['Acciones'] <= 0.0001:
                pos['Acciones'] = 0.0
                pos['Invertido'] = 0.0
                pos['Precio_Medio'] = 0.0
                
        else:
            pos['Acciones'] += acciones_raw
            if pos['Acciones'] <= 0.0001:
                pos['Acciones'] = 0.0
                pos['Invertido'] = 0.0
                pos['Precio_Medio'] = 0.0
            elif pos['Invertido'] > 0:
                pos['Precio_Medio'] = pos['Invertido'] / pos['Acciones']

    # Preparamos tabla de Cartera
    df_cartera = pd.DataFrame.from_dict(cartera, orient='index')
    df_cartera = df_cartera[df_cartera['Acciones'] > 0]
    df_cartera = df_cartera.sort_values('Invertido', ascending=False)
    total_invertido_actual = df_cartera['Invertido'].sum() if not df_cartera.empty else 0.0

    # NUEVO: Preparamos tabla de P&L desglosado
    df_pnl = pd.DataFrame.from_dict(pnl_por_activo, orient='index', columns=['P&L_Bruto'])
    # Ordenamos de mayor ganancia a mayor pérdida
    df_pnl = df_pnl.sort_values('P&L_Bruto', ascending=False)

    # --- IMPRESIÓN DEL INFORME PATRIMONIAL ---
    print("="*60)
    print(" 🏛️  PANEL DE GESTIÓN PATRIMONIAL - TRADE REPUBLIC")
    print("="*60)
    
    print("\n💰 1. FLUJO DE CAJA (NET INFLOWS)")
    print(f"   => CAPITAL NETO EN RIESGO: {capital_neto:,.2f} €")
    
    print("\n🩸 2. COSTES DE FRICCIÓN (EFICIENCIA)")
    print(f"   - Comisiones Brutas:       {total_comisiones:,.2f} €")
    print(f"   - Impuestos Retenidos:     {total_impuestos:,.2f} €")
    if optimizacion_fiscal > 0:
        print(f"   + Ajustes/Devoluciones TR: {optimizacion_fiscal:,.2f} €")
    print(f"   ---------------------------------------")
    print(f"   => COSTE DE FRICCIÓN NETO: {coste_friccion:,.2f} €")
    
    print("\n📈 3. RENTABILIDAD REALIZADA E INGRESOS (PILAR 4)")
    print(f"   + Intereses de la cuenta:  {total_intereses:,.2f} €")
    print(f"   + Dividendos cobrados:     {total_dividendos:,.2f} €")
    print(f"   + P&L Ventas (Bruto):      {beneficio_realizado:,.2f} €")
    print(f"   ---------------------------------------")
    
    beneficio_neto = beneficio_realizado + total_intereses + total_dividendos + coste_friccion
    print(f"   => BENEFICIO NETO REAL*:   {beneficio_neto:,.2f} €")
    print("      *(Ventas + Intereses + Dividendos - Comisiones Netas)")
    
    # NUEVO: IMPRIMIMOS EL DESGLOSE DE VENTAS
    print("\n" + "-"*60)
    print(" 🎯 DESGLOSE DE P&L POR ACTIVO VENDIDO (Bruto)")
    print("-"*60)
    if df_pnl.empty:
        print("   No hay ventas registradas.")
    else:
        df_pnl_mostrar = df_pnl.copy()
        df_pnl_mostrar['P&L_Bruto'] = df_pnl_mostrar['P&L_Bruto'].apply(lambda x: f"{x:,.2f} €")
        pd.set_option('display.max_rows', None)
        print(df_pnl_mostrar.to_string())

    print("\n" + "="*60)
    print(f" 📊 4. CARTERA ABIERTA (Invertido: {total_invertido_actual:,.2f} €)")
    print("="*60)
    
    if df_cartera.empty:
        print("   No hay posiciones abiertas actualmente.")
    else:
        df_mostrar = df_cartera.copy()
        df_mostrar['Acciones'] = df_mostrar['Acciones'].apply(lambda x: f"{x:,.4f}")
        df_mostrar['Precio_Medio'] = df_mostrar['Precio_Medio'].apply(lambda x: f"{x:,.2f} €")
        df_mostrar['Invertido'] = df_mostrar['Invertido'].apply(lambda x: f"{x:,.2f} €")
        
        pd.set_option('display.max_rows', None)
        print(df_mostrar.to_string())

if __name__ == "__main__":
    procesar_csv()