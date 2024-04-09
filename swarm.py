import os
import numpy as np
from scipy.optimize import minimize
from scripts.add_leaks import add_leaks
from scripts.compare_reports import compare_reports
from scripts.parse_nodes import parse_nodes

def objective_function(coefficients):
    leak_dict = {leak_names[i]: coefficients[i] for i in range(len(leak_names))}

    # Add leaks to the model
    add_leaks(leak_dict, base_net, output_net)

    # Run EPANET simulation
    os.system(f"{epanet_dir} {output_net} {output_report}")

    # Compare model report and current report
    diff = compare_reports(model_report, output_report)

    return diff

# Optimization Algorithm using PSO
def optimization_algorithm():
    # Define the PSO parameters
    options = {'c1': 0.5, 'c2' : 0.9, 'maxiter': 100}

    # Initialize the swarm with random particle positions
    initial_positions = np.random.uniform(low=min_leak_coefficient, high=max_leak_coefficient, size=len(leak_names))

    # Run PSO optimization
    result = minimize(objective_function, initial_positions, options=options)

    # Extract the optimal solution
    optimal_coefficients = result.x

    # Construct the optimal leak coefficients dictionary
    optimal_leak_coefficients = {leak_names[i]: optimal_coefficients[i] for i in range(len(leak_names))}

    return optimal_leak_coefficients

# Main
if __name__ == "__main__":
    files_dir = "/home/michal/MiSS-EPANET-Leaks-in-waterworks-research-project/knowledge_sources/real_life_network_data/"
    epanet_dir = "/home/michal/EPANET-2.2.0-Linux/bin/runepanet"
    base_net = f"{files_dir}base.inp"
    model_net = f"{files_dir}model.inp"
    output_net = f"{files_dir}swarm.inp"
    model_report = f"{files_dir}model.txt"
    output_report = f"{files_dir}swarm.txt"

    # manually add two leaks
    emitters = {"RED1":0.02, "SW2": 0.05}
    add_leaks(emitters, base_net, model_net)
    os.system(f"{epanet_dir} {model_net} {model_report}")

    # retrieve optimization parameters
    leak_names = parse_nodes(base_net)
    min_leak_coefficient = 0.0
    max_leak_coefficient = 0.1

    #perform optimization
    optimal_leak_coefficients = optimization_algorithm()

    # check what our algorithm calculated
    add_leaks(optimal_leak_coefficients, base_net, output_net)
    os.system(f"{epanet_dir} {output_net} {output_report}")
    diff = compare_reports(model_report, output_report)
    print({k: v for k, v in optimal_leak_coefficients.items() if v > 0.0})
    print("Difference:", diff)

