import matplotlib.pyplot as plt
import numpy as np
from scipy import stats


class Dados:
    """
    Classe para encapsular e calcular dados experimentais de distância e tempo.

    A classe recebe uma lista de medições, calcula as médias de tempo,
    e os erros estatísticos e totais para as medições de tempo e distância.

    Attributes:
        medidas (list): A lista de medições brutas.
        qtd_medidas (int): A quantidade de medições.
        distancias_cm (np.ndarray): Array com as distâncias em centímetros.
        tempos_s_lista (list): Lista de listas com as medições de tempo em segundos.
        tempos_s_mean (np.ndarray): Array com as médias dos tempos.
        erro_instrumental_tempo_s (np.ndarray): Erro instrumental do cronômetro.
        erro_estatistico_tempo_s (np.ndarray): Erro estatístico (desvio padrão da média) dos tempos.
        erro_total_tempo_s (np.ndarray): Erro total propagado para o tempo.
        erro_instrumental_distancia_cm (np.ndarray): Erro instrumental da régua.
        erro_paralaxe_distancia_cm (np.ndarray): Erro de paralaxe na medição da distância.
        erro_total_distancia_cm (np.ndarray): Erro total propagado para a distância.
    """
    def __init__(self, medidas, erro_instrumental_distancia_cm, erro_paralaxe_distancia_cm=0):
        """
        Inicializa o objeto Dados.

        Args:
            medidas (list): Lista de dicionários, onde cada dicionário contém
                            'distancia_cm' (float) e 'tempos_s' (list de floats).
            erro_instrumental_distancia_cm (float): O valor do erro instrumental
                                                     para a medição de distância.
            erro_paralaxe_distancia_cm (float, optional): O valor do erro de paralaxe.
                                                          Default é 0.
        """
        self.medidas = medidas
        self.qtd_medidas = len(medidas)
        self.distancias_cm = np.array([m['distancia_cm'] for m in medidas])
        self.tempos_s = np.array([np.mean(t) for t in [m['tempos_s'] for m in medidas]])
        
        # Erros
        self.erro_instrumental_tempo_s = np.full(self.qtd_medidas, 0.001)
        self.erro_estatistico_tempo_s = np.array([stats.sem(t) for t in [m['tempos_s'] for m in medidas]])
        self.erro_total_tempo_s = np.sqrt(self.erro_instrumental_tempo_s**2 + self.erro_estatistico_tempo_s**2)
        
        self.erro_instrumental_distancia_cm = np.full(self.qtd_medidas, erro_instrumental_distancia_cm)
        self.erro_paralaxe_distancia_cm = np.full(self.qtd_medidas, erro_paralaxe_distancia_cm)
        self.erro_total_distancia_cm = np.sqrt(self.erro_instrumental_distancia_cm**2 + self.erro_paralaxe_distancia_cm**2)

    def exibir_media_e_erro_tempos(self):
        """Exibe as médias dos tempos e seus erros totais correspondentes.

        Este método itera sobre as médias de tempo calculadas (`self.tempos_s`)
        e seus respectivos erros totais (`self.erro_total_tempo_s`). Para cada
        par de valores, determina o número correto de casas decimais com base
        no primeiro dígito significativo do erro, usando a função auxiliar
        `encontrar_casa_decimal`.

        A média e o erro são então arredondados para essa precisão e exibidos
        na saída padrão.
        """

        for media, erro in zip(self.tempos_s, self.erro_total_tempo_s):
            casa_decimal = encontrar_casa_decimal(erro)
            print(round(media, casa_decimal), round(erro, casa_decimal))

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
    
    # Formatando a legenda com valores arredondados para melhor visualização
    casas_decimais_slope = encontrar_casa_decimal(erro_slope)
    casas_decimais_intercept = encontrar_casa_decimal(erro_intercept)
    
    slope_rounded = round(slope, casas_decimais_slope)
    erro_slope_rounded = round(erro_slope, casas_decimais_slope)
    intercept_rounded = round(intercept, casas_decimais_intercept)
    erro_intercept_rounded = round(erro_intercept, casas_decimais_intercept)
    
    # A incerteza do ajuste pode ser estimada pelo erro padrão da regressão
    # Para simplificar, vamos usar o erro dos pontos por enquanto.
    # Idealmente, os erros no slope e intercept deveriam ser calculados.
    
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

