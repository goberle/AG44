from pprint import pprint

def reduced_matrix(adj_list, scc):
    red_mat = []

    for component1 in scc:
        tmp_mat = []
        for component2 in scc:
            it = 0
            if component1 != component2:
                for vertex1 in component1:
                    for vertex2 in component2:
                        if vertex2 in adj_list[vertex1]:
                            it += 1
            tmp_mat.append(it)
        red_mat.append(tmp_mat)
 
    return red_mat

def strongly_connected_components(adj_list):
    index_counter = [0]
    stack = []
    lowlinks = {}
    index = {}
    result = []
    
    def strongconnect(node):
        index[node] = index_counter[0]
        lowlinks[node] = index_counter[0]
        index_counter[0] += 1
        stack.append(node)
    
        successors = adj_list[node]
        for successor in successors:
            if successor not in index:
                strongconnect(successor)
                lowlinks[node] = min(lowlinks[node],lowlinks[successor])
            elif successor in stack:
                lowlinks[node] = min(lowlinks[node],index[successor])
        
        if lowlinks[node] == index[node]:
            connected_component = []
            while True:
                successor = stack.pop()
                connected_component.append(successor)
                if successor == node: break
            result.append(connected_component)
    
    for node in adj_list:
        if node not in index:
            strongconnect(node)
    
    return result

def adjmat_to_adjlist(adj_mat):
    adj_list = {}

    for (index,nodes) in enumerate(adj_mat):
        adj_list[index+1] = ([verteces+1 for verteces in range(len(nodes)) if nodes[verteces]>=1])
        
    return adj_list

def topological_sort(adj_list):
    result = []
    marked = []

    def visit(node):
        if node in marked:
            return
        if node not in result:
            marked.append(node)
            successors = adj_list[node]
            for successor in successors:
                visit(successor)
            result.insert(0, node)

    for node in adj_list:
        if node not in result:
            visit(node)

    return result

def longest_path(adj_list, topsort):
    w = {}
    result = []
    for node in adj_list:
        w[node] = 1

    for node in topsort:
        successors = adj_list[node]
        for successor in successors:
            w[successor] = max(w[successor], w[node]+1)

    print "Weight list :"
    print w

    wt = int
    n = max(w, key=w.get)
    while wt != 0:
        result.insert(0, n)
        wt = 0
        for node in adj_list:
            successors = adj_list[node]
            if n in successors:
                if w[node] > wt:
                    wt = w[node]
                    cn = node
        n = cn

    return result

def main():
    print "Welcome to the AG44 first project !"

    print "Parsing file . . ."
    f = open ('matrix' , 'r')
    adj_mat = [ map(int,line.split(' ')) for line in f ]
    f.close()
    print "Adjacancy matrix :"
    pprint(adj_mat)

    adj_list = adjmat_to_adjlist(adj_mat)
    print "Adjacancy list :"
    pprint(adj_list)

    scc = strongly_connected_components(adj_list)
    print "Strongly Connected Components :"
    print scc

    red_adj_mat = reduced_matrix(adj_list, scc)
    print "Reduced Matrix :"
    pprint(red_adj_mat)

    red_adj_list = adjmat_to_adjlist(red_adj_mat)
    print "Reduced adjacancy list :"
    pprint(red_adj_list)

    topsort = topological_sort(red_adj_list)
    print "Topological Sort :"
    print topsort

    lpath = longest_path(red_adj_list, topsort)
    print "Longest Path :"
    print lpath

if __name__ == '__main__':
    main()