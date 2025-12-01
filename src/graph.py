# src/graph.py
import numpy as np

class Graph:
    def __init__(self, cidades):
        """
        Inicializa o Grafo com a lista de cidades.
        
        Args:
            cidades (list): Lista de dicionários contendo 'id', 'x', 'y'.
        """
        self.cidades = cidades
        self.num_cidades = len(cidades)
        # Matriz de Distâncias (N x N) pré-calculada para otimização
        self.matriz_distancias = self._calcular_matriz_distancias()

    def _calcular_matriz_distancias(self):
        """
        Gera uma matriz NumPy NxN com as distâncias euclidianas.
        Requisito: Uso de matrizes.
        """
        matriz = np.zeros((self.num_cidades, self.num_cidades))
        
        for i in range(self.num_cidades):
            for j in range(self.num_cidades):
                if i != j:
                    # Cálculo da distância Euclidiana: sqrt((x1-x2)^2 + (y1-y2)^2)
                    dist = np.sqrt(
                        (self.cidades[i]['x'] - self.cidades[j]['x'])**2 + 
                        (self.cidades[i]['y'] - self.cidades[j]['y'])**2
                    )
                    matriz[i][j] = dist
                    
        return matriz

    def get_distancia(self, i, j):
        """Retorna a distância entre a cidade de índice i e j."""
        return self.matriz_distancias[i][j]