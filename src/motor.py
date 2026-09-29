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
    
    # Cargamos el CSV (forzamos los tipos numéricos para evitar errores)
    df = pd.read_csv(archivo)
    
    # Rellenamos los vacíos (NaN) con 0 en las columnas de dinero
    for col in ['amount', 'fee', 'tax']:
        if col in df.columns:
            df[col] = df[col].fillna(0.0)

    # ---------------------------------------------------------
    # PILAR 1: CAPITAL NETO APORTADO (Cash Flow)
    # ---------------------------------------------------------
    tipos_ingreso = ['TRANSFER_INSTANT_INBOUND', 'CUSTOMER_INPAYMENT']
    tipos_retirada = ['TRANSFER_INSTANT_OUTBOUND']
    
    # Filtramos y sumamos (round para evitar decimales infinitos de Python)
    total_ingresado = df[df['type'].isin(tipos_ingreso)]['amount'].sum()
    
    # Las retiradas suelen venir en negativo, así que usamos abs() por si acaso o sumamos directamente
    total_retirado = df[df['type'].isin(tipos_retirada)]['amount'].sum()
    
    capital_neto = total_ingresado + total_retirado # Sumamos porque el retirado ya es negativo

    # ---------------------------------------------------------
    # PILAR 2: EFICIENCIA OPERATIVA (Costes de Fricción)
    # ---------------------------------------------------------
    total_comisiones = df['fee'].sum()
    total_impuestos = df['tax'].sum()
    coste_total = total_comisiones + total_impuestos

    # ---------------------------------------------------------
    # PILAR 4 (Parcial): INGRESOS PASIVOS
    # ---------------------------------------------------------
    total_intereses = df[df['type'] == 'INTEREST_PAYMENT']['amount'].sum()

    # --- IMPRESIÓN DEL INFORME PATRIMONIAL ---
    print("="*50)
    print(" 🏛️  PANEL DE GESTIÓN PATRIMONIAL - FASE 1")
    print("="*50)
    
    print("\n💰 1. FLUJO DE CAJA (NET INFLOWS)")
    print(f"   + Depósitos totales:      {total_ingresado:,.2f} €")
    print(f"   - Retiradas totales:      {total_retirado:,.2f} €")
    print(f"   ---------------------------------------")
    print(f"   => CAPITAL NETO EN RIESGO: {capital_neto:,.2f} €")
    
    print("\n🩸 2. COSTES DE FRICCIÓN (EFICIENCIA)")
    print(f"   - Comisiones pagadas (fee): {total_comisiones:,.2f} €")
    print(f"   - Impuestos retenidos (tax): {total_impuestos:,.2f} €")
    
    print("\n💸 3. RENDIMIENTO PASIVO")
    print(f"   + Intereses de la cuenta:    {total_intereses:,.2f} €")
    
    print("\n" + "="*50)

if __name__ == "__main__":
    procesar_csv()