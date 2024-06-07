import os
import numpy as np
from scipy.optimize import minimize
from scripts.add_advanced_leaks import add_advanced_leaks
from scripts.add_observers import add_observers
from scripts.compare_reports import compare_reports
from scripts.parse_pipes import parse_pipes
import random

def objective_function(arguments):
    proposal = []
    for i in range(0, len(arguments), 2):
        node1, node2 = pipes[i // 2]
        coeff = arguments[i]
        dist = arguments[i + 1]
        proposal.append({"node1": node1, "node2": node2, "distance": dist, "coeff": coeff})
    add_advanced_leaks(proposal, observers_net, output_net)
    os.system(f"{epanet_dir} {output_net} {output_report}")
    diff = compare_reports(model_report, output_report)
    return diff

def optimization_algorithm():
    options = {'maxiter': 100}
    bounds = [(min_leak_coefficient, max_leak_coefficient), (min_distance, max_distance)] * len(pipes)
    initial_positions = []
    for _ in range(len(pipes)):
        distance = random.uniform(min_distance, max_distance)
        coefficient = random.uniform(min_leak_coefficient, max_leak_coefficient)
        initial_positions.extend([coefficient, distance])

    # Run PSO optimization
    result = minimize(objective_function, initial_positions, method='L-BFGS-B', options=options, bounds=bounds)

    # Extract the optimal solution
    optimal_coefficients = result.x

    optimal_leak_coefficients = []
    # Construct the optimal leak coefficients dictionary
    for i in range(0, len(optimal_coefficients), 2):
        node1, node2 = pipes[i // 2]
        coeff = optimal_coefficients[i]
        dist = optimal_coefficients[i + 1]
        optimal_leak_coefficients.append({"node1": node1, "node2": node2, "distance": dist, "coeff": coeff})

    return optimal_leak_coefficients

# Main
if __name__ == "__main__":
    files_dir = "/home/michal/MiSS-EPANET-Leaks-in-waterworks-research-project/knowledge_sources/real_life_network_data/"
    epanet_dir = "/home/michal/EPANET-2.2.0-Linux/bin/runepanet"
    base_net = f"{files_dir}base.inp"
    observers_net = f"{files_dir}observers.inp"
    model_net = f"{files_dir}model.inp"
    output_net = f"{files_dir}swarm.inp"
    model_report = f"{files_dir}model.txt"
    output_report = f"{files_dir}swarm.txt"

    observers = ["SW20", "HP12", "HP5", "SW/K01"]
    leaks = [{"node1": "AN4", "node2": "AN5", "distance": 0.5, "coeff": 0.05}, {"node1": "SW12", "node2": "SW13", "distance": 0.6, "coeff": 0.07}]
    add_observers(observers, base_net, observers_net)
    add_advanced_leaks(leaks, observers_net, model_net)
    os.system(f"{epanet_dir} {model_net} {model_report}")

    # retrieve optimization parameters
    pipes = parse_pipes(base_net)
    min_leak_coefficient = 0.0
    max_leak_coefficient = 0.1
    min_distance = 0.1
    max_distance = 0.9

    #perform optimization
    best_individual = optimization_algorithm()

    # check what our algorithm calculated
    add_advanced_leaks(best_individual, observers_net, output_net)
    os.system(f"{epanet_dir} {output_net} {output_report}")
    diff = compare_reports(model_report, output_report)
    for pair in best_individual :
        if pair["coeff"] > 0:
            print(pair)
    print("Difference:", diff)

