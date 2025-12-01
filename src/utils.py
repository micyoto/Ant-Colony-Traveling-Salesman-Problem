# src/utils.py
import matplotlib.pyplot as plt
import os

def ler_cidades(caminho_arquivo):
    """Lê o arquivo de texto e converte para lista de cidades."""
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
    """Salva o relatório final em txt."""
    try:
        with open(caminho_saida, 'w') as f:
            f.write("RELATORIO FINAL - OTIMIZACAO POR COLONIA DE FORMIGAS\n")
            f.write("====================================================\n")
            f.write(f"Melhor Distancia Encontrada: {melhor_distancia:.4f}\n")
            f.write("====================================================\n")
            f.write("Sequencia de Cidades (Rota):\n")
            rota_ids = [cidades[i]['id'] for i in melhor_rota]
            f.write(" -> ".join(rota_ids))
            f.write("\n")
        print(f"--> Relatório salvo em: {caminho_saida}")
    except Exception as e:
        print(f"Erro ao salvar arquivo: {e}")

def salvar_snapshot(graph, rota, geracao, distancia):
    """
    Gera e salva uma imagem da rota atual (Snapshot).
    Usado para mostrar a evolução a cada X gerações.
    """
    # Garante que a pasta output existe
    caminho_dir = os.path.join(os.path.dirname(__file__), '..', 'output')
    os.makedirs(caminho_dir, exist_ok=True)
    
    rota_plot = rota + [rota[0]]
    x = [graph.cidades[i]['x'] for i in rota_plot]
    y = [graph.cidades[i]['y'] for i in rota_plot]
    
    plt.figure(figsize=(6, 6))
    plt.plot(x, y, 'o-b', alpha=0.6) # Cidades em azul
    plt.plot(x, y, '-r', linewidth=1) # Rota em vermelho
    
    plt.title(f'Geração {geracao} - Distância: {distancia:.2f}')
    plt.xlabel('X')
    plt.ylabel('Y')
    
    nome_arquivo = os.path.join(caminho_dir, f'snap_geracao_{geracao:03d}.png')
    plt.savefig(nome_arquivo)
    plt.close() # Fecha para economizar memória

def plotar_graficos(graph, melhor_rota, historico_melhor, historico_media):
    """
    Gera o gráfico final com Mapa da Rota e Convergência Comparativa.
    """
    rota_plot = melhor_rota + [melhor_rota[0]]
    x = [graph.cidades[i]['x'] for i in rota_plot]
    y = [graph.cidades[i]['y'] for i in rota_plot]
    
    plt.figure(figsize=(14, 6))
    
    # Gráfico 1: Melhor Rota Final
    plt.subplot(1, 2, 1)
    plt.plot(x, y, 'o-k', markersize=6) # Pontos pretos
    plt.plot(x, y, '-r', linewidth=2, label='Melhor Caminho')
    plt.title(f'Melhor Rota Final (Dist: {historico_melhor[-1]:.2f})')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.legend()
    
    for c in graph.cidades:
        plt.text(c['x'], c['y'], f" {c['id']}", fontsize=9, color='blue')

    # Gráfico 2: Convergência (Melhor vs Média)
    plt.subplot(1, 2, 2)
    plt.plot(historico_media, color='blue', linestyle='--', alpha=0.5, label='Média da População')
    plt.plot(historico_melhor, color='green', linewidth=2, label='Melhor Global')
    
    plt.title('Evolução da Colônia (Convergência)')
    plt.xlabel('Gerações')
    plt.ylabel('Distância Total')
    plt.grid(True, linestyle=':', alpha=0.7)
    plt.legend()
    
    # Salva na pasta output
    caminho_img = os.path.join(os.path.dirname(__file__), '..', 'output', 'grafico_final.png')
    plt.savefig(caminho_img)
    plt.show()