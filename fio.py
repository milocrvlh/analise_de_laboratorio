import numpy as np
from scipy import stats
from funcoes_relatorio import grafico

def corda(valor_altura_fio, valores_diametro, valores_diferenca_dilatacao):
    # massa
    massa1_g, massa2_g, massa3_g, massa4_g, massa5_g = (350.96, 349.98, 350.88, 350.09, 340.85)
    massas_acumulados_g =np.array([
        massa1_g,
        massa1_g + massa2_g,
        massa1_g + massa2_g + massa3_g,
        massa1_g + massa2_g + massa3_g + massa4_g,
        massa1_g + massa2_g+ massa3_g + massa4_g + massa5_g
    ])
    massas_acumulados_kg = massas_acumulados_g/1000

    erro_massa_g = np.full(len(massas_acumulados_g), 0.1)
    erro_massa_kg = erro_massa_g/1000

    # Gravidade
    g = 9.80665

    # Peso  -------------- F
    pesos_acumulados_N = g * massas_acumulados_kg
    erro_pesos_acumulados_N = g * erro_massa_kg

    # Altura do Fio ------------- L0
    altura_fio_mm =  valor_altura_fio
    erro_altura_fio_mm = 0.5

    # Diãmetro do Fio

    diametro_fio_mm = np.array(valores_diametro)
    media_diametro_fio_mm = np.mean(diametro_fio_mm)
    erro_diametro_fio_mm = np.hypot(0.01, stats.sem(diametro_fio_mm))

    diametro_fio_m = media_diametro_fio_mm / 1000
    erro_diametro_fio_m = erro_diametro_fio_mm / 1000

    # Raio 

    raio_fio_m = diametro_fio_m / 2
    erro_raio_fio = erro_diametro_fio_m / 2

    # Seção Reta do Fio -- A
    area_secao_reta_m2 = np.pi * raio_fio_m ** 2
    erro_area_secao_reta_m2 = 2 * np.pi * raio_fio_m * erro_raio_fio


    # Diferença de comprimento 
    delta_l_mm = np.array(valores_diferenca_dilatacao)
    erro_delta_l_mm = np.full(len(delta_l_mm), 0.005)

    delta_l_lo = delta_l_mm  / altura_fio_mm
    erro_delta_l_lo = np.hypot(erro_delta_l_mm/altura_fio_mm, (delta_l_mm*erro_altura_fio_mm)/altura_fio_mm**2)

    resultado_linearizacao = stats.linregress(pesos_acumulados_N, delta_l_lo)
    angular_st = resultado_linearizacao.slope
    linear_st = resultado_linearizacao.intercept
    erro_angular_st = resultado_linearizacao.stderr
    erro_linear_st = resultado_linearizacao.intercept_stderr


    x = pesos_acumulados_N
    y = delta_l_lo
    erro_x = erro_pesos_acumulados_N
    erro_y =erro_delta_l_lo

    # Criação do Gráfico
    grafico(
        x=x,
        y=y,
        erro_x=erro_x,
        erro_y=erro_y,
        slope=angular_st,
        intercept=linear_st,
        erro_slope=erro_angular_st,
        erro_intercept=erro_linear_st,
        xlabel="$P (N)$",
        ylabel="$\\frac{{\\Delta L}}{{L_0}}$",
        title="Deformação Unitária pelo Peso"
    )

    print(f"A área da seção reta em m^2 é {area_secao_reta_m2} com erro de {erro_area_secao_reta_m2}")

# fio A
corda(
    valor_altura_fio=435.0,
    valores_diametro=[0.31,0.29,0.30,0.31,0.31,0.31,0.31,0.31,0.32,0.31,0.31,0.30,0.31,0.33,0.31,0.33,0.31,0.31],
    valores_diferenca_dilatacao=[0.110, 0.220, 0.330, 0.440, 0.560]
)

# fio B
# corda(
#     valor_altura_fio=423.0,
#     valores_diametro=[0.54, 0.53, 0.54, 0.535, 0.535],
#     valores_diferenca_dilatacao=None
# )