import matplotlib.pyplot as plt
import numpy as np
from scipy import stats


def encontrar_casa_decimal(numero):
    """
    Encontra a posição da primeira casa decimal significativa de um número.

    Esta função é útil para determinar o número de casas decimais a serem
    usadas ao arredondar um valor com base em sua incerteza.

    Args:
        numero (float): O número a ser analisado.

    Returns:
        int: A posição da primeira casa decimal significativa.
             Retorna 0 se o número for 0 ou maior ou igual a 1.

    Example:
        >>> encontrar_casa_decimal(0.05)
        2
        >>> encontrar_casa_decimal(0.345)
        1
        >>> encontrar_casa_decimal(1.2)
        0
    """
    if numero == 0 or abs(numero) >= 1:
        return 0

    n = abs(numero)
    
    posicao = abs(np.floor(np.log10(n)))
    
    return int(posicao)


def grafico(x, y, erro_x, erro_y, slope, erro_slope, intercept, erro_intercept, xlabel, ylabel, title):
    """
    Gera um gráfico de dispersão com barras de erro e uma reta de ajuste.

    Args:
        x (np.ndarray): Valores do eixo x.
        y (np.ndarray): Valores do eixo y.
        erro_x (np.ndarray): Erros associados aos valores de x.
        erro_y (np.ndarray): Erros associados aos valores de y.
        slope (float): Coeficiente angular da reta de ajuste.
        erro_slope (float): Erro do coeficiente angular da reta de ajuste
        intercept (float): Intercepto da reta de ajuste.
        erro_intercept (float): Erro do intercepto da reta de ajuste.
        xlabel (str): Rótulo do eixo x.
        ylabel (str): Rótulo do eixo y.
        title (str): Título do gráfico.
    """
    plt.rcParams['text.usetex'] = True
    plt.rcParams['text.latex.preamble'] = r'\usepackage{amsmath}'
    
    casas_decimais_slope = encontrar_casa_decimal(erro_slope)
    casas_decimais_intercept = encontrar_casa_decimal(erro_intercept)
    
    slope_rounded = round(slope, casas_decimais_slope)
    erro_slope_rounded = round(erro_slope, casas_decimais_slope)
    intercept_rounded = round(intercept, casas_decimais_intercept)
    erro_intercept_rounded = round(erro_intercept, casas_decimais_intercept)
    
    
    plt.plot(x, slope * x + intercept, color='red', label=f'Reta de Ajuste: $y = ({slope_rounded}\pm{erro_slope_rounded}) \cdot x + ({intercept_rounded}\pm{erro_intercept_rounded})$')
    plt.errorbar(x, y,
                        xerr=erro_x, yerr=erro_y,
                        fmt='o', color='black', ecolor='gray', capsize=2, zorder=10, label='Pontos experimentais')
    plt.legend()
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.grid(True)
    plt.show()

