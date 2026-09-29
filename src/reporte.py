import pandas as pd

def imprimir_informe(nombre_archivo, metricas):
    """Recibe los cálculos y los muestra por consola con formato."""
    print("="*60)
    print(" 🏛️  PANEL DE GESTIÓN PATRIMONIAL - TRADE REPUBLIC")
    print("="*60)
    print(f"📄 Analizando: {nombre_archivo}")
    
    print("\n💰 1. FLUJO DE CAJA (NET INFLOWS)")
    print(f"   => CAPITAL NETO EN RIESGO: {metricas['capital_neto']:,.2f} €")
    
    print("\n🩸 2. COSTES DE FRICCIÓN (EFICIENCIA)")
    print(f"   - Comisiones Brutas:       {metricas['comisiones']:,.2f} €")
    print(f"   - Impuestos Retenidos:     {metricas['impuestos']:,.2f} €")
    if metricas['optimizacion'] > 0:
        print(f"   + Ajustes/Devoluciones TR: {metricas['optimizacion']:,.2f} €")
    print(f"   ---------------------------------------")
    print(f"   => COSTE DE FRICCIÓN NETO: {metricas['coste_friccion']:,.2f} €")
    
    print("\n📈 3. RENTABILIDAD REALIZADA E INGRESOS (PILAR 4)")
    print(f"   + Intereses de la cuenta:  {metricas['intereses']:,.2f} €")
    print(f"   + Dividendos cobrados:     {metricas['dividendos']:,.2f} €")
    print(f"   + P&L Ventas (Bruto):      {metricas['beneficio_realizado']:,.2f} €")
    print(f"   ---------------------------------------")
    
    beneficio_neto = metricas['beneficio_realizado'] + metricas['intereses'] + metricas['dividendos'] + metricas['coste_friccion']
    print(f"   => BENEFICIO NETO REAL*:   {beneficio_neto:,.2f} €")
    print("      *(Ventas + Intereses + Dividendos - Comisiones Netas)")
    
    print("\n" + "-"*60)
    print(" 🎯 DESGLOSE DE P&L POR ACTIVO VENDIDO (Bruto)")
    print("-"*60)
    df_pnl = metricas['df_pnl']
    if df_pnl.empty:
        print("   No hay ventas registradas.")
    else:
        df_pnl_mostrar = df_pnl.copy()
        df_pnl_mostrar['P&L_Bruto'] = df_pnl_mostrar['P&L_Bruto'].apply(lambda x: f"{x:,.2f} €")
        pd.set_option('display.max_rows', None)
        print(df_pnl_mostrar.to_string())

    print("\n" + "="*60)
    print(f" 📊 4. CARTERA ABIERTA (Invertido: {metricas['total_invertido']:,.2f} €)")
    print("="*60)
    
    df_cartera = metricas['df_cartera']
    if df_cartera.empty:
        print("   No hay posiciones abiertas actualmente.")
    else:
        df_mostrar = df_cartera.copy()
        df_mostrar['Acciones'] = df_mostrar['Acciones'].apply(lambda x: f"{x:,.4f}")
        df_mostrar['Precio_Medio'] = df_mostrar['Precio_Medio'].apply(lambda x: f"{x:,.2f} €")
        df_mostrar['Invertido'] = df_mostrar['Invertido'].apply(lambda x: f"{x:,.2f} €")
        
        pd.set_option('display.max_rows', None)
        print(df_mostrar.to_string())