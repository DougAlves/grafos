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
        

    # Busca em largura lexicográfica 
    def lbfs(self):
        # Conjunto de vértices
        V = list(self.graph.keys())

        # Conjunto de vértices visitados
        visitados = set()

        # Ordenação dos vértices de V
        sigma = [V]
        while True:
            con = range(len(sigma))
            u = [(i, j) for j in con for i in sigma[j] if i not in visitados]
            if len(u) == 0:
                break
            else:
                u, c = u[0]
                visitados.add(u)
                r = []
                nr = [u]
                pip = sigma.pop(c)
                for v in pip:
                    if v in self.graph[u]:
                        r.append(v)
                    elif v != u:
                        nr.append(v)
                if len(nr) != 0:
                    sigma.insert(c, nr)
                if len(r) != 0:
                    sigma.insert(c, r)
        return sigma

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

g = Graph(10)
g.addEdge(1, 4)
g.addEdge(2, 3)
g.addEdge(2, 1)
g.addEdge(4, 1)
g.addEdge(4, 6)
g.addEdge(1, 7)
g.addEdge(9, 2)
g.addEdge(9, 4)
print("Colorindo")
print(g.color())
print("Grafo")
print(g.printEdges())
print("Vértices coloridos")
print(g.printColoredVertices())