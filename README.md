# 📈 Trade Republic Analytics - Wealth Management Tool

## 💡 Visión del Proyecto
Herramienta en Python diseñada para el análisis automatizado de carteras de inversión a partir de extractos en crudo (CSV) de Trade Republic. 

Este proyecto busca transformar el seguimiento visual básico de una app de bróker en un verdadero panel de control de **Gestión Patrimonial (Wealth Management)**. El objetivo no es solo ver el saldo actual, sino auditar matemáticamente la rentabilidad real, los costes operativos ocultos y la exposición del capital.

## 🎯 Objetivos Financieros (Los 4 Pilares)
El motor de análisis está diseñado para responder a preguntas clave sobre la salud del patrimonio, estructurado en cuatro pilares fundamentales:

### 1. Capital Neto Aportado (Cash Flow)
Seguimiento estricto de los flujos de entrada y salida (*Net Inflows*).
* **Métrica:** Depósitos totales - Retiradas totales.
* **Objetivo:** Conocer el capital base real en riesgo sobre el cual se deben calcular las rentabilidades.

### 2. Eficiencia Operativa (Costes de Fricción)
Auditoría del "asesino silencioso" de la rentabilidad a largo plazo.
* **Métrica:** Sumatoria de Comisiones pagadas (`fee`) e Impuestos retenidos (`tax`).
* **Objetivo:** Diferenciar entre la rentabilidad bruta de los activos y la rentabilidad **neta** real que llega al bolsillo del inversor.

### 3. Exposición y Coste Medio (Average Cost Basis)
Monitorización matemática de la cartera viva.
* **Métrica:** Cálculo del Precio Medio de Compra ponderado por el volumen de acciones de cada empresa/ETF.
* **Objetivo:** Conocer el punto de equilibrio exacto (*break-even*) de cada activo histórico.

### 4. Rentabilidad Realizada (Pérdidas y Ganancias)
El rendimiento tangible y pasivo del dinero.
* **Métrica:** Sumatoria de Ingresos Pasivos (Dividendos + Intereses de cuenta remunerada) y Plusvalías/Minusvalías ejecutadas por ventas.

---

## 🚀 Fases de Desarrollo (Roadmap)
* **Fase 1 (Actual):** Motor estático. Procesamiento de archivos `.csv`, limpieza de datos, y cálculo exacto de todos los flujos históricos (comisiones, dividendos, aportaciones y precio medio).
* **Fase 2 (Futuro):** Integración de precios en vivo (ej. `yfinance`) para cruzar el *Average Cost Basis* calculado en local con la cotización en tiempo real de los mercados, obteniendo así la **rentabilidad latente** (Unrealized P&L).

## 📂 Estructura de Directorios

```text
trade-republic-analytics/
├── data/
│   ├── input/               # Extractos crudos (.csv) del bróker [Ignorados en Git por privacidad]
│   └── output/              # Reportes financieros generados
├── config/                  
│   └── categorias.json      # Reglas para agrupación de activos (ETFs, Acciones, Bonos)
├── src/                     
│   ├── main.py              # Orquestador del análisis y CLI
│   └── motor.py             # Lógica matemática, cálculo de promedios y parseo del CSV
├── requirements.txt         # Dependencias del proyecto
└── README.md