import os
import numpy as np
from scripts.add_leaks import add_leaks
from scripts.compare_reports import compare_reports
from scripts.add_observers import add_observers
from scripts.parse_nodes import parse_nodes
from deap import base, creator, tools, algorithms
import random

min_leak_coefficient = 0.0 
max_leak_coefficient = 0.1

def create_individual():
    leak_node = np.random.choice(leak_names)
    leak_coefficient = np.random.uniform(min_leak_coefficient, max_leak_coefficient)
    return [leak_node, leak_coefficient]

def evaluate(individual):
    leak_node, leak_coefficient = individual
    add_leaks({leak_node: leak_coefficient}, base_net, output_net)
    os.system(f"{epanet_dir} {output_net} {output_report}")
    diff = compare_reports(model_report, output_report)
    return (diff,)

def custom_crossover(ind1, ind2):
    ind1_name = ind1[0]
    ind2_name = ind2[0]
    ind1_coefficient = ind1[1]
    ind2_coefficient = ind2[1]
    offspring1 = [ind1_name, ind2_coefficient]
    offspring2 = [ind2_name, ind1_coefficient]
    return creator.Individual(offspring1), creator.Individual(offspring2)

def custom_mutation(individual, mu, sigma, indpb):
    if random.random() < indpb:
        node, coefficient = individual
        coefficient += random.gauss(mu, sigma)
        if coefficient < min_leak_coefficient:
            coefficient = min_leak_coefficient
        individual = (node, coefficient)
    return creator.Individual(individual), 
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

    observers = ["SW20", "HP12", "HP5", "SW/K01"]
    emitters = {"SD19":0.05}
    add_observers(observers, base_net, observers_net)
    add_leaks(emitters, observers_net, model_net)
    os.system(f"{epanet_dir} {model_net} {model_report}")

    # retrieve optimization parameters
    leak_names = parse_nodes(base_net)

    creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
    creator.create("Individual", tuple, fitness=creator.FitnessMin)
    toolbox = base.Toolbox()
    toolbox.register("individual", create_individual)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    toolbox.register("evaluate", evaluate)
    toolbox.register("mate", custom_crossover)
    toolbox.register("mutate", custom_mutation, mu=0.05, sigma=0.05, indpb=0.2)
    toolbox.register("select", tools.selBest)

    population_size = 50
    num_generations = 20
    pop = [creator.Individual(toolbox.individual()) for _ in range(population_size)]
    algorithms.eaSimple(pop, toolbox, cxpb=0.5, mutpb=0.2, ngen=num_generations, verbose=True)
    best_individual = tools.selBest(pop, k=1)[0]
    best_leak_node, best_leak_coefficient = best_individual
    
    add_leaks({best_leak_node: best_leak_coefficient}, base_net, output_net)
    os.system(f"{epanet_dir} {output_net} {output_report}")
    diff = compare_reports(model_report, output_report)
    print(best_leak_node, best_leak_coefficient)
    print("Difference:", diff)