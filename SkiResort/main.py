from collections import defaultdict
import networkx as nx
import re

config = {
	'V':    [0, 3.00, 'green'],
	'B':    [0, 2.40, 'blue'],
	'R':    [0, 1.80, 'red'],
	'N':    [0, 1.20, 'black'],
	'KL':   [0, 1.0, 'grey'],
	'SURF': [0, 6.00, 'grey'],
	'TPH':  [240, 1.20, 'grey'],
	'TC':	[120, 1.80, 'grey'],
	'TSD':	[60, 1.80, 'grey'],
	'TS':	[60, 2.40, 'grey'],
	'TK':	[60, 2.40, 'grey'],
	'BUS':	[2400, 1800, 'yellow']
}

def drawGraph(G):
	nx.write_dot(G, 'graph.gv')

def reachablePoints(G, start, lvl):
	points = [start]

	def dfs(G, start, lvl):
		visited = set()
		visited.add(start)
		stack = [(start,iter(G[start]))]
		while stack:
			parent,children = stack[-1]
			try:
				child = next(children)
				if child not in visited:
					d = G.edge[parent][child]
					for e in d:
						if d[e]['type'] in lvl:
							yield parent,child
							visited.add(child)
							stack.append((child,iter(G[child])))
							break
			except StopIteration:
				stack.pop()

	for s,t in dfs(G, start, lvl):
		points.append(t)

	return points

def shortestPath(pred, dist, i, j):
	p = []
	t = dist[i][j]

	def path(i, j):
		if i == j:
			p.append(i)
		try:
			inter = pred[i][j]
		except KeyError:
			return
		path(i, inter)
		p.append(j)

	path(i, j)
	return p, t

def floydWarshall(G):
	dist = defaultdict(lambda : defaultdict(lambda: float('inf')))
	pred = defaultdict(dict)
	for u in G:
		dist[u][u] = 0
	
	for u,v,d in G.edges(data=True):
		e_weight = d.get('weight', 1.0)
		dist[u][v] = min(e_weight, dist[u][v])
		pred[u][v] = u

	for w in G:
		for u in G:
			for v in G:
				if dist[u][v] > dist[u][w] + dist[w][v]:
					dist[u][v] = dist[u][w] + dist[w][v]
					pred[u][v] = pred[w][v]

	return dict(pred),dict(dist)

def parse(dataski):
	G = nx.MultiDiGraph()
	f = open(dataski, 'r')

	nbNodes = int(f.readline())
	for i in range(nbNodes):
		c = re.split(r'\t+', f.readline())
		G.add_node(int(c[0]), label=c[1], altitude=int(c[2]))

	nbEdges = int(f.readline())
	for i in range(nbEdges):
		c = re.split(r'\t+', f.readline())
		if c[2] != "BUS":
			w = config[c[2]][0] + ((abs(G.node[int(c[3])]['altitude'] - G.node[int(c[4])]['altitude'])) * config[c[2]][1])
		else:
			if c[1] == "navette1600-1800" or c[1] == "navette1800-1600":
				w = config[c[2]][1]
			else:
				w = config[c[2]][0]
		G.add_edge(int(c[3]), int(c[4]), label=c[1], weight=w, type=c[2], color=config[c[2]][2])

	f.close()
	return G

def main():
	G = parse('dataski.txt')
	pred, dist = floydWarshall(G)
	sp, time = shortestPath(pred, dist, 1, 4)
	rp = reachablePoints(G, 31, ['V', 'TPH', 'TSD', 'TK', 'TS', 'TC', 'BUS'])

	print sp
	print str(time) + 's'
	print rp

	drawGraph(G)

if __name__ == '__main__':
	main()
