# Mission Control AI - Atlas Test Gamma 
**Componente Curricular:** Pensamento Computacional e Automação com Python  
**Equipe Responsável:** Equipe Hermes(Composta por Pedro Lemgruber,Gustavo Pola e Caio Ceschini)

## Visão Geral do Projeto
O **Mission Control AI** é um sistema inteligente desenvolvido em Python puro para simular e monitorar os sinais vitais e estruturais de uma missão espacial experimental. O programa analisa dados telemétricos simulados de múltiplos ciclos operacionais, calcula índices de risco em tempo real, gera diagnósticos dinâmicos e emite recomendações acionáveis, culminando em um relatório estatístico completo sobre o estado geral da missão.

---

##  Arquitetura de Dados

O núcleo de dados do sistema baseia-se em estruturas nativas e multidimensionais do Python:

1. **Matriz de Telemetria (`dados_missao`):** Uma matriz bidimensional ($M \times N$) onde cada linha representa um **Ciclo de Monitoramento** temporal e cada coluna representa uma métrica específica coletada.
2. **Vetor de Identificação (`areas_monitoradas`):** Uma lista indexada de strings mapeada diretamente com a ordem posicional das colunas da matriz para garantir a correspondência dos dados.

### Mapeamento das Colunas da Matriz
| Índice da Coluna | Métrica Monitorada | Unidade de Medida |
| :---: | :--- | :---: |
| `[0]` | Temperatura Interna | °C |
| `[1]` | Comunicação com a Base | % |
| `[2]` | Sistema de Energia (Bateria) | % |
| `[3]` | Suporte de Oxigênio | % |
| `[4]` | Estabilidade Operacional | % |

---

## Processo Lógico e Regras de Negócio

A inteligência de tomada de decisão do sistema fundamenta-se estritamente em **regras lógicas de limiares condicionais**, sem dependências de pacotes externos. O processamento divide-se em três etapas:

### 1. Análise Individual de Parâmetros
Cada função de monitoramento individual (`analisar_temperatura`, `analisar_comunicacao`, etc.) recebe o valor numérico bruto e aplica condições para retornar uma tupla com a seguinte assinatura: `(pontos_de_risco, "CLASSIFICAÇÃO", "Mensagem de Alerta")`.

As faixas de corte adotadas obedecem aos seguintes critérios de pontuação ($0$ para normalidade, $1$ para atenção e $2$ para cenários críticos):

* **Temperatura:** * $< 18°C$ ou entre $31°C$ e $35°C$ $\rightarrow$ **1 ponto** (Atenção)
    * Entre $18°C$ e $30°C$ $\rightarrow$ **0 pontos** (Normal)
    * $> 35°C$ $\rightarrow$ **2 pontos** (Crítico)
* **Comunicação / Bateria / Oxigênio / Estabilidade:** * $\ge$ Limiar Ideal (Variável por área) $\rightarrow$ **0 pontos** (Normal)
    * Limiar Intermediário $\rightarrow$ **1 ponto** (Atenção)
    * $<$ Limiar Crítico $\rightarrow$ **2 pontos** (Crítico)

### 2. Consolidação de Riscos por Ciclo
A pontuação de risco acumulada de um único ciclo é obtida pela somatória simples dos pontos de risco individuais atribuídos a cada uma das 5 métricas:

$$\text{Risco Total do Ciclo} = \sum (\text{Pontos de Risco Individual})$$

A classificação do estado da missão por ciclo obedece às faixas consolidadas abaixo:
* **De 0 a 2 pontos:** `MISSÃO ESTÁVEL`
* **De 3 a 5 pontos:** `MISSÃO EM ATENÇÃO`
* **De 6 a 10 pontos:** `MISSÃO CRÍTICA`

### 3. Mecanismo de Recomendações Dinâmicas e Cumulativas
Diferente de estruturas rígidas com `if/elif`, a função `gerar_recomendacao` utiliza uma abordagem de **pilha cumulativa (`list.append()`)**. Ela varre todas as variáveis simultaneamente e concatena todas as ações corretivas necessárias em uma única mensagem de saída formatada por quebras de linha (`\n`), permitindo alertar a tripulação sobre múltiplos problemas de engenharia ao mesmo tempo.

---

##  Processamento Estatístico Final (`gerar_relatorio_final`)

Ao término da varredura ciclo a ciclo, o sistema processa a matriz global para extrair relatórios macroscópicos:

* **Cálculo de Médias Aritméticas:** Avalia o comportamento médio a longo prazo de cada parâmetro.
* **Tendência da Missão:** Aplica um algoritmo comparativo entre o risco do ciclo inicial ($t_0$) e o ciclo final ($t_n$). Se o risco final for superior ao inicial, infere-se uma **tendência de piora**; caso contrário, há estabilização ou melhora.
* **Identificação da Área Mais Afetada:** Acumula os pontos históricos penalizados por coluna. Utilizando funções nativas de alta performance (`max()` e `.index()`), identifica qual sistema de engenharia representou a maior dor de cabeça para a missão ao longo do tempo.
* **Algoritmo de Risco Sentinela:** Identifica o ciclo mais crítico inicializando o rastreador em `-1`. Isto garante que mesmo que ocorra uma simulação perfeita de nível $0$, a rotina capture e indique o primeiro ciclo de varredura como ponto de partida referencial.

---
