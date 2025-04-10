import networkx as nx
import numpy as np
import itertools as it
import time
from matplotlib import pyplot as plt
from numba import njit

path1 = "net1.txt"
benchmark = "benchmark_net.txt"
path2 = "net2.txt"


def read_network(path, separator='\t'):
    length = 0
    with open(path) as file:
        nodes = []
        for line in file:
            line = line.replace('\n', '')
            nodes.append(list(map(int, line.split(separator))))
            length += 1
        # print(2 * nodes[1][0])
    return nodes, length

@njit
def count_dens(node_order, edge, MLP, Ts):
    for i in range(len(Ts)):
        if node_order != [0, 0]:
            MLP[i] += np.log10(np.power(node_order[edge[1]], Ts[i])) / np.sum(
                np.power(np.asarray(node_order), Ts[i]))
    return MLP

def read_and_analyze_network(path, separator='\t', T_start=0, T_stop=2, T_step=0.1):
    start_time = time.time()
    Ts = np.arange(T_start, T_stop + T_step / 2, T_step)
    MLP = np.zeros(len(Ts))
    node_order = [0, 0]
    # print(Ts)

    with open(path) as file:
        for line in file:
            # print(line)
            line = line.replace('\n', '')
            edge = list(map(int, line.split(separator)))
            for i in range(len(Ts)):
                if node_order != [0, 0]:
                    MLP[i] += np.log10(
                        np.power(node_order[edge[1]], Ts[i]) / np.sum(np.power(np.asarray(node_order), Ts[i])))
            try:
                node_order[edge[0]] += 1
                print("add ", line)
            except:
                node_order.append(1)
                print("append ", line)
            node_order[edge[1]] += 1
            # print(node_order)
            # if edge[0] % 1000 == 99:
            #     print(edge[0], ". ", MLP)

        print(MLP)
        print("Runtime: ", time.time() - start_time)
    return Ts, MLP


def make_graph(nods_n_cons):
    G = nx.Graph()
    for node_cons in nods_n_cons:
        node = node_cons[0]
        cons = node_cons[1:]
        for con in cons:
            G.add_edge(node, con)
    return G


# nodes1, length1 = read_network(path1, " ")
# nodes2, length2 = read_network(path2, " ")
Ts, MLP = read_and_analyze_network(benchmark, " ", T_start=0.5, T_stop=1.5, T_step=0.02)
plt.scatter(Ts, MLP)
for i in range(len(MLP)):
    if MLP[i] == np.max(MLP):
        print(Ts[i], ". ", MLP[i], "MAXIMUM")
    else:
        print(Ts[i], ". ", MLP[i])

# graph1 = make_graph(nodes1[0:10])
# graph2 = make_graph(nodes2[0:10])
# nx.draw_kamada_kawai(graph]1, with_labels=True, font_weight='bold')


plt.show()
# 49.13948082923889