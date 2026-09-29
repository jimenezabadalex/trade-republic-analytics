from datos import cargar_datos
from calculadora import calcular_metricas
from mercado import enriquecer_cartera
from reporte import imprimir_informe

def main():
    # 1. Extraer Datos
    df, nombre_archivo = cargar_datos()
    if df is None:
        print("❌ No se encontró ningún CSV en data/input/")
        return
        
    # 2. Matemáticas Históricas
    metricas = calcular_metricas(df)
    
    # 3. Datos en Tiempo Real (Fase 2)
    metricas['df_cartera'] = enriquecer_cartera(metricas['df_cartera'], metricas['mapa_activos'])
    
    # 4. Mostrar Informe
    imprimir_informe(nombre_archivo, metricas)

if __name__ == "__main__":
    main()