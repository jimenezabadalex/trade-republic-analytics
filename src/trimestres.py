import pandas as pd

def analizar_trimestres(df_csv, df_ventas):
    """Agrupa los ingresos, gastos y ventas por trimestres."""
    
    # 1. Preparamos el CSV general
    df = df_csv.copy()
    df['Trimestre'] = df['datetime'].dt.to_period('Q')
    
    # 2. Preparamos las ventas (si hay)
    if not df_ventas.empty:
        df_v = df_ventas.copy()
        df_v['Trimestre'] = df_v['datetime'].dt.to_period('Q')
        ventas_agrupadas = df_v.groupby('Trimestre')['PnL_Venta'].sum()
    else:
        ventas_agrupadas = pd.Series(dtype=float)

    # 3. Calculamos métricas por cada trimestre que exista en tu historial
    trimestres = sorted(df['Trimestre'].unique())
    resultados = []
    
    for t in trimestres:
        dft = df[df['Trimestre'] == t]
        
        # Dinero que has metido en TR ese trimestre
        ingresos = dft[dft['type'].isin(['TRANSFER_INSTANT_INBOUND', 'CUSTOMER_INPAYMENT', 'TRANSFER_INBOUND'])]['amount'].sum()
        retiradas = abs(dft[dft['type'].isin(['TRANSFER_INSTANT_OUTBOUND', 'TRANSFER_OUTBOUND'])]['amount'].sum())
        capital_aportado = ingresos - retiradas
        
        # Rentabilidad pasiva (Intereses y Dividendos)
        intereses = dft[dft['type'] == 'INTEREST_PAYMENT']['amount'].sum()
        dividendos = dft[dft['type'] == 'DIVIDEND']['amount'].sum()
        
        # Gastos operativos
        comisiones = abs(dft['fee'].sum())
        impuestos = abs(dft['tax'].sum())
        
        # P&L de Ventas (lo buscamos en nuestro registro)
        pnl_ventas = ventas_agrupadas.get(t, 0.0)
        
        # Beneficio Neto Trimestral (Lo que has ganado/perdido cerrado en ese trimestre)
        beneficio_trimestral = pnl_ventas + intereses + dividendos - comisiones - impuestos
        
        resultados.append({
            'Trimestre': str(t),
            'Aportación Neta': capital_aportado,
            'Beneficio Ventas': pnl_ventas,
            'Dividendos': dividendos,
            'Intereses': intereses,
            'Costes (Com+Imp)': -(comisiones + impuestos),
            'BENEFICIO NETO': beneficio_trimestral
        })
        
    return pd.DataFrame(resultados)

def imprimir_trimestres(df_trimestres):
    print("\n" + "="*90)
    print(" 📆 6. EVOLUCIÓN HISTÓRICA POR TRIMESTRES (P&L Realizado)")
    print("="*90)
    
    if df_trimestres.empty:
        print("   No hay datos suficientes para mostrar trimestres.")
        return
        
    df_mostrar = df_trimestres.copy()
    
    # Formateamos los números para que se vean bonitos
    columnas_moneda = ['Aportación Neta', 'Beneficio Ventas', 'Dividendos', 'Intereses', 'Costes (Com+Imp)', 'BENEFICIO NETO']
    for col in columnas_moneda:
        df_mostrar[col] = df_mostrar[col].apply(lambda x: f"{x:+,.2f} €" if x != 0 else "-")
        
    pd.set_option('display.max_rows', None)
    # Escondemos el índice numérico para que quede más limpio
    print(df_mostrar.to_string(index=False))