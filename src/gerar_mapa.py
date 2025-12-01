import matplotlib.pyplot as plt
import os

# Função rápida para ler e plotar apenas os pontos
def plotar_dataset_berlin():
    x, y = [], []
    
    # Lê o arquivo que você já criou
    with open('input/cidades.txt', 'r') as f:
        for linha in f:
            partes = linha.strip().split()
            x.append(float(partes[1]))
            y.append(float(partes[2]))

    plt.figure(figsize=(8, 6))
    plt.scatter(x, y, c='blue', marker='o', s=50, alpha=0.6)
    plt.title("Dataset Berlin52: Distribuição das Cidades")
    plt.xlabel("Coordenada X")
    plt.ylabel("Coordenada Y")
    plt.grid(True, linestyle='--', alpha=0.5)
    
    # Salva na pasta output
    os.makedirs('output', exist_ok=True)
    plt.savefig('output/berlin52_dataset.png')
    print("Imagem salva em output/berlin52_dataset.png")

if __name__ == "__main__":
    plotar_dataset_berlin()