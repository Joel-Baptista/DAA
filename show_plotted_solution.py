from edge_cover_optimizer import EdgeCoverOptimizer
import json
from excel_writer import ExcelWriter
from math import comb

f = open('/home/joelbaptista/Desktop/DAA/other_data/four_to_twelve_early_stop_lar_1.json')
tests = json.load(f)
f.close()

# for key in tests:
#
#     a = key.replace('(', '')
#     b = a.replace(')', '')
#     tuple_key = tuple(map(float, b.split(', ')))

n = 12
p = 0.75

GO = EdgeCoverOptimizer()
GO.nodes = n
GO.probability = p

GO.gnp_random_connected_graph()

GO.add_weights_to_graph()

GO.min_edge_selection = tests[f"({n}, {p})"]["best_selection"]

print(GO)

GO.plot_node_graph()
