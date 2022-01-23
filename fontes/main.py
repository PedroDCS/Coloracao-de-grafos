'''
Nome Discente: Pedro Daniel Camargos Soares
Matrícula: 0020640

Nome Discente: Lucas Gabriel de Almeida						
Matrícula: 0035333
Data: 20/01/2022

'''

'''
Algoritmo com objetivo de econtrar o numero cromatico em um grafo G (V,A)
Utilizando o algoritmo de coloração de grafos guloso e
o algoritmo de Welsh Powell
'''

from collections import defaultdict
from heapq import *
import time
import sys
class Grafo(object):
    # Implementação básica de um grafo.

    def __init__(self, v):
        # numero de vertices
        self.vertices = v
        # representação por list de adjacencia
        self.adj = defaultdict(list)
        # vetor auxiliar para salvar a adjacencia de cada vertice, facilitando as implementações dos algoritmos
        self.adjaux = [set() for _ in range(int(v))]
        
    def adiciona_aresta(self, u, v, peso):
        # Adiciona uma aresta entre os vertices 'u' e 'v' e o seu peso
        # lista de adjacencia normal
        self.adj[u].insert(0, [v, peso])
        self.adj[v].insert(0, [u, peso])
        # vetor auxiliar, que salva somente a adjacencia de cada vertice
        self.adjaux[u].add(v)
        self.adjaux[v].add(u)

    # se caso for printar o grafo, isso o formatara
    def __str__(self):
        return '{}({})'.format(self.__class__.__name__, dict(self.adj))

    def coloracao_gulosa(self):
        # deixa todos os vertices com um valor de cor invalido para serem coloridos
        resultado = [-1] * int(self.vertices)
        # coloca a primeira cor no primeiro vertice
        resultado[0] = 0;
 
        # vetor temporario para armazenar as cores disponiveis
        # caso o valor da cor seja True, significa que ela ja foi colocada em um vertice adjacente
        disponivel = [False] * int(self.vertices)
    
        #atribui uma cor aos vertices restantes do grafo
        for u in range(1, int(self.vertices)):
            
            # processa todos os vertices adjacentes e coloca suas cores como insisponiveis
            for vizinho, peso in self.adj[u]:
                if (resultado[vizinho] != -1):
                    disponivel[resultado[vizinho]] = True
    
            # procura a primeira cor disponivel
            cor = 0
            while cor < int(self.vertices):
                if (disponivel[cor] == False):
                    break
                cor += 1
                
            # então atribui a cor disponivel ao vertice em questão
            resultado[u] = cor
    
            # reseta os valores das cores para False para as proximas iterações
            for vizinho, peso in self.adj[u]:
                if (resultado[vizinho] != -1):
                    disponivel[resultado[vizinho]] = False
    
        # retorna o resultado
        return resultado, max(resultado)+1

    def coloracao_Welsh_Powell(self):
        # deixa todos os vertices com um valor de cor invalido para serem coloridos
        resultado = [-1] * int(self.vertices)

        # vetor auxiliar que guarda os vertices que ainda não possuem cores
        restante = []
        for i in range(int(self.vertices)):
            restante.append([i,len(self.adj[i])])
        # os vertices são organizados de acordo com o seu grau, do maior para o menor
        restante = sorted(restante, key=lambda x: x[1],reverse=True)

        #começa com a primeira cor
        color = 0
        #vetor auxiliar para salvar os vertices adjacentes ao vertice em questão
        coloradj = []

        # vetor auxiliar que guarda os vertices que ainda não possuem cores
        # porem, só ira armazernar os vertices ja organizados, sem o seu grau
        rest = [item[0] for item in restante]

        # enquanto existir vertices sem cores, faça
        while len(rest) != 0:
            #pega o primeiro vertice do vetor e da a ele a primeira cor disponivel
            u = rest.pop(0)
            resultado[u] = color

            # salva os vertices adjacentes ao vertice em questão
            coloradj = []
            coloradj.append(u)
            coloradj+=self.adjaux[u]

            # pega todos os vertices ainda não coloridos para que sejam iterados
            resto = []
            resto+= rest
            #variavel auxiliar para salvar o index do vertice 
            index=0
            # enquanto existir vertices sem cores, faça
            while len(resto) >0:
                if len(rest)%10000 ==0:
                    print(len(rest))
                i = resto.pop(0)
                # caso o vertice não seja visinho de um vertice colorido com a cor em questão, seja colorido
                if (i not in coloradj):
                    resultado[i] = color
                    x = rest.pop(index)
                    coloradj+=self.adjaux[i]
                    index-=1
                index+=1
            color+=1
        #retorna o resultado e o numero de cores necessarias
        return resultado, color

def main(args):
    def arquivosaida(arq, alg, tempo, resultadoado, cores, inicioAlgoritmo, fimAlgoritmo, g):
        arquivo = open(arq+".txt", 'w')
        arquivo.write(
            "==================== Coloracao de Grafos =====================\n")
        arquivo.write(alg+"\n")

        arquivo.write("Data de execucao do algoritmo: " +
                      time.ctime(inicioAlgoritmo)+"\n")
        #arquivo.write("Data de execucao do algoritmo: " + str(data)+"\n")
        arquivo.write(
            "==============================================================\n")
        arquivo.write("Tempo de execucao do Algoritmo: " + str(tempo)+"\n")
        arquivo.write("Numero de Cores necessarias: " +
                      str(cores)+"\n")

        arquivo.write(
            "==============================================================\n")
        verticescoloridos = ''
        for u in range(int(g.vertices)):
            verticescoloridos += "Vertice " + str(u) + " --->  Cor "+ str(resultadoado[u]) + "\n"
        arquivo.write(verticescoloridos)
        arquivo.close()

    def lerArq(arq):
        arquivo = open(str(arq), 'r')
        vertices = arquivo.readline()
        arestas = arquivo.readline()
        linhas = arquivo.readlines()
        arquivo.close()
        return vertices, arestas, linhas

    if args.__len__() < 4:
        print("falta de parametros")
        exit()

    algoritmo = int(args[1])
    entrada = args[2]
    saida = args[3]

    vertices, arestas, linhas = lerArq(entrada)

    graph = Grafo(vertices)
    for linha in linhas:
        aux = linha.split()
        graph.adiciona_aresta(int(aux[0]), int(aux[1]), float(aux[2]))
 
    if algoritmo == 1:
        algoritmo = "algoritmo Para coloracao de grafos guloso"
        print(algoritmo)
        inicio = time.time()
        resultado, color = graph.coloracao_gulosa()
        fim = time.time()
        print("Tempo de Execucao: ",fim - inicio,"\n")
        arquivosaida(saida, algoritmo, fim - inicio,
                    resultado, color, inicio, fim, graph)
    elif algoritmo == 2:
        algoritmo = "algoritmo de coloracao de grafos de Welsh-Powell"
        print(algoritmo)
        inicio = time.time()
        resultado, color = graph.coloracao_Welsh_Powell()
        fim = time.time()
        print("Tempo de Execucao: ",fim - inicio,"\n")
        arquivosaida(saida, algoritmo, fim - inicio,
                    resultado, color, inicio, fim, graph)
    else:
        print("Digite uma entrada de algoritmo valida")

if __name__ == "__main__":
    main(sys.argv)
