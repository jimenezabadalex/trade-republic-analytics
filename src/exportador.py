import pandas as pd
from pathlib import Path

def exportar_a_excel(metricas, df_trimestres, nombre_salida="Reporte_TradeRepublic.xlsx"):
    """Exporta todas las métricas y dataframes a un único archivo Excel con varias hojas."""
    
    BASE_DIR = Path(__file__).parent.parent
    dir_output = BASE_DIR / "data" / "output"
    
    # Nos aseguramos de que la carpeta exista, si no, la crea automáticamente
    dir_output.mkdir(parents=True, exist_ok=True) 
    ruta_archivo = dir_output / nombre_salida
    
    print("\n" + "="*80)
    print(" 💾 7. EXPORTANDO A EXCEL...")
    print("="*80)
    
    # 1. Preparamos los datos del Resumen Global
    df_cartera = metricas['df_cartera']
    total_invertido = metricas['total_invertido']
    
    if 'Valor_Actual' in df_cartera.columns:
        total_valor_actual = df_cartera['Valor_Actual'].sum()
        total_pnl_latente = df_cartera['PnL_Latente'].sum()
    else:
        total_valor_actual = total_invertido
        total_pnl_latente = 0.0
        
    beneficio_neto = metricas['beneficio_realizado'] + metricas['dividendos'] + metricas['intereses'] - metricas['coste_friccion']
    gran_total = beneficio_neto + total_pnl_latente
    
    # Creamos una tabla resumen bonita
    datos_resumen = {
        'Concepto': [
            'Capital Neto Aportado',
            'Costes Totales (Comisiones + Impuestos - Opt. Fiscal)',
            'Total Dividendos e Intereses',
            'Beneficio Histórico Realizado (Solo Ventas)',
            'Beneficio Neto Histórico (Cerrado)',
            'Capital Invertido Actual',
            'Valor de Mercado Actual',
            'P&L Latente (Mercado Actual)',
            'RENTABILIDAD HISTÓRICA TOTAL (MAX)'
        ],
        'Valor (€)': [
            metricas['capital_neto'],
            metricas['coste_friccion'],
            metricas['dividendos'] + metricas['intereses'],
            metricas['beneficio_realizado'],
            beneficio_neto,
            total_invertido,
            total_valor_actual,
            total_pnl_latente,
            gran_total
        ]
    }
    df_resumen = pd.DataFrame(datos_resumen)

    # 2. Escribimos todas las tablas en un único archivo Excel usando hojas separadas
    try:
        with pd.ExcelWriter(ruta_archivo, engine='openpyxl') as writer:
            # Hoja 1: Resumen
            df_resumen.to_excel(writer, sheet_name='1. Resumen Global', index=False)
            
            # Hoja 2: Cartera Abierta
            if not df_cartera.empty:
                df_cartera.to_excel(writer, sheet_name='2. Cartera Abierta')
                
            # Hoja 3: Evolución Trimestral
            if not df_trimestres.empty:
                df_trimestres.to_excel(writer, sheet_name='3. Trimestres', index=False)
                
            # Hoja 4: Historial de P&L por activo
            if not metricas['df_pnl'].empty:
                metricas['df_pnl'].to_excel(writer, sheet_name='4. PnL Historico')
                
        print(f"   ✅ ¡Éxito! Reporte guardado en: {ruta_archivo}")
    except Exception as e:
        print(f"   ❌ Error al guardar el Excel: {e}")
        print("   (Si tienes el archivo Excel abierto, ciérralo y vuelve a intentarlo)")