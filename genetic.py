import os
import numpy as np
from scripts.add_leaks import add_leaks
from scripts.compare_reports import compare_reports
from scripts.add_observers import add_observers
from scripts.parse_nodes import parse_nodes
from deap import base, creator, tools, algorithms

min_leak_coefficient = 0.0 
max_leak_coefficient = 0.1

def evaluate(individual):
    if not all(val > 0 for val in individual): 
        return (1000,)
    leak_dict = {leak_names[i]: individual[i] for i in range(len(leak_names))}
    add_leaks(leak_dict, base_net, output_net)
    os.system(f"{epanet_dir} {output_net} {output_report}")
    diff = compare_reports(model_report, output_report)
    return (diff,)

def create_individual():
    return creator.Individual(np.random.uniform(min_leak_coefficient, max_leak_coefficient) for _ in range(len(leak_names)))

# Main
if __name__ == "__main__":
    files_dir = "/home/michal/MiSS-EPANET-Leaks-in-waterworks-research-project/knowledge_sources/real_life_network_data/"
    epanet_dir = "/home/michal/EPANET-2.2.0-Linux/bin/runepanet"
    base_net = f"{files_dir}base.inp"
    observers_net = f"{files_dir}observers.inp"
    model_net = f"{files_dir}model.inp"
    output_net = f"{files_dir}genetic.inp"
    model_report = f"{files_dir}model.txt"
    output_report = f"{files_dir}genetic.txt"

    # manually add two leaks
    emitters = {"RED1":0.02, "SW2": 0.05}
    observers = ["SW20", "HP12", "HP5", "SW/K01"]
    add_observers(observers, base_net, observers_net)
    add_leaks(emitters, observers_net, model_net)
    os.system(f"runepanet {model_net} {model_report}")

    # retrieve optimization parameters
    leak_names = parse_nodes(base_net)

    toolbox = base.Toolbox()
    creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMin)
    toolbox.register("individual", create_individual)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    toolbox.register("evaluate", evaluate)
    toolbox.register("mate", tools.cxBlend, alpha=0.5)
    toolbox.register("mutate", tools.mutGaussian, mu=0, sigma=0.1, indpb=0.2)
    toolbox.register("select", tools.selTournament, tournsize=3)

    population_size = 50
    num_generations = 20
    pop = toolbox.population(n=population_size)
    algorithms.eaSimple(pop, toolbox, cxpb=0.5, mutpb=0.2, ngen=num_generations, verbose=True)
    best_individual = tools.selBest(pop, k=1)[0]
    optimal_leak_coefficients = {leak_names[i]: best_individual[i] for i in range(len(leak_names))}
    
    add_leaks(optimal_leak_coefficients, base_net, output_net)
    os.system(f"{epanet_dir} {output_net} {output_report}")
    diff = compare_reports(model_report, output_report)
    print({k: v for k, v in optimal_leak_coefficients.items() if v > 0.0})
    print("Difference:", diff)