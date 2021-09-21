class Graph:
    def __init__(self):
        self.vertices=31
        self.graph=[[],
                    [2,9,14,21,28],[3],[20],[5],[6],[18],[8],[],
                    [10,22],[11,24],[12],[13,30],[],
                    [15],[20],[17],[18],[7,30],[],
                    [16,4],[9],[23],[10],[25],[26,29],[27],[],
                    [24],[12],[19,31],[]]
	    
    def isNotVisited(self,x, path):
	    size = len(path)
	    for i in range(size):
		    if (path[i] == x):return 0		
	    return 1

    def findpaths(self,src, dst, allpath):
        q = []
        path = []
        path.append(src)
        q.append(path.copy())
        #print(q)
        while (q):
            path = q.pop(0)
            #print(path)
            last = path[len(path) - 1]
            if (last == dst):allpath.append(path)
            for i in range(len(self.graph[last])):
                if (self.isNotVisited(self.graph[last][i], path)):
                    newpath = path.copy()
                    newpath.append(self.graph[last][i])
                    q.append(newpath)
        return allpath
                    
        

# if __name__ == "__main__":
#     src = 2
#     dst = 4
#     g=Graph()
#     #g.add_edge()
#     allpath=g.findpaths(src, dst, [])
#     print("answer: ",allpath)






'''
def add_edge(self):
        self.graph[1].append([2,9,14,21,28])
        self.graph[2].append([3])
        self.graph[3].append([20])
        self.graph[4].append([5])
        self.graph[5].append([6])
        self.graph[6].append([18])
        self.graph[7].append([8])
        self.graph[8].append([]) #last stoppage of the route
        self.graph[9].append([10,22])
        self.graph[10].append([11,24])
        self.graph[11].append([12])
        self.graph[12].append([13,30])
        self.graph[13].append([]) #last stoppage of the route
        self.graph[14].append([15])
        self.graph[15].append([20])
        self.graph[16].append([17])
        self.graph[17].append([18])
        self.graph[18].append([7,30])
        self.graph[19].append([])#last stoppage of the root
        self.graph[20].append([16,4])
        self.graph[21].append([9])
        self.graph[22].append([23])
        self.graph[23].append([10])
        self.graph[24].append([25])
        self.graph[25].append([26,29])
        self.graph[26].append([27])
        self.graph[27].append([])#last stoppage of the root
        self.graph[28].append([24])
        self.graph[29].append([12])
        self.graph[30].append([19,31])
        self.graph[31].append([])#last stoppage of the root 
        print(self.graph)
'''