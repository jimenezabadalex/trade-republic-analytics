import pandas as pd

def calcular_metricas(df):
    tipos_ingreso = ['TRANSFER_INSTANT_INBOUND', 'CUSTOMER_INPAYMENT', 'TRANSFER_INBOUND']
    tipos_retirada = ['TRANSFER_INSTANT_OUTBOUND', 'TRANSFER_OUTBOUND']
    
    total_ingresado = df[df['type'].isin(tipos_ingreso)]['amount'].sum()
    total_retirado = df[df['type'].isin(tipos_retirada)]['amount'].sum()
    capital_neto = total_ingresado + total_retirado
    
    total_comisiones = abs(df['fee'].sum())
    total_impuestos = abs(df['tax'].sum())
    optimizacion_fiscal = abs(df[df['type'] == 'TAX_OPTIMIZATION']['amount'].sum())
    coste_friccion = total_comisiones + total_impuestos - optimizacion_fiscal
    
    total_intereses = df[df['type'] == 'INTEREST_PAYMENT']['amount'].sum()
    total_dividendos = df[df['type'] == 'DIVIDEND']['amount'].sum()

    cartera = {}
    beneficio_realizado = 0.0
    pnl_por_activo = {}
    
    # NUEVO: Aquí guardaremos la fecha y el beneficio de cada venta
    registro_ventas = [] 
    
    for index, row in df.iterrows():
        tipo = row['type']
        activo = row['name']
        acciones_raw = row['shares']
        precio = row['price']
        fecha = row['datetime']
        
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
                
                if activo not in pnl_por_activo:
                    pnl_por_activo[activo] = 0.0
                pnl_por_activo[activo] += ganancia_operacion
                
                # NUEVO: Guardamos el ticket de la venta
                registro_ventas.append({
                    'datetime': fecha,
                    'Activo': activo,
                    'PnL_Venta': ganancia_operacion
                })

            pos['Acciones'] -= acciones_vendidas
            pos['Invertido'] -= (acciones_vendidas * pos['Precio_Medio'])
            
            if pos['Acciones'] <= 0.0001:
                pos['Acciones'] = 0.0
                pos['Invertido'] = 0.0
                pos['Precio_Medio'] = 0.0
                
        else:
            pos['Acciones'] += acciones_raw
            if pos['Acciones'] > 0.0001 and pos['Invertido'] > 0:
                pos['Precio_Medio'] = pos['Invertido'] / pos['Acciones']
            elif pos['Acciones'] <= 0.0001:
                pos['Acciones'] = 0.0
                pos['Precio_Medio'] = 0.0

    df_cartera = pd.DataFrame.from_dict(cartera, orient='index')
    if not df_cartera.empty:
        df_cartera = df_cartera[df_cartera['Acciones'] > 0]
        df_cartera = df_cartera.sort_values('Invertido', ascending=False)
    total_invertido = df_cartera['Invertido'].sum() if not df_cartera.empty else 0.0

    df_pnl = pd.DataFrame.from_dict(pnl_por_activo, orient='index', columns=['P&L_Bruto'])
    if not df_pnl.empty:
        df_pnl = df_pnl.sort_values('P&L_Bruto', ascending=False)

    df_compras = df[df['type'].isin(['BUY', 'SAVINGS_PLAN'])].dropna(subset=['symbol', 'name'])
    mapa_activos = df_compras.drop_duplicates(subset=['name']).set_index('name')['symbol'].to_dict()

    # NUEVO: Convertimos el registro a un DataFrame para dárselo a los trimestres
    df_ventas = pd.DataFrame(registro_ventas) if registro_ventas else pd.DataFrame(columns=['datetime', 'Activo', 'PnL_Venta'])

    return {
        'capital_neto': capital_neto,
        'coste_friccion': coste_friccion,
        'comisiones': total_comisiones,
        'impuestos': total_impuestos,
        'optimizacion': optimizacion_fiscal,
        'intereses': total_intereses,
        'dividendos': total_dividendos,
        'beneficio_realizado': beneficio_realizado,
        'df_cartera': df_cartera,
        'df_pnl': df_pnl,
        'total_invertido': total_invertido,
        'mapa_activos': mapa_activos,
        'df_ventas': df_ventas # <--- Pasamos el diario de ventas
    }