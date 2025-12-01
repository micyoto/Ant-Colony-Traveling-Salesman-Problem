# src/aco.py
import numpy as np
import random
import utils # Importa para chamar o snapshot

class AntColony:
    def __init__(self, graph, num_formigas, alfa, beta, evaporacao, q):
        self.graph = graph
        self.num_formigas = num_formigas
        self.alfa = alfa
        self.beta = beta
        self.evaporacao = evaporacao
        self.Q = q
        
        # Inicializa feromônio
        self.feromonio = np.ones((graph.num_cidades, graph.num_cidades)) * 0.1
        
        self.melhor_rota_global = []
        self.melhor_distancia_global = float('inf')
        
        # Históricos para o gráfico de convergência
        self.historico_melhor = []
        self.historico_media = []

    def _selecionar_proxima_cidade(self, atual, visitadas):
        """Calcula probabilidade e escolhe próxima cidade."""
        probabilidades = []
        disponiveis = [i for i in range(self.graph.num_cidades) if i not in visitadas]
        somatorio = 0.0
        
        for destino in disponiveis:
            tau = self.feromonio[atual][destino]
            dist = self.graph.get_distancia(atual, destino)
            eta = 1.0 / (dist if dist > 0 else 0.0001)
            
            valor = (tau ** self.alfa) * (eta ** self.beta)
            probabilidades.append(valor)
            somatorio += valor

        if somatorio == 0:
            return random.choice(disponiveis)
        
        probabilidades = [p / somatorio for p in probabilidades]
        return np.random.choice(disponiveis, p=probabilidades)

    def run(self, num_iteracoes):
        print(f"Iniciando ACO com {num_iteracoes} iterações e {self.num_formigas} formigas...")
        
        for it in range(num_iteracoes):
            todas_rotas = []
            todas_distancias = []
            
            # --- Passo 1: Construção das Soluções ---
            for _ in range(self.num_formigas):
                inicio = random.randint(0, self.graph.num_cidades - 1)
                rota = [inicio]
                visitadas = {inicio}
                distancia_atual = 0.0
                curr = inicio
                
                while len(rota) < self.graph.num_cidades:
                    prox = self._selecionar_proxima_cidade(curr, visitadas)
                    distancia_atual += self.graph.get_distancia(curr, prox)
                    rota.append(prox)
                    visitadas.add(prox)
                    curr = prox
                
                # Fechar o ciclo
                distancia_atual += self.graph.get_distancia(rota[-1], rota[0])
                
                todas_rotas.append(rota)
                todas_distancias.append(distancia_atual)

                # Atualiza Melhor Global
                if distancia_atual < self.melhor_distancia_global:
                    self.melhor_distancia_global = distancia_atual
                    self.melhor_rota_global = rota
            
            # --- Coleta de Estatísticas ---
            media_iteracao = np.mean(todas_distancias)
            self.historico_melhor.append(self.melhor_distancia_global)
            self.historico_media.append(media_iteracao)
            
            # --- Snapshot a cada 20 gerações (e na primeira) ---
            if it == 0 or (it + 1) % 20 == 0:
                utils.salvar_snapshot(
                    self.graph, 
                    self.melhor_rota_global, 
                    it + 1, 
                    self.melhor_distancia_global
                )

            # --- Passo 2: Atualização de Feromônio ---
            self.feromonio *= (1.0 - self.evaporacao)
            
            for i, rota in enumerate(todas_rotas):
                dist = todas_distancias[i]
                deposito = self.Q / dist
                for j in range(len(rota)):
                    a = rota[j]
                    b = rota[(j + 1) % len(rota)]
                    self.feromonio[a][b] += deposito
                    self.feromonio[b][a] += deposito
            
            # Log no terminal
            if (it + 1) % 10 == 0:
                print(f"Iteração {it+1:03d} | Melhor: {self.melhor_distancia_global:.2f} | Média: {media_iteracao:.2f}")

        print("Execução finalizada.")