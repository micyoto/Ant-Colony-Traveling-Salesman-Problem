# src/aco.py
import numpy as np
import random

class AntColony:
    def __init__(self, graph, num_formigas, alfa, beta, evaporacao, q):
        """
        Configura a Colônia de Formigas.
        Args:
            graph: Objeto da classe Graph.
            num_formigas: Número de agentes.
            alfa: Importância do feromônio.
            beta: Importância da visibilidade (distância).
            evaporacao: Taxa de evaporação (0.0 a 1.0).
            q: Intensidade do feromônio depositado.
        """
        self.graph = graph
        self.num_formigas = num_formigas
        self.alfa = alfa
        self.beta = beta
        self.evaporacao = evaporacao
        self.Q = q
        
        # Matriz de Feromônios (inicializada com valor pequeno)
        self.feromonio = np.ones((graph.num_cidades, graph.num_cidades)) * 0.1
        
        self.melhor_rota_global = []
        self.melhor_distancia_global = float('inf')
        self.historico_convergencia = []

    def _selecionar_proxima_cidade(self, atual, visitadas):
        """Calcula a probabilidade e escolhe a próxima cidade (Roleta Viciada)."""
        probabilidades = []
        disponiveis = [i for i in range(self.graph.num_cidades) if i not in visitadas]

        somatorio = 0.0
        
        for destino in disponiveis:
            tau = self.feromonio[atual][destino]      # Quantidade de Feromônio
            dist = self.graph.get_distancia(atual, destino)
            
            # Visibilidade (eta) = 1 / distancia
            eta = 1.0 / (dist if dist > 0 else 0.0001)
            
            # Fórmula do ACO: (tau^alfa) * (eta^beta)
            valor = (tau ** self.alfa) * (eta ** self.beta)
            probabilidades.append(valor)
            somatorio += valor

        # Se somatório for 0 (caso raro numérico), escolhe aleatório
        if somatorio == 0:
            return random.choice(disponiveis)
        
        # Normaliza probabilidades (soma deve ser 1)
        probabilidades = [p / somatorio for p in probabilidades]
        
        # Escolha ponderada baseada na probabilidade
        return np.random.choice(disponiveis, p=probabilidades)

    def run(self, num_iteracoes):
        """Executa o loop principal da otimização."""
        print(f"Iniciando ACO com {num_iteracoes} iterações e {self.num_formigas} formigas...")
        
        for it in range(num_iteracoes):
            todas_rotas = []
            todas_distancias = []
            
            # --- Passo 1: Construção das Soluções pelas Formigas ---
            for _ in range(self.num_formigas):
                # Formiga começa em cidade aleatória
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
                
                # Retorno à cidade inicial (fechar o ciclo)
                distancia_atual += self.graph.get_distancia(rota[-1], rota[0])
                
                todas_rotas.append(rota)
                todas_distancias.append(distancia_atual)

                # Verifica se é a melhor solução global encontrada
                if distancia_atual < self.melhor_distancia_global:
                    self.melhor_distancia_global = distancia_atual
                    self.melhor_rota_global = rota
            
            self.historico_convergencia.append(self.melhor_distancia_global)

            # --- Passo 2: Atualização dos Feromônios ---
            # Evaporação global
            self.feromonio *= (1.0 - self.evaporacao)
            
            # Depósito de novo feromônio pelas formigas desta iteração
            for i, rota in enumerate(todas_rotas):
                dist = todas_distancias[i]
                # Q dividido pela distância total (caminhos menores ganham mais feromônio)
                deposito = self.Q / dist 
                
                for j in range(len(rota)):
                    # Define origem e destino (circular, incluindo volta ao início)
                    a = rota[j]
                    b = rota[(j + 1) % len(rota)]
                    
                    # Atualiza matriz (grafo não-direcionado: ida e volta recebem feromônio)
                    self.feromonio[a][b] += deposito
                    self.feromonio[b][a] += deposito
            
            # Log de progresso a cada 10 iterações
            if (it + 1) % 10 == 0:
                print(f"Iteração {it+1}/{num_iteracoes} -> Melhor Distância: {self.melhor_distancia_global:.4f}")

        print("Execução finalizada.")