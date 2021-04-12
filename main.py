

class Grafo:
    def __init__(self, vertices): 
        self.graph = dict()
        for v in range(vertices):
            self.graph[v + 1] = []
   
    def addEdge(self,u,v):
        self.graph[u].append(v)
        self.graph[v].append(u)

#busca em laggura lexicografica 
    def lbfs(self):
        l = len(self.graph.keys())
        V = list(self.graph.keys())
        visitados = set()
        sigma = [V]
        i = 0
        while True:
            con = range(len(sigma))
            u = [(i, j) for j in con for i in sigma[j] if i not in visitados]
            if len(u) == 0:
                break
            else:
                u, c = u[0]
                visitados.add(u)
                print(u, c)
                r = []
                nr = [u]
                pip = sigma.pop(c)
                print(pip)
                for v in pip:
                    if v in self.graph[u]:
                        r.append(v)
                    elif v != u:
                        nr.append(v)
                if len(nr) != 0:
                    sigma.insert(c, nr)
                if len(r) != 0:
                    sigma.insert(c, r)
                print(sigma)
        return sigma
    
    def colorir(self):
        coloracao = [x for x in self.graph.keys()]
        ordem = self.lbfs()
        return 'oi'

g = Grafo(4)
g.addEdge(1,2)
g.addEdge(1,4)
g.addEdge(4,2)
g.addEdge(1,3)
print(g.lbfs())