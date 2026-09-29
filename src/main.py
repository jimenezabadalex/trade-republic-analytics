from datos import cargar_datos
from calculadora import calcular_metricas
from mercado import enriquecer_cartera
from reporte import imprimir_informe
from trimestres import analizar_trimestres, imprimir_trimestres # <-- NUEVO

def main():
    # 1. Extraer
    df, nombre_archivo = cargar_datos()
    if df is None:
        print("❌ No se encontró ningún CSV en data/input/")
        return
        
    # 2. Calcular Base
    metricas = calcular_metricas(df)
    
    # 3. Mercado en Tiempo Real
    metricas['df_cartera'] = enriquecer_cartera(metricas['df_cartera'], metricas['mapa_activos'])
    
    # 4. Análisis Trimestral (NUEVO)
    df_trimestres = analizar_trimestres(df, metricas['df_ventas'])
    
    # 5. Imprimir Informes
    imprimir_informe(nombre_archivo, metricas)
    imprimir_trimestres(df_trimestres) # <-- NUEVO

if __name__ == "__main__":
    main()