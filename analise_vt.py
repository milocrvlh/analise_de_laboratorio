import json
from scipy import stats
from funcoes_relatorio import Dados, grafico

def main():
    # Ler os dados brutos
    with open('dados.json') as json_data:
        dados = json.load(json_data)

    # Análise para s(t)
    dados_vt = Dados(
        medidas=dados['medidas_para_v(t)'],
        erro_instrumental_distancia_cm=0.05,
        erro_paralaxe_distancia_cm=0.15
    )
    dados_vt.exibir_media_e_erro_tempos()


if __name__ == "__main__":
    main()