# src/utils.py
import matplotlib.pyplot as plt

def ler_cidades(caminho_arquivo):
    """
    Lê o arquivo de texto e converte para estrutura de dados.
    Formato esperado: ID X Y
    Requisito: Leitura de arquivo de texto.
    """
    cidades = []
    try:
        with open(caminho_arquivo, 'r') as f:
            for linha in f:
                partes = linha.strip().split()
                if len(partes) >= 3:
                    cidades.append({
                        'id': partes[0],
                        'x': float(partes[1]),
                        'y': float(partes[2])
                    })
        print(f"--> Leitura concluída: {len(cidades)} cidades carregadas.")
        return cidades
    except FileNotFoundError:
        print(f"Erro: Arquivo '{caminho_arquivo}' não encontrado.")
        exit()

def salvar_resultados(caminho_saida, melhor_rota, melhor_distancia, cidades):
    """
    Salva os resultados em arquivo txt.
    Requisito: Saída em arquivo de texto.
    """
    try:
        with open(caminho_saida, 'w') as f:
            f.write("RELATORIO FINAL - OTIMIZACAO POR COLONIA DE FORMIGAS\n")
            f.write("====================================================\n")
            f.write(f"Melhor Distancia Encontrada: {melhor_distancia:.4f}\n")
            f.write("====================================================\n")
            f.write("Sequencia de Cidades (Rota):\n")
            
            # Converte índices da rota para os IDs originais das cidades
            rota_ids = [cidades[i]['id'] for i in melhor_rota]
            f.write(" -> ".join(rota_ids))
            f.write("\n")
            
        print(f"--> Resultados salvos com sucesso em: {caminho_saida}")
    except Exception as e:
        print(f"Erro ao salvar arquivo: {e}")

def plotar_graficos(graph, melhor_rota, historico_convergencia):
    """
    Gera os gráficos solicitados no artigo (Rota e Convergência).
    """
    # Prepara dados para o plot da rota (precisa fechar o ciclo adicionando o início ao fim)
    rota_plot = melhor_rota + [melhor_rota[0]]
    x = [graph.cidades[i]['x'] for i in rota_plot]
    y = [graph.cidades[i]['y'] for i in rota_plot]
    
    plt.figure(figsize=(14, 6))
    
    # Gráfico 1: Mapa das Cidades e Rota
    plt.subplot(1, 2, 1)
    plt.plot(x, y, 'o-r', markersize=8, linewidth=1.5) # Rota em vermelho
    plt.title('Melhor Rota Encontrada')
    plt.xlabel('Coordenada X')
    plt.ylabel('Coordenada Y')
    
    # Anota o ID das cidades no gráfico
    for i, c in enumerate(graph.cidades):
        plt.text(c['x'], c['y'], f" {c['id']}", fontsize=10, color='blue')

    # Gráfico 2: Curva de Convergência
    plt.subplot(1, 2, 2)
    plt.plot(historico_convergencia, color='green')
    plt.title('Convergência (Evolução da Melhor Distância)')
    plt.xlabel('Iterações (Gerações)')
    plt.ylabel('Distância Total')
    plt.grid(True, linestyle='--', alpha=0.7)
    
    plt.tight_layout()
    plt.savefig('grafico_resultado.png') # Salva imagem para o artigo
    plt.show()