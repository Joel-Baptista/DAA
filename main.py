from edge_cover_optimizer import EdgeCoverOptimizer
import json
from excel_writer import ExcelWriter
from math import comb


def calculate_expected_running_time(nodes_for_time, probability_for_time, speed, space_search=1.0):

    predicted_time = 0

    for cn in nodes_for_time:
        for cp in probability_for_time:

            predicted_edges = comb(cn, 2) * cp

            predicted_maximum_iterations = pow(2, predicted_edges)

            predicted_time += predicted_maximum_iterations * speed * space_search

    day = int(predicted_time // (24 * 3600))
    time = predicted_time % (24 * 3600)
    hour = int(time // 3600)
    time %= 3600

    minutes = int(time // 60)
    time %= 60

    seconds = int(time)

    print("It is estimated for the search to last " + str(day) + " days and " + str(hour) + "h" + str(minutes) + "m" + str(seconds) + "s")


nodes = [4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
probability = [0.125, 0.25, 0.5, 0.75]
method = ["optimal", "greedy"]
experiment = "four_to_thirteen"

calculate_expected_running_time(nodes, probability, pow(10, -5), 2 * pow(10, -6))
input()

results = {}
fields = ["nodes", 
            "probability",
            "edges",
            "optimal solution",
            "optimal tested sets",
            "optimal basic operations",
            "optimal running time",
            "greedy solution",
            "greedy tested sets",
            "greedy basic operations",
            "greedy running time"]

data = {"nodes": [],
        "probability": [],
        "edges": [],
        "optimal solution": [],
        "optimal tested sets": [],
        "optimal basic operations": [],
        "optimal running time": [],
        "greedy solution": [],
        "greedy tested sets": [],
        "greedy basic operations": [],
        "greedy running time": []
        }

GO = EdgeCoverOptimizer()

for n in nodes:
    for p in probability:
        GO.nodes = n
        GO.probability = p

        # print("Generating Graph")

        GO.gnp_random_connected_graph()

        # print("Adding Weights")
        GO.add_weights_to_graph()

        print(GO)

        data["nodes"].append(n)
        data["probability"].append(p)
        data["edges"].append(GO.num_edges)
        
        for m in method:
            if m == "optimal":
                
                GO.optimize_edge_cover_v2()

                data["optimal solution"].append(GO.min_weight)
                data["optimal tested sets"].append(GO.sets_tested)
                data["optimal basic operations"].append(GO.basic_operations)
                data["optimal running time"].append(GO.running_time)

                results[f"({n}, {p})"] = {"best_edge_cover": GO.min_weight_edge_cover,
                                          "best_weight": GO.min_weight,
                                          "best_selection": GO.min_edge_selection,
                                          "performed_sets_tested": GO.sets_tested,
                                          "performed_basic_operations": GO.basic_operations,
                                          "edge_num": GO.num_edges,
                                          "running_time": GO.running_time}

                with open(f"{experiment}_optimal.json", "w") as write_file:
                    json.dump(results, write_file, indent=4)

                GO.print_results()
            elif m == "greedy":
                
                GO.greedy_edge_cover()

                data["greedy solution"].append(GO.min_weight)
                data["greedy tested sets"].append(GO.sets_tested)
                data["greedy basic operations"].append(GO.basic_operations)
                data["greedy running time"].append(GO.running_time)

                results[f"({n}, {p})"] = {"best_edge_cover": GO.min_weight_edge_cover,
                                          "best_weight": GO.min_weight,
                                          "best_selection": GO.min_edge_selection,
                                          "performed_sets_tested": GO.sets_tested,
                                          "performed_basic_operations": GO.basic_operations,
                                          "edge_num": GO.num_edges,
                                          "running_time": GO.running_time}

                with open(f"{experiment}_greedy.json", "w") as write_file:
                    json.dump(results, write_file, indent=4)

                GO.print_results()

        ew = ExcelWriter()

        ew.add_data(data=data, fields=fields)
        ew.save_data(filename="four_to_thirteen")


# GO = EdgeCoverOptimizer(n = 200, p = 0.5)

# GO.gnp_random_connected_graph()

# GO.add_weights_to_graph()

# # print(GO)

# GO.greedy_edge_cover()

# GO.print_results()

# GO.plot_node_graph()