from edge_cover_optimizer import EdgeCoverOptimizer
import json
from excel_writer import ExcelWriter

nodes = [4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
probability = [0.125, 0.25, 0.5, 0.75]
method = ["optimal", "greedy"]

results = {}
fields = ["nodes", "probability", "edges", "optimal solution", "greedy solution", "optimal iterations", "greedy iterations", "optimal running time", "greedy running time"]
data = {"nodes": [],
        "probability": [],
        "edges": [],
        "optimal solution": [],
        "greedy solution": [],
        "optimal iterations": [],
        "greedy iterations": [],
        "optimal running time": [],
        "greedy running time": []
        }

GO = EdgeCoverOptimizer()

for n in nodes:
    for p in probability:
        GO.nodes = n
        GO.probability = p

        print("Generating Graph")

        GO.gnp_random_connected_graph()

        print("Adding Weights")
        GO.add_weights_to_graph()

        print(GO)

        data["nodes"].append(n)
        data["probability"].append(p)
        data["edges"].append(GO.num_edges)
        
        for m in method:
            if m == "optimal":
                
                GO.optimize_edge_cover_v2()

                data["optimal solution"].append(GO.min_weight)
                data["optimal iterations"].append(GO.iterations)
                data["optimal running time"].append(GO.running_time)

            elif m == "greedy":
                
                GO.greedy_edge_cover()

                data["greedy solution"].append(GO.min_weight)
                data["greedy iterations"].append( GO.iterations)
                data["greedy running time"].append(GO.running_time)

        results[f"({n}, {p})"] = {"best_edge_cover": GO.min_weight_edge_cover,
                           "best_weight": GO.min_weight,
                           "best_selection": GO.min_edge_selection,
                           "performed_iteration": GO.iterations,
                           "performed_valid_iterations": GO.valid_iterations,
                           "edge_num": GO.num_edges,
                           "running_time": GO.running_time}


ew = ExcelWriter()

ew.add_data(data=data, fields=fields)
ew.save_data(filename="four_to_twelve_early_stop")

with open("four_to_twelve_early_stop_lar.json", "w") as write_file:
    json.dump(results, write_file, indent=4)

# GO = EdgeCoverOptimizer(n = 200, p = 0.5)

# GO.gnp_random_connected_graph()

# GO.add_weights_to_graph()

# # print(GO)

# GO.greedy_edge_cover()

# GO.print_results()

# GO.plot_node_graph()