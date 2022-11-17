from itertools import combinations, groupby, chain
import itertools
import networkx as nx
import random
import matplotlib.pyplot as plt
from math import comb, sin, cos, pi, ceil, floor
import time
import numpy as np
from sympy.utilities.iterables import multiset_permutations

class EdgeCoverOptimizer:
    def __init__(self, n = None, p = None, s = 88740):

        self.nodes = n
        self.probability = p
        self.seed = s
        self.G = None
        self.expected_iterations = None
        self.min_weight = None
        self.min_weight_edge_cover = None
        self.min_edge_selection = None
        self.sets_tested = None
        self.basic_operations = None
        self.valid_iterations = None
        self.running_time = None
        self.optimization = ""

        # self.gnp_random_connected_graph() # Creates instance of G that is a graph of nx 

        # self.add_weights_to_graph()  # Adds weights to the created instance of G

    def gnp_random_connected_graph(self):
        """
        Generates a random undirected graph, similarly to an Erdős-Rényi 
        graph, but enforcing that the resulting graph is conneted
        """
        edges = combinations(range(self.nodes), 2)
        G = nx.Graph()
        G.add_nodes_from(range(self.nodes))
        
        if self.probability <= 0:
            return G
        if self.probability >= 1:
            return nx.complete_graph(self.nodes, create_using=G)

        for _, node_edges in groupby(edges, key=lambda x: x[0]):
            node_edges = list(node_edges)
            random.seed(self.seed)
            random_edge = random.choice(node_edges)
            G.add_edge(*random_edge)
            for e in node_edges:
                if random.random() < self.probability:
                    G.add_edge(*e)
        
        self.G = G
        self.expected_iterations = 2**len(G.edges())
    
    def add_weights_to_graph(self):
        random.seed(self.seed)
        self.num_edges = len(self.G.edges()) 
        self.max_num_edges = comb(self.nodes, 2) 
        for (u, v) in self.G.edges():
            self.G.edges[u,v]['weight'] = random.randint(1,20)

    def check_edge_cover(self, g):
        list_of_nodes = []

        for nodes in g:
            self.basic_operations += 1
            if nodes[0] not in list_of_nodes:
                list_of_nodes.append(nodes[0])
            
            if nodes[1] not in list_of_nodes:
                list_of_nodes.append(nodes[1])

        self.basic_operations += 1
        return (len(list_of_nodes) == len(self.G.nodes()))
    
    def greedy_edge_cover(self):
        self.optimization = "Greedy Heuristic"

        st = time.time()
        count = 0
        
        self.sets_tested = 0
        is_edge_cover = False
        greedy_edge_list = []
        edge_list = self.G.edges()
        weights_list = []
        min_sum = 0
        added_edges_list = []

        for (u, v) in self.G.edges():
            self.basic_operations += 1
            weights_list.append(self.G.edges[u, v]["weight"])

        zipped_lists = zip(weights_list, edge_list, range(0, len(edge_list)))
        sorted_pairs = sorted(zipped_lists)

        tuples = zip(*sorted_pairs)
        self.basic_operations += len(sorted_pairs)
        weights_sorted, edges_sorted, index_sorted = [list(tuple) for tuple in tuples]

        selection = [0] * len(edge_list)

        for i in range(floor(self.nodes / 2), len(edges_sorted)):
            self.sets_tested += 1
            count += 1

            self.basic_operations += 1

            if edges_sorted[i][0] in added_edges_list and edges_sorted[i][1] in added_edges_list:
                continue
            
            added_edges_list.append(edges_sorted[i][0])
            added_edges_list.append(edges_sorted[i][1])

            greedy_edge_list.append(edges_sorted[i])
            min_sum += weights_sorted[i]

            selection[index_sorted[i]] = 1

            is_edge_cover = self.check_edge_cover(greedy_edge_list)

            if is_edge_cover:
                break

        self.min_weight_edge_cover = greedy_edge_list
        self.min_weight = min_sum
        self.min_edge_selection = selection
        self.running_time = (time.time() - st) / 60
        self.iterations = count

    def optimize_edge_cover_v2(self):
        self.optimization = "Brute Force Optimization - Early stopping"

        self.iterations = 0
        self.valid_iterations = 0
        self.basic_operations = 0
        self.sets_tested = 0

        st = time.time()
        self.min_weight = None
        finish_search = False
        edge_num_first_edge_cover = None
        count = 0
        prev_percent = 0

        for n in range(floor(self.nodes / 2), self.num_edges + 1):
            lst = [1] * n + [0] * (self.num_edges - n)
            self.basic_operations += 1
            for perm in multiset_permutations(lst):
                self.sets_tested += 1 
                self.basic_operations += 4
                self.iterations += 1
                count += 1
                if count/self.expected_iterations * 100 > prev_percent:
                    print(str(prev_percent) + "%") 
                    prev_percent += 10

                new_g_edges = [x for x, y in zip(self.G.edges(), list(perm)) if y == 1]

                is_edge_cover = self.check_edge_cover(new_g_edges)

                if edge_num_first_edge_cover is None and is_edge_cover:
                    edge_num_first_edge_cover = n

                if is_edge_cover:
                    if n > edge_num_first_edge_cover and edge_num_first_edge_cover is not None:
                        print("Stop Searching")
                        finish_search = True
                        break
                    
                    self.valid_iterations += 1
                    weight_sum = 0

                    for (u, v) in new_g_edges:
                        self.basic_operations += 1
                        weight_sum += self.G.edges[u, v]['weight']
                    
                    if self.min_weight is None:
                        print("We got a new best: " + str(weight_sum))
                        self.min_weight = weight_sum
                        self.min_weight_edge_cover = new_g_edges
                        self.min_edge_selection = list(perm)     

                    elif weight_sum < self.min_weight:
                        print("We got a new best: " + str(weight_sum))
                        self.min_weight = weight_sum
                        self.min_weight_edge_cover = new_g_edges
                        self.min_edge_selection = list(perm)     

            if finish_search:
                break

        self.running_time = time.time() - st
    

    def optimize_edge_cover(self):
        self.optimization = "Brute Force Optimization"

        st = time.time()
        self.min_weight = None


        print("Start forming combinations")
        edges_comb = itertools.product(*[[0, 1]] * len(self.G.edges()))

        self.iterations = 0
        self.valid_iterations = 0
        edge_num_first_edge_cover = None

        if len(self.G.edges()) < 23:
            percent_step = 10
        else:
            percent_step = 2

        count = 0
        prev_percent = 0
        for activation in edges_comb:
            self.iterations += 1

            count += 1

            if count/self.expected_iterations * 100 > prev_percent :
                print(str(prev_percent) + "%") 
                prev_percent += percent_step

            new_g_edges = [x for x, y in zip(self.G.edges(), list(activation)) if y == 1]

            is_edge_cover = self.check_edge_cover(new_g_edges)

            if edge_num_first_edge_cover is None and is_edge_cover:
                edge_num_first_edge_cover = len(new_g_edges)

            if is_edge_cover:
                # if len(new_g_edges) > edge_num_first_edge_cover and edge_num_first_edge_cover is not None:
                #     print("Stop Searching")
                #     break

                self.valid_iterations += 1
                weight_sum = 0
                for (u, v) in new_g_edges:
                    weight_sum += self.G.edges[u, v]['weight']
                
                if self.min_weight is None:
                    print("We got a new best: " + str(weight_sum))
                    self.min_weight = weight_sum
                    self.min_weight_edge_cover = new_g_edges
                    self.min_edge_selection = list(activation)     

                elif weight_sum < self.min_weight:
                    print("We got a new best: " + str(weight_sum))
                    self.min_weight = weight_sum
                    self.min_weight_edge_cover = new_g_edges
                    self.min_edge_selection = list(activation)     

        self.running_time = (time.time() - st) / 60
    
    def __str__(self):

        result = f"Selected Nodes: {self.nodes}\n"
        result += f"Selected Probability: {self.probability}\n"
        result += f"Real Distribution: {round(self.num_edges/self.max_num_edges, 4)}\n"
        result += f"Edge Number: {self.num_edges}\n"
        result += f"Maximum Iterations: {self.expected_iterations}\n"
        result += f"Maximum Running time: {self.expected_iterations * pow(10, -4) / 60} minutes\n"

        return result

    def print_results(self):
        result = "<=========================================================>\n"
        result += f"Optimization technique: {self.optimization}\n"
        result += f"Best Edge Cover: {self.min_weight_edge_cover}\n"
        result += f"Best Weight: {self.min_weight}\n"
        result += f"Running Time: {self.running_time}\n"
        result += f"Performed Iterations: {self.iterations}\n"
        result += f"Performed Weight Calculations: {self.valid_iterations}\n"
        result += f"Performed Basic Operations: {self.basic_operations}\n"
        result += f"Tested Sets: {self.sets_tested}\n"

        print(result)

    def plot_node_graph(self):
        color_options = ['b','r']
        width_options = [1, 3]
        weights = {}
        colors = []
        width = []

        new_pos = {}

        layers = ceil((len(self.G.nodes()) - 1) / 5)
        raidus_step = 10 / layers
        theta_step = (layers * 2 * pi) / len(self.G.nodes)
        layer = 0
        r = 0
        t = 0
        for i in range(0, len(self.G.nodes())):
            t += theta_step + 0.1
            if i > layer * 5:
                r += raidus_step
                layer += 1

            new_pos[i] = np.array([r * cos(t) + 10, r * sin(t) + 10])



        i = 0
        for (u, v) in (self.G.edges()):
            colors.append(color_options[int(self.min_edge_selection[i])])
            width.append(width_options[int(self.min_edge_selection[i])])
            weights[(u, v)] = self.G.edges[u,v]['weight']
            i += 1

        plt.figure(figsize=(10,10))
        pos = nx.spring_layout(self.G)
        nx.draw_networkx_nodes(self.G,pos=new_pos)
        nx.draw_networkx_edges(self.G,edge_color=colors,pos=new_pos, width=width)
        nx.draw_networkx_edge_labels(self.G, pos=new_pos, edge_labels=weights)
        nx.draw_networkx_labels(self.G, pos=new_pos)

        plt.show()