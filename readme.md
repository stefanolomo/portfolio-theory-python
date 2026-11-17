# Portfolio Theory Project

## 1. Hipótesis & Abstract

Este proyecto implementa y comprueba empíricamente los principios de la Teoría Moderna de Carteras (MPT) de Harry Markowitz.

La hipótesis es que la diversificación estratégica mediante el análisis de la matriz de covarianza permite aislar el riesgo no sistemático de los activos. Por lo tanto, un algoritmo de optimización logrará un Ratio de Sharpe superior al de cualquier cartera de activos aislados (en adelante SSP, *Single Stock Portfolio*), maximizando el exceso de retorno sobre una tasa libre de riesgo dada.

## 2. Universo de Activos

*   **AAPL:** Tecnología
*   **JPM:** Bancos
*   **XOM:** Energía
*   **TLT:** Bonos del Tesoro
*   **GLD:** Oro

Se toma un *Risk-Free Rate* (RFR) realista del 5.12% anual.  
**Fuentes de datos:** Precios de cierre ajustados (*Adj Close*) extraídos vía la API de `yfinance`.

## 3. Metodología

El análisis se divide en tres fases de comprobación secuencial:

### 3.1. Grupo de Control (SSP)
Cálculo del rendimiento, volatilidad y Ratio de Sharpe asumiendo una asignación del 100% a cada activo individualmente.

### 3.2. Simulación Estocástica (Montecarlo)
Generación de un espacio de soluciones de $n$ portafolios aleatorios mediante operaciones tensoriales vectorizadas (`np.einsum`), permitiendo solamente compras (*Long-Only*). 

**Análisis de Complejidad:**
La cantidad de iteraciones necesarias para saturar el espacio geométrico crece en tiempo exponencial bajo la fórmula $n = k^{N - 1}$, donde:
*   $k$: Resolución de la búsqueda (discretización del capital).
*   $N$: Cantidad de activos en el universo.

Para este experimento se asume una resolución de precisión porcentual ($k=100$) en un universo de $N=5$ activos. Por lo tanto, el motor somete la matriz a $n = 100^4 = 100.000.000$ de iteraciones divididas en lotes para optimizar el uso de RAM.

### 3.3. Optimización Analítica

*   **3.3.1. Ascenso de Gradiente (SciPy SLSQP):** Uso de cálculo diferencial numérico para hallar el máximo Ratio de Sharpe atado a las restricciones de negocio (*Long-Only*, los pesos suman exactamente 100%). 
*   **3.3.2. Forma Cerrada (Álgebra Lineal):** Cálculo de la cartera tangente óptima absoluta mediante la inversión de la matriz de covarianza (permitiendo posiciones cortas o *Long-Short*):

$$\mathbf{w}_T = \frac{\boldsymbol{\Sigma}^{-1} (\boldsymbol{\mu} - r_f \mathbf{1})}{\mathbf{1}^T \boldsymbol{\Sigma}^{-1} (\boldsymbol{\mu} - r_f \mathbf{1})}$$

---

## 4. Resultados

### 4.1. Matriz de Covarianza (Anualizada)

| Ticker | AAPL | GLD | JPM | TLT | XOM |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **AAPL** | 0.079357 | 0.002267 | 0.030720 | -0.007064 | 0.021890 |
| **GLD** | 0.002267 | 0.025017 | -0.002383 | 0.005184 | 0.002407 |
| **JPM** | 0.030720 | -0.002383 | 0.076139 | -0.016026 | 0.037309 |
| **TLT** | -0.007064 | 0.005184 | -0.016026 | 0.022791 | -0.010961 |
| **XOM** | 0.021890 | 0.002407 | 0.037309 | -0.010961 | 0.061818 |

### 4.2. Portafolios de Control (SSP)

| Activo | Retorno Esperado | Riesgo (Volatilidad) | Sharpe Ratio |
| :--- | :--- | :--- | :--- |
| **AAPL** | 27.44% | 28.17% | 0.79 |
| **JPM** | 18.99% | 27.59% | 0.50 |
| **GLD** | 9.30% | 15.82% | 0.26 |
| **XOM** | 10.33% | 24.86% | 0.21 |
| **TLT** | 3.83% | 15.10% | -0.09 |

### 4.3. Optimización Estocástica (Montecarlo: $10^8$ iteraciones)

| Métrica | Valor |
| :--- | :--- |
| **Retorno Esperado** | 18.78% |
| **Riesgo (Volatilidad)** | 15.93% |
| **Sharpe Ratio** | 0.86 |
| **Tiempo de Ejecución** | 20.81 segundos |

**Pesos Asignados:**
*   **AAPL:** 45.13%
*   **GLD:** 26.42%
*   **JPM:** 18.79%
*   **TLT:** 9.66%
*   **XOM:** 0.01%

### 4.4. Optimización Analítica (SciPy SLSQP / Ascenso de Gradiente)

| Métrica | Valor |
| :--- | :--- |
| **Retorno Esperado** | 18.64% |
| **Riesgo (Volatilidad)** | 15.77% |
| **Sharpe Ratio** | 0.86 |
| **Tiempo de Ejecución** | 0.00 segundos (8 iteraciones, 48 evaluaciones) |

**Pesos Óptimos Exactos:**
*   **AAPL:** 44.76%
*   **GLD:** 26.24%
*   **JPM:** 18.48%
*   **TLT:** 10.51%
*   **XOM:** 0.00%

_Conclusión del rendimiento algorítmico:_ La implementación analítica (SciPy) logró una pureza matemática superior, eliminando por completo el ruido estocástico (reduciendo XOM al 0.00% exacto) y reduciendo el riesgo total del portafolio, ejecutándose en una fracción de milisegundo frente a los casi 21 segundos de fuerza bruta.
