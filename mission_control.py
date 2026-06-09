dados_missao = [
    [19, 95, 89, 99, 92],
    [25, 90, 74, 96, 88],
    [30, 84, 52, 87, 72],
    [37, 50, 40, 82, 53],
    [32, 30, 15, 75, 37],
    [38, 50, 20, 80, 46]
]

areas_monitoradas = [
    "Temperatura interna",
    "Comunicação com a base",
    "Sistema de energia",
    "Suporte de oxigênio",
    "Estabilidade operacional"
]


# --- FUNÇÕES DE ANÁLISE INDIVIDUAL ---
# Cada função retorna: (pontos_de_risco, "CLASSIFICAÇÃO", "Mensagem de Alerta")

def analisar_temperatura(temp):
    if temp < 18:
        return 1, "ATENÇÃO", "Temperatura baixa"
    elif 18 <= temp <= 30:
        return 0, "NORMAL", "Temperatura estável"
    elif 30 < temp <= 35:
        return 1, "ATENÇÃO", "Temperatura elevada"
    else:
        return 2, "CRÍTICO", "Risco de superaquecimento"


def analisar_comunicacao(com):
    if com < 30:
        return 2, "CRÍTICO", "Comunicação com a base em nível crítico"
    elif 30 <= com <= 59:
        return 1, "ATENÇÃO", "Comunicação instável"
    else:
        return 0, "NORMAL", "Comunicação estável"


def analisar_bateria(bat):
    if bat < 20:
        return 2, "CRÍTICO", "Bateria em nível crítico"
    elif 20 <= bat <= 49:
        return 1, "ATENÇÃO", "Bateria abaixo do recomendado"
    else:
        return 0, "NORMAL", "Bateria estável"


def analisar_oxigenio(oxi):
    if oxi < 80:
        return 2, "CRÍTICO", "Oxigênio em nível crítico"
    elif 80 <= oxi <= 89:
        return 1, "ATENÇÃO", "Oxigênio abaixo do ideal"
    else:
        return 0, "NORMAL", "Oxigênio adequado"


def analisar_estabilidade(est):
    if est < 40:
        return 2, "CRÍTICO", "Estabilidade operacional crítica"
    elif 40 <= est <= 69:
        return 1, "ATENÇÃO", "Estabilidade operacional reduzida"
    else:
        return 0, "NORMAL", "Estabilidade operacional adequada"


# --- FUNÇÕES DE SÍNTESE E MÉTRICAS CONSOLIDADAS ---

def calcular_risco_ciclo(ciclo):
    p_temp = analisar_temperatura(ciclo[0])[0]
    p_com = analisar_comunicacao(ciclo[1])[0]
    p_bat = analisar_bateria(ciclo[2])[0]
    p_oxi = analisar_oxigenio(ciclo[3])[0]
    p_est = analisar_estabilidade(ciclo[4])[0]
    return p_temp + p_com + p_bat + p_oxi + p_est


def classificar_ciclo(pontuacao):
    if 0 <= pontuacao <= 2:
        return "MISSÃO ESTÁVEL"
    elif 3 <= pontuacao <= 5:
        return "MISSÃO EM ATENÇÃO"
    else:
        return "MISSÃO CRÍTICA"


def analisar_tendencia(ciclos):
    risco_inicial = calcular_risco_ciclo(ciclos[0])
    risco_final = calcular_risco_ciclo(ciclos[-1])

    if risco_final > risco_inicial:
        return "A missão apresentou tendência de piora."
    elif risco_final < risco_inicial:
        return "A missão apresentou tendência de melhora."
    else:
        return "A missão permaneceu estável em relação ao início."


def identificar_area_mais_afetada(ciclos):
    pontos_por_area = [0, 0, 0, 0, 0]

    for ciclo in ciclos:
        pontos_por_area[0] += analisar_temperatura(ciclo[0])[0]
        pontos_por_area[1] += analisar_comunicacao(ciclo[1])[0]
        pontos_por_area[2] += analisar_bateria(ciclo[2])[0]
        pontos_por_area[3] += analisar_oxigenio(ciclo[3])[0]
        pontos_por_area[4] += analisar_estabilidade(ciclo[4])[0]

    maior_pontuacao = max(pontos_por_area)
    indice_maior = pontos_por_area.index(maior_pontuacao)

    return areas_monitoradas[indice_maior], pontos_por_area


def gerar_recomendacao(pontuacao_ciclo, temp, com, bat, oxi, est):
    recomendacoes=[]
    if pontuacao_ciclo == 0:
        return "Manter operação normal e continuar monitoramento."

    elif pontuacao_ciclo == 10:
        return "Ativar modo de segurança e priorizar suporte à vida, energia e comunicação."

    if analisar_temperatura(temp)[0] == 2: recomendacoes.append( "Verificar controle térmico da missão.")
    if analisar_comunicacao(com)[0] == 2:  recomendacoes.append( "Tentar restabelecer contato com a base.")
    if analisar_bateria(bat)[0] == 2:      recomendacoes.append( "Ativar modo de economia de energia.")
    if analisar_oxigenio(oxi)[0] == 2:     recomendacoes.append( "Acionar protocolo de suporte à vida.")
    if analisar_estabilidade(est)[0] == 2: recomendacoes.append( "Reduzir operações não essenciais.")

    if analisar_temperatura(temp)[0] == 1: recomendacoes.append( "Temperatura em niveis de atenção.")
    if analisar_comunicacao(com)[0] == 1:  recomendacoes.append( "Atenção, comunicação instável.")
    if analisar_bateria(bat)[0] == 1:      recomendacoes.append( "Niveis de energia em estado de atenção.")
    if analisar_oxigenio(oxi)[0] == 1:     recomendacoes.append( "Niveís de oxigenio em estado de atenção.")
    if analisar_estabilidade(est)[0] == 1: recomendacoes.append( "Atenção, nave apresentando instabilidade.")
    if 3 <= pontuacao_ciclo <= 5:
        return "Monitorar sistemas em atenção e preparar plano de contingência."



def gerar_relatorio_final(ciclos):
    total_ciclos = len(ciclos)
    soma_temp = soma_com = soma_bat = soma_oxi = soma_est = 0
    soma_risco_total = 0
    ciclos_criticos = 0

    maior_risco = -1
    ciclo_mais_critico = 0

    for idx, ciclo in enumerate(ciclos):
        soma_temp += ciclo[0]
        soma_com += ciclo[1]
        soma_bat += ciclo[2]
        soma_oxi += ciclo[3]
        soma_est += ciclo[4]

        risco = calcular_risco_ciclo(ciclo)
        soma_risco_total += risco

        if classificar_ciclo(risco) == "MISSÃO CRÍTICA":
            ciclos_criticos += 1

        if risco > maior_risco:
            maior_risco = risco
            ciclo_mais_critico = idx + 1

    area_critica, lista_pontos = identificar_area_mais_afetada(ciclos)
    risco_medio = soma_risco_total / total_ciclos
    classificacao_final = classificar_ciclo(round(risco_medio))

    print("\n============================================================")
    print("RELATÓRIO FINAL DA MISSÃO")
    print("============================================================")
    print("Missão: Atlas Test Gamma")
    print("Equipe: Equipe Hermes\n")
    print(f"Quantidade de ciclos analisados: {total_ciclos}\n")
    print(f"Média de temperatura: {soma_temp / total_ciclos:.2f} °C")
    print(f"Média de comunicação: {soma_com / total_ciclos:.2f}%")
    print(f"Média de bateria: {soma_bat / total_ciclos:.2f}%")
    print(f"Média de oxigênio: {soma_oxi / total_ciclos:.2f}%")
    print(f"Média de estabilidade: {soma_est / total_ciclos:.2f}%\n")
    print(f"Ciclo mais crítico: Ciclo {ciclo_mais_critico}")
    print(f"Maior pontuação de risco: {maior_risco}")
    print(f"Risco médio da missão: {risco_medio:.2f}")
    print(f"Quantidade de ciclos críticos: {ciclos_criticos}\n")
    print("Tendência da missão:")
    print(analisar_tendencia(ciclos) + "\n")
    print("Pontuação acumulada por área:")
    for i in range(5):
        print(f" {areas_monitoradas[i]}: {lista_pontos[i]} pontos")
    print(f"\nÁrea mais afetada:\n {area_critica}")
    print(f"\nClassificação final da missão:\n {classificacao_final}")


# ==============================================================================
# EXECUÇÃO DO FLUXO PRINCIPAL (SAÍDA NO TERMINAL)
# ==============================================================================

print("============================================================")
print("MISSION CONTROL AI")
print("============================================================")
print("Missão: Atlas Test Gamma")
print("Equipe: Equipe Hermes")
print(f"Quantidade de ciclos analisados: {len(dados_missao)}")
print("============================================================")

for i, ciclo in enumerate(dados_missao):
    print(f"\nCICLO {i + 1}")

    p_temp, status_temp, msg_temp = analisar_temperatura(ciclo[0])
    p_com, status_com, msg_com = analisar_comunicacao(ciclo[1])
    p_bat, status_bat, msg_bat = analisar_bateria(ciclo[2])
    p_oxi, status_oxi, msg_oxi = analisar_oxigenio(ciclo[3])
    p_est, status_est, msg_est = analisar_estabilidade(ciclo[4])

    risco_total = p_temp + p_com + p_bat + p_oxi + p_est
    classificacao = classificar_ciclo(risco_total)

    recomendacao = gerar_recomendacao(risco_total, ciclo[0], ciclo[1], ciclo[2], ciclo[3], ciclo[4])

    print(f"Temperatura: {ciclo[0]} °C | {status_temp} | {msg_temp}")
    print(f"Comunicação: {ciclo[1]}% | {status_com} | {msg_com}")
    print(f"Bateria: {ciclo[2]}% | {status_bat} | {msg_bat}")
    print(f"Oxigênio: {ciclo[3]}% | {status_oxi} | {msg_oxi}")
    print(f"Estabilidade: {ciclo[4]}% | {status_est} | {msg_est}")
    print(f"Pontuação de risco do ciclo: {risco_total}")
    print(f"Classificação do ciclo: {classificacao}")
    print(f"Recomendação: {recomendacao}")

gerar_relatorio_final(dados_missao)