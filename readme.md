# ...

## Hipotesis & Abstract

Este proyecto implementa y comprueba empiricamente los principios de la Teoria Moderna de Cartas (MPT) de Harry Markowitz.

La hipotesis es que la diversificacion estrategica mediante el analisis de la matriz de covarianza permite aislar el riesgo no sistematico de los activos. Por lo tanto, un algoritmo de optimizacion lograra un ratio de sharpe superior al de cualquier cartera de activos aislados (en adelante SSP, single stock portfolio), maximizando el exceso de retorno sobre una tasa de libre de riesgo dada.

## Universo de activos

AAPL: Tecnologia
JPM: Bancos
XOM: Energia
TLT: Bonos del tesoro
GLD: Oro

Fuentes de datos: precios de cierre ajustados (Adj Close)

## Metodologia

Se divide en tres fases de comprobacion secuencial

1. Grupo de control (SSP):
Calculo del rendimiento volatilidad y ratio de sharpe asumientdo una asignacion del 100% a cada activo individualmente.

2. Simulacion de Montecarlo
Generacion de un espacio de soluciones de n portafolios aleatorios mediante operaciones tensoriales  permitiendo solamente compras.

3. Optimizacion analitica
Uso de algebra lineal para encontrar la cartera tangente exacta de la forma determinista y compararla con el optimo estocastico.

## Resulados

### Matriz de covarianza hallada

| Ticker | AAPL | GLD | JPM | TLT | XOM |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **AAPL** | 0.079357 | 0.002267 | 0.030720 | -0.007064 | 0.021890 |
| **GLD** | 0.002267 | 0.025017 | -0.002383 | 0.005184 | 0.002407 |
| **JPM** | 0.030720 | -0.002383 | 0.076139 | -0.016026 | 0.037309 |
| **TLT** | -0.007064 | 0.005184 | -0.016026 | 0.022791 | -0.010961 |
| **XOM** | 0.021890 | 0.002407 | 0.037309 | -0.010961 | 0.061818 |

### Retorno, varianza y sharpe de SSP

Single stock portfolios: 5
AAPL ssp ex. returns: 27.44% anual - risk: 28.17% - Sharpe Ratio: 0.09
XOM ssp ex. returns: 9.30% anual - risk: 15.82% - Sharpe Ratio: -0.23
JPM ssp ex. returns: 18.99% anual - risk: 27.59% - Sharpe Ratio: 0.00
TLT ssp ex. returns: 3.83% anual - risk: 15.10% - Sharpe Ratio: -0.30
GLD ssp ex. returns: 10.33% anual - risk: 24.86% - Sharpe Ratio: -0.10

