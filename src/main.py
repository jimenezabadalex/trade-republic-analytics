from datos import cargar_datos
from calculadora import calcular_metricas
from reporte import imprimir_informe

def main():
    # 1. Extraer
    df, nombre_archivo = cargar_datos()
    if df is None:
        print("❌ No se encontró ningún CSV en data/input/")
        return
        
    # 2. Calcular
    metricas = calcular_metricas(df)
    
    # 3. Mostrar
    imprimir_informe(nombre_archivo, metricas)

if __name__ == "__main__":
    main()