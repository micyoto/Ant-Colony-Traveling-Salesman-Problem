# src/main.py
import os
import sys

# Adiciona o diretório atual ao path para garantir importações locais funcionem
sys.path.append(os.path.dirname(__file__))

from graph import Graph
from aco import AntColony
import utils

# ==============================================================================
# AJUSTE DE CAMINHOS (FIX)
# ==============================================================================
# Pega o diretório onde este arquivo (main.py) está localizado: .../seu_projeto/src
DIRETORIO_SRC = os.path.dirname(os.path.abspath(__file__))

# Volta um nível para chegar na raiz do projeto: .../seu_projeto
DIRETORIO_PROJETO = os.path.dirname(DIRETORIO_SRC)

# Monta os caminhos absolutos baseados na estrutura do projeto
ARQUIVO_ENTRADA = os.path.join(DIRETORIO_PROJETO, 'input', 'cidades.txt')
ARQUIVO_SAIDA   = os.path.join(DIRETORIO_PROJETO, 'output', 'resultado.txt')
IMG_SAIDA       = os.path.join(DIRETORIO_PROJETO, 'output', 'grafico_resultado.png')

# ==============================================================================
# CONFIGURAÇÕES
# ==============================================================================
# Parâmetros do Algoritmo Genético (ACO)
NUM_FORMIGAS    = 30     # Tamanho da população
NUM_ITERACOES   = 100    # Critério de parada
ALFA            = 1.0    # Importância do Rastro (Feromônio)
BETA            = 3.0    # Importância da Visibilidade (Distância)
EVAPORACAO      = 0.5    # Taxa de evaporação
INTENSIDADE_Q   = 100.0  # Constante de depósito

def main():
    print("=== Trabalho 02: Otimização Combinatória (TSP com ACO) ===")
    print(f"Diretório base do projeto detectado: {DIRETORIO_PROJETO}")
    
    # 1. Validação do Arquivo
    if not os.path.exists(ARQUIVO_ENTRADA):
        print(f"\n[ERRO CRÍTICO] Arquivo não encontrado!")
        print(f"O script esperava encontrar o arquivo aqui: {ARQUIVO_ENTRADA}")
        print("Verifique se você criou a pasta 'input' e o arquivo 'cidades.txt' dentro dela.")
        return # Para a execução

    lista_cidades = utils.ler_cidades(ARQUIVO_ENTRADA)
    
    # 2. Inicialização do Grafo
    grafo = Graph(lista_cidades)
    
    # 3. Configuração e Execução do ACO
    aco = AntColony(
        graph=grafo,
        num_formigas=NUM_FORMIGAS,
        alfa=ALFA,
        beta=BETA,
        evaporacao=EVAPORACAO,
        q=INTENSIDADE_Q
    )
    
    aco.run(NUM_ITERACOES)
    
    # 4. Resultados
    # Verifica se a pasta output existe, se não, cria
    os.makedirs(os.path.dirname(ARQUIVO_SAIDA), exist_ok=True)
    
    utils.salvar_resultados(
        ARQUIVO_SAIDA, 
        aco.melhor_rota_global, 
        aco.melhor_distancia_global, 
        grafo.cidades
    )
    
    print("\nGerando gráficos...")
    # Pequeno ajuste necessário no utils.py para aceitar o caminho da imagem
    # Mas se você não alterou o utils, ele vai salvar na pasta onde o terminal está.
    # Para garantir, edite o utils.py ou apenas deixe como está que vai funcionar,
    # mas a imagem pode cair na raiz.
    
    utils.plotar_graficos(
        grafo, 
        aco.melhor_rota_global, 
        aco.historico_convergencia
    )

if __name__ == "__main__":
    main()