class Vertex:
    def __init__(self, key):
        self.key = key
        self.neighborhood = []
        self.color = 0
        self.saturation_degree = 0
        self.degree = 0

    # OK
    def addSaturationDegree(self):
        for vertex in self.value:
            if vertex.color != 0:
                self.saturation_degree += 1
        return None

    # OK
    def decreaseSaturationDegree(self):
        for vertex in self.value:
            if vertex.color != 0:
                self.saturation_degree -= 1
        return None
    
    # OK
    def addDegree(self):
        self.degree += 1

    
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
            if neighbor.color == 0:
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

    def generateVertices(self, number_of_vertices):
        vertices = dict()
        for i in range(number_of_vertices):
            vertices[i + 1] = Vertex(i + 1)
        return vertices
    def addEdge(self,u,v):
        self.vertices[u].neighborhood.append(v)
        self.vertices[v].neighborhood.append(u)
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

    def vertexOrderedDegreeDict(self):
         # Generate a dict with the degree of every vertex in the graph
        vertex_degree_dict = {vertex:vertex.degree for vertex in self.vertices.values()}

        # Order from the highest degree to the lowest degree
        return dict(sorted(vertex_degree_dict.items(), key=lambda x:x[1], reverse=True))

    def higherSaturation (self):
        higherSaturation = 0
        vertex = Vertex()
        for vertex in self.vertices:
            if vertex.saturation > higherSaturation and vertex.color == 0:
                higherSaturation = vertex.saturation
                vertex = vertex
        return vertex

g = Graph(4)
g.addEdge(1,2)
g.addEdge(2,3)
g.addEdge(1,4)
print("Vertices")
print([g.vertices])
print("Edges")
print(g.edges)
print("Vertex Degree Dict")
print(g.vertexOrderedDegreeDict())