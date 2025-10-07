import json
from scipy import stats
from exp1.funcoes_relatorio_old import Dados, grafico

def main():
    # Ler os dados brutos
    with open('dados.json') as json_data:
        dados = json.load(json_data)

    # Análise para s(t)
    dados_st = Dados(
        medidas=dados['medidas_para_s(t)'],
        erro_instrumental_distancia_cm=0.05,
        erro_paralaxe_distancia_cm=0.15
    )

    # Cálculo para Tempo ao Quadrado
    tempo_quadrado = dados_st.tempos_s ** 2
    erro_total_tempo_quadrado = 2 * dados_st.tempos_s * dados_st.erro_total_tempo_s

    # Exibição média e desvio padrão
    dados_st.exibir_media_e_erro_tempos()


    # Regressão Linear para s(t)
    resultado_linearizacao = stats.linregress(tempo_quadrado, dados_st.distancias_cm)
    angular_st = resultado_linearizacao.slope
    linear_st = resultado_linearizacao.intercept
    erro_angular_st = resultado_linearizacao.stderr
    erro_linear_st = resultado_linearizacao.intercept_stderr

#     # Criação do Gráfico
#     grafico(
#         x=tempo_quadrado,
#         y=dados_st.distancias_cm,
#         erro_x=erro_total_tempo_quadrado,
#         erro_y=dados_st.erro_total_distancia_cm,
#         slope=angular_st,
#         intercept=linear_st,
#         erro_slope=erro_angular_st,
#         erro_intercept=erro_linear_st,
#         xlabel="$t^2$ ($s^2$)",
#         ylabel="$H$ ($cm$)",
#         title="Altura pelo Tempo ao Quadrado"
#     )
if __name__ == "__main__":
    main()