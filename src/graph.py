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
        # Matriz de Distâncias pré-calculada
        self.matriz_distancias = self._calcular_matriz_distancias()

    def _calcular_matriz_distancias(self):
        """Gera matriz NxN com distâncias euclidianas."""
        matriz = np.zeros((self.num_cidades, self.num_cidades))
        for i in range(self.num_cidades):
            for j in range(self.num_cidades):
                if i != j:
                    dist = np.sqrt(
                        (self.cidades[i]['x'] - self.cidades[j]['x'])**2 + 
                        (self.cidades[i]['y'] - self.cidades[j]['y'])**2
                    )
                    matriz[i][j] = dist
        return matriz

    def get_distancia(self, i, j):
        return self.matriz_distancias[i][j]