
test_graph = (('a', 'd'), ('c', 'o'))
test_dict = {
    'a': set(['d', 'c', 'o']),
    'd': set(['a', 'c', 'o']),
    'c': set(['a', 'd', 'o']),
    'o': set(['a', 'd', 'c'])
}

real_array = [['a', 'd', 't'], ['c', 'o', 'v'], ['j', 'f', 'm'], ['p', 'k', 'e']]


def dfs(graph, start, visited=None):
    if visited is None:
        visited = set()
    visited.add(start)
    for next in graph[start] - visited:
        dfs(graph, next, visited)
    return visited


def dfs_paths_2(graph, start, goal, path=None):
    if path is None:
        path = [start]
    if start == goal and len(path) >= 3:
        yield path
    for next in graph[start] - set(path):
        yield from dfs_paths_2(graph, next, goal, path + [next])

def dfs_paths_1(graph, start, goal):
    stack = [(start, [start])]
    while stack:
        (vertex, path) = stack.pop()
        for next in graph[vertex] - set(path):
            if next == goal:
                yield path + [next]
            else:
                stack.append((next, path + [next]))


def getGraphFromArray(array):
    def getNeighbourhood(x, y, array):
        if not array[x]:
            return set()

        maxX = len(array) - 1
        maxY = len(array[x]) - 1
        cordsX = []
        cordsY = []
        
        if x == 0:
            cordsX = [0, 1]
        elif x == maxX:
            cordsX = [maxX-1, maxX]
        else:
            cordsX = [x-1, x, x+1]

        if y == 0:
            cordsY = [0, 1]
        elif y == maxY:
            cordsY = [maxY-1, maxY]
        else:
            cordsY = [y-1, y, y+1]

        neighbords = []

        for mX in cordsX:
            for mY in cordsY:
                if mX == x and mY == y:
                    continue
                neighbords.append(array[mX][mY])
                
        return set(neighbords)


    graph = {}
    for x in range(len(array)):
        for y in range(len(array[x])):
            graph[array[x][y]] = getNeighbourhood(x, y, array)

    return graph

def generatePathes(array):
    graphDict = getGraphFromArray(array)
    vertexes = set(graphDict.keys())
    patches = []
    for firstV in vertexes:
        for endV in vertexes - set([firstV]):
            patches.extend(list(dfs_paths_2(graphDict, firstV, endV)))

    return patches
    



