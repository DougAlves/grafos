import time
import os


class Vertex:
    def __init__(self, key):
        self.key = key
        self.neighborhood = []
        self.color = 0
        self.saturation_degree = 0
        self.degree = 0

    # OK
    def calculateSaturationDegree(self):
        for neighbor in self.neighborhood:
            if neighbor.color != 0:
                self.saturation_degree += 1

    # OK
    def addSaturationDegree(self):
        self.saturation_degree += 1

    # OK
    def decreaseSaturationDegree(self):
        self.saturation_degree -= 1
    
    # OK
    def addDegree(self):
        self.degree += 1

    # OK
    def addNeighborhoodSaturationDegree(self):
        for neighbor in self.neighborhood:
            neighbor.addSaturationDegree()

    # OK
    def decreaseNeighborhoodSaturationDegree(self):
        for neighbor in self.neighborhood:
            neighbor.decreaseSaturationDegree()
    # OK
    def possibleColorsSet(self, number_of_vertices):
        possible_colors = list(range(1, number_of_vertices + 1))
        possible_colors_set = set(possible_colors)
        colors_already_used = set()

        for neighbor in self.neighborhood:
            if neighbor == 0:
                continue
            colors_already_used.add(neighbor.color)
        possible_colors_set -= colors_already_used
        if len(possible_colors_set) == 0:
            return None
        return list(possible_colors_set)




class Graph:
    def __init__(self, number_of_vertices): 
        self.vertices = self.generateVertices(number_of_vertices)
        self.edges = []
        self.nun_colors = 0

    # OK
    def generateVertices(self, number_of_vertices):
        vertices = dict()
        for i in range(number_of_vertices):
            vertices[i + 1] = Vertex(i + 1)
        return vertices

    # OK
    def addEdge(self,u,v):
        self.vertices[u].neighborhood.append(self.vertices[v])
        self.vertices[v].neighborhood.append(self.vertices[u])
        self.vertices[u].addDegree()
        self.vertices[v].addDegree()
        if (u, v) in self.edges or (v, u) in self.edges:
            return None
        else:
            self.edges.append((u, v))
        

    
    # OK
    def todosColoridos(self):
        for vertex in self.vertices.items():
            if vertex[1].color == 0:
                return False
        return True

    # OK
    def vertexOrderedDegreeDict(self):
         # Generate a dict with the degree of every vertex in the graph
        vertex_degree_dict = {vertex:vertex.degree for vertex in self.vertices.values()}

        # Order from the highest degree to the lowest degree
        return dict(sorted(vertex_degree_dict.items(), key=lambda x:x[1], reverse=True))

    # OK
    def higherSaturation(self):
        higherSaturation = 0
        higherSaturationVertex = None
        for vertex in self.vertices.items():
            if vertex[1].saturation_degree > higherSaturation and vertex[1].color == 0:
                higherSaturation = vertex[1].saturation_degree
                higherSaturationVertex = vertex[1]
            elif vertex[1].color == 0:
                higherSaturationVertex = vertex[1]
        return higherSaturationVertex


    # OK
    def color(self):
        if self.todosColoridos():
            return True
        higherSaturationVertex = self.higherSaturation()
        possibleColorsSet = higherSaturationVertex.possibleColorsSet(len(self.vertices.items()))
        if not possibleColorsSet:
            return False
        for color in possibleColorsSet:
            higherSaturationVertex.color = color
            higherSaturationVertex.addNeighborhoodSaturationDegree()
            if self.color():
                return True
            else:
                higherSaturationVertex.decreaseNeighborhoodSaturationDegree()
                higherSaturationVertex.color = 0
        return False

    def printEdges(self):
        for edge in self.edges:
            print("({}) --> ({})".format(edge[0], edge[1]))
        return True

    def printColoredVertices(self):
        for vertex in self.vertices.items():
            print("Vertex ({}) with color {}".format(vertex[1].key, vertex[1].color))
    
    def colorsUsed(self):
        maior = -1324
        for vertex in self.vertices.items():
            maior = max(maior, vertex[1].color)
        
        self.nun_colors = maior
        return maior

    def writeResults(self, path):
        f = open(path, 'w')
        f.write(f'v {len(self.vertices.keys())} x {self.colorsUsed()}\n')
        for vertex in self.vertices.items():
            f.write(f'x {vertex[1].key} {vertex[1].color}\n')

        for edge in self.edges:
            a, b = edge
            f.write(f"e {a} {b}\n")
        

def buildGraphUFRN(path):
    f = open(path, "r")
    grafo = None
    for line in f.readlines():
        if ':' in line:
            continue
        if not (' ' in line):
            grafo = Graph(int(line))
        else:
            a, b = (line.split(' ')[0],line.split(' ')[1])
            a, b = (int(a), int(b))
            grafo.addEdge(a, b)
    return grafo

def buildGraphOrLib(path):
    f = open(path, "r")
    _, _, nun_v, _ = f.readline().split()
    nun_v = int(nun_v)
    grafo = Graph(nun_v)
    for line in f.readlines():
        _, a, b = line.split()
        grafo.addEdge(int(a), int(b))
    return grafo

ufrn_path = 'datasets/ufrn/'
orlib_path = 'datasets/or-library/'


def apeend_general_table(dataset, nun_colors, delta_time, nun_v):
    f = open('resultados_gerais.txt', 'a')
    f.write(f'\n{dataset}, {nun_colors}, {nun_v} , {delta_time}')


def testUFRN():
    for dataset in os.listdir(ufrn_path):
        g = buildGraphUFRN(ufrn_path + dataset)
        antes = time.time()
        g.color()
        dt = time.time() - antes
        print(f'{dataset} - {dt}')
        g.writeResults('datasets/resultados/ufrn/' + dataset)
        apeend_general_table(dataset, g.nun_colors, dt, len(g.vertices.keys()))

def testOrLib():
    for dataset in os.listdir(orlib_path):
        g = buildGraphOrLib(orlib_path + dataset)
        print('built')
        antes = time.time()
        g.color()
        dt = time.time() - antes
        print(f'{dataset} - {dt}')
        g.writeResults('datasets/resultados/or-library/' + dataset)
        apeend_general_table(dataset, g.nun_colors, dt, len(g.vertices.keys()))

testUFRN()
testOrLib()
