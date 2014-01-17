from taggraph import nodes,edges
import networkx as nx
import matplotlib.pyplot as plt


def create_node_graph(nodes):
	g = nx.Graph()
	for name,value in nodes.iteritems():
		g.add_node(name)
		g.node[name]['size'] = value

	return g

ng = create_node_graph(nodes)
sizes = [ng.node[n]['size'] *100 for n in ng.node]
print sizes
nx.draw(ng,nodelist=ng.node.keys(),node_size=sizes)
plt.show()


