# src/main.py
import os
import sys

# Ajuste de path para importação local
sys.path.append(os.path.dirname(__file__))

from graph import Graph
from aco import AntColony
import utils

# ==============================================================================
# CONFIGURAÇÃO DE CAMINHOS
# ==============================================================================
DIRETORIO_SRC = os.path.dirname(os.path.abspath(__file__))
DIRETORIO_PROJETO = os.path.dirname(DIRETORIO_SRC)
ARQUIVO_ENTRADA = os.path.join(DIRETORIO_PROJETO, 'input', 'cidades.txt')
ARQUIVO_SAIDA   = os.path.join(DIRETORIO_PROJETO, 'output', 'resultado.txt')

# ==============================================================================
# PARÂMETROS DO ACO
# ==============================================================================
NUM_FORMIGAS    = 30     # População
NUM_ITERACOES   = 100    # Gerações
ALFA            = 1.0    # Peso do Feromônio
BETA            = 3.0    # Peso da Visibilidade
EVAPORACAO      = 0.5    # Taxa de evaporação
INTENSIDADE_Q   = 100.0  # Depósito de feromônio

def main():
    print("=== Trabalho 02: TSP com Colônia de Formigas (Snapshot + Convergência) ===")
    
    # 1. Validação
    if not os.path.exists(ARQUIVO_ENTRADA):
        print(f"[ERRO] Arquivo não encontrado: {ARQUIVO_ENTRADA}")
        return

    # 2. Setup
    cidades = utils.ler_cidades(ARQUIVO_ENTRADA)
    grafo = Graph(cidades)
    
    aco = AntColony(
        graph=grafo, 
        num_formigas=NUM_FORMIGAS,
        alfa=ALFA, 
        beta=BETA, 
        evaporacao=EVAPORACAO, 
        q=INTENSIDADE_Q
    )
    
    # 3. Execução
    # (Os snapshots serão salvos automaticamente na pasta output durante a execução)
    aco.run(NUM_ITERACOES)
    
    # 4. Resultados Finais
    os.makedirs(os.path.dirname(ARQUIVO_SAIDA), exist_ok=True)
    
    utils.salvar_resultados(
        ARQUIVO_SAIDA, 
        aco.melhor_rota_global, 
        aco.melhor_distancia_global, 
        grafo.cidades
    )
    
    print("\nGerando gráfico final de convergência...")
    utils.plotar_graficos(
        grafo, 
        aco.melhor_rota_global, 
        aco.historico_melhor,
        aco.historico_media  # Passando o histórico da média
    )

if __name__ == "__main__":
    main()