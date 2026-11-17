# Portfolio Theory Proyect

## 1. Hipotesis & Abstract

Este proyecto implementa y comprueba empiricamente los principios de la Teoria Moderna de Cartas (MPT) de Harry Markowitz.

La hipotesis es que la diversificacion estrategica mediante el analisis de la matriz de covarianza permite aislar el riesgo no sistematico de los activos. Por lo tanto, un algoritmo de optimizacion lograra un ratio de sharpe superior al de cualquier cartera de activos aislados (en adelante SSP, single stock portfolio), maximizando el exceso de retorno sobre una tasa de libre de riesgo dada.

## 2. Universo de activos

AAPL: Tecnologia
JPM: Bancos
XOM: Energia
TLT: Bonos del tesoro
GLD: Oro

Se toma un risk free rate de 5.1% anual, al dia de 17/11/2026.

Fuentes de datos: precios de cierre ajustados (Adj Close)

## 3. Metodologia

Se divide en tres fases de comprobacion secuencial

3.1. Grupo de control (SSP):
Calculo del rendimiento volatilidad y ratio de sharpe asumientdo una asignacion del 100% a cada activo individualmente.

3.2. Simulacion de Montecarlo
Generacion de un espacio de soluciones de n portafolios aleatorios mediante operaciones tensoriales permitiendo solamente compras.
Se utiliza n = k ^ (N - 1),
donde:
k es la resolucion de la busqueda
N es la cantidad de activos

En este caso especifico se toma:
k=100
N=5
Entonces n=10^8

3.3. Optimizacion analitica

3.3.1 Ascenso de gradiente
Uso de geometria diferencial via ascenso del gradiente para hallar maximos atado a las restricciones (solo se permiten compras, los pesos suman 100%) 

3.3.2 Forma cerrada de cartera tangente (Con ventas en corto permitidas)
Forma cerrada de la cartera optima, solamente atada a la restriccion que los pesos sumen 100%:
	
$$
\mathbf{w}_T = \frac{\boldsymbol{\Sigma}^{-1} (\boldsymbol{\mu} - r_f \mathbf{1})}{\mathbf{1}^T \boldsymbol{\Sigma}^{-1} (\boldsymbol{\mu} - r_f \mathbf{1})}
$$


## 4. Resulados

### 4.1. Matriz de covarianza hallada

| Ticker | AAPL | GLD | JPM | TLT | XOM |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **AAPL** | 0.079357 | 0.002267 | 0.030720 | -0.007064 | 0.021890 |
| **GLD** | 0.002267 | 0.025017 | -0.002383 | 0.005184 | 0.002407 |
| **JPM** | 0.030720 | -0.002383 | 0.076139 | -0.016026 | 0.037309 |
| **TLT** | -0.007064 | 0.005184 | -0.016026 | 0.022791 | -0.010961 |
| **XOM** | 0.021890 | 0.002407 | 0.037309 | -0.010961 | 0.061818 |

### 4.2. Portfolios SSP

| Portfolio | Expected Returns (Anual) | Risk (Riesgo) | Sharpe Ratio |
| :--- | :--- | :--- | :--- |
| **AAPL** | 27.44% | 28.17% | 0.09 |
| **XOM** | 9.30% | 15.82% | -0.23 |
| **JPM** | 18.99% | 27.59% | 0.00 |
| **TLT** | 3.83% | 15.10% | -0.30 |
| **GLD** | 10.33% | 24.86% | -0.10 |

### 4.3. Portafolio hallado con Montecarlo

| Métrica | Valor |
| :--- | :--- |
| **Retorno esperado** | 18.64% anual |
| **Volatilidad** | 15.77% |
| **Sharpe Ratio** | 0.86 |

| Activo | Peso |
| :--- | :--- |
| **AAPL** | 44.94% |
| **XOM** | 25.56% |
| **JPM** | 18.46% |
| **TLT** | 11.03% |
| **GLD** | 0.00% |

### 4.4. Portafolio hallado con metodo ascenso gradiente

