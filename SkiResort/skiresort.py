from collections import defaultdict
import argparse
import networkx as nx
import re

config = {
	'V':    [0, 3.00, 'green'],
	'B':    [0, 2.40, 'blue'],
	'R':    [0, 1.80, 'red'],
	'N':    [0, 1.20, 'black'],
	'KL':   [0, 1.0, 'purple'],
	'SURF': [0, 6.00, 'orange'],
	'TPH':  [240, 1.20, 'grey'],
	'TC':	[120, 1.80, 'grey'],
	'TSD':	[60, 1.80, 'grey'],
	'TS':	[60, 2.40, 'grey'],
	'TK':	[60, 2.40, 'grey'],
	'BUS':	[2400, 1800, 'yellow']
}

def drawGraph(G, sp, rp):
	G.node[rp[0]]['color'] = 'green'
	for p in rp:
		G.node[p]['style'] = 'filled'

	for i in range(0, len(sp)):
		G.node[sp[i]]['fontcolor'] = 'red'
		try:
			w = []
			for e in G.edge[sp[i]][sp[i+1]]:
				w.append(G.edge[sp[i]][sp[i+1]][e]['weight'])
			G.edge[sp[i]][sp[i+1]][w.index(min(w))]['penwidth'] = 4
		except IndexError:
			break

	nx.write_dot(G, 'graph.gv')

def reachablePoints(G, start, lvl):
	points = [start]
	l = ['TPH','TC','TSD','TS','TK','BUS']
	for line in lvl:
		l.append(line)

	def dfs(G, start, l):
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
						if d[e]['type'] in l:
							yield parent,child
							visited.add(child)
							stack.append((child,iter(G[child])))
							break
			except StopIteration:
				stack.pop()

	for s,t in dfs(G, start, l):
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

def main(f, s, d, rp, lvl, o):
	G = parse(f)
	pred, dist = floydWarshall(G)
	sp, time = shortestPath(pred, dist, s, d)
	rp = reachablePoints(G, rp, lvl)

	print "Shortest Path : " + str(sp) + " in : " + str(time) + 'seconds'
	print "Reachable Points : " + str(rp)

	drawGraph(G, sp, rp)

def init():
	parser = argparse.ArgumentParser(description='AG44 : SkiResort')
	parser.add_argument('-f', action="store", default="dataski.txt", help="Data file")
	parser.add_argument('s', action="store", type=int, help="Source node for shortest path.")
	parser.add_argument('d', action="store", type=int, help="Destination node for shortest path.")
	parser.add_argument('rp', action="store", type=int, help="Source node for reachables points")
	parser.add_argument('lvl', action="store", default=[], help="List of routes depending on the level of the skier. (V,B,R,N,KL,SURF)")
	parser.add_argument('-o', action="store", default="graph.gv", help="Output file for the graph")
	args = parser.parse_args()

	main(args.f, args.s, args.d, args.rp, args.lvl, args.o)

if __name__ == '__main__':
	init()
