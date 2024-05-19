import os
import sys
import threading
from scripts.add_advanced_leaks import add_advanced_leaks
from scripts.compare_reports import compare_reports
from scripts.add_observers import add_observers
from scripts.parse_pipes import parse_pipes
from deap import base, creator, tools, algorithms
import random
import matplotlib.pyplot as plt
from scoop import futures
import pathlib

min_leak_coefficient = 0.0 
max_leak_coefficient = 0.1

script_dir = str(pathlib.Path(__file__).parent.resolve())
files_dir = script_dir + "/knowledge_sources/real_life_network_data/"
epanet_dir = script_dir + "/knowledge_sources/EPANET-2.2.0-Linux/bin/runepanet"
base_net = f"{files_dir}base.inp"
observers_net = f"{files_dir}observers.inp"
model_net = f"{files_dir}model.inp"
output_net = f"{files_dir}genetic-{threading.get_ident()}.inp"
model_report = f"{files_dir}model.txt"
output_report = f"{files_dir}genetic-{threading.get_ident()}.txt"

def create_individual():
    network = []
    for pair in pipes:
        node1, node2 = pair
        distance = random.uniform(0.1, 0.9)
        coefficient = random.uniform(min_leak_coefficient, max_leak_coefficient)
        network.append({"node1": node1, "node2": node2, "distance": distance, "coeff": coefficient})
    return network

def evaluate(individual):
    add_advanced_leaks(individual, observers_net, output_net)
    os.system(f"{epanet_dir} {output_net} {output_report}")
    diff = compare_reports(model_report, output_report)
    return (diff,)

def custom_crossover(ind1, ind2):
    offspring1 = []
    offspring2 = []
    for i in range(len(ind1)):
        coeff_point = random.randint(0, 1)
        distance_point = random.randint(0, 1)
        offspring1.append({"node1": ind1[i]["node1"], "node2": ind1[i]["node2"], 
                           "distance": distance_point * ind1[i]["distance"] + (1 - distance_point) * ind2[i]["distance"], 
                           "coeff": coeff_point * ind1[i]["coeff"] + (1 - coeff_point) * ind2[i]["coeff"]})
        offspring2.append({"node1": ind1[i]["node1"], "node2": ind1[i]["node2"], 
                           "distance": distance_point * ind2[i]["distance"] + (1 - distance_point) * ind1[i]["distance"], 
                           "coeff": coeff_point * ind2[i]["coeff"] + (1 - coeff_point) * ind1[i]["coeff"]})

    return creator.Individual(offspring1), creator.Individual(offspring2)

def custom_mutation(individual, mutpb_d, mutpb_c, mu_d, sigma_d, mu_c, sigma_c):
    mutated = []
    for i in range(len(individual)):
        distance = individual[i]["distance"]
        coeff = individual[i]["coeff"]
        if random.random() < mutpb_d:
            mutated_distance = max(0.1, min(0.9, distance + random.gauss(mu_d, sigma_d)))
        else:
            mutated_distance = distance
        if random.random() < mutpb_c:
            mutated_coeff = max(0, min(0.1, coeff + random.gauss(mu_c, sigma_c)))
        else:
            mutated_coeff = coeff
        mutated.append({"node1": individual[i]["node1"], "node2": individual[i]["node2"], "distance": mutated_distance, "coeff": mutated_coeff})
    return creator.Individual(mutated),
# Main
if __name__ == "__main__":
    
    observers = ["SW20", "HP12", "HP5", "SW/K01"]
    leaks = [{"node1": "AN4", "node2": "AN5", "distance": 0.5, "coeff": 0.05}, {"node1": "SW12", "node2": "SW13", "distance": 0.6, "coeff": 0.07}]
    add_observers(observers, base_net, observers_net)
    add_advanced_leaks(leaks, observers_net, model_net)
    os.system(f"{epanet_dir} {model_net} {model_report}")

    pipes = parse_pipes(base_net)
    creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
    creator.create("Individual", tuple, fitness=creator.FitnessMin)
    toolbox = base.Toolbox()
    toolbox.register("individual", create_individual)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    toolbox.register("evaluate", evaluate)
    toolbox.register("mate", custom_crossover)
    toolbox.register("mutate", custom_mutation, mutpb_d=0.2, mutpb_c=0.2, mu_d=0.50, sigma_d=0.40, mu_c=0.05, sigma_c=0.05)
    toolbox.register("select", tools.selBest)
    toolbox.register("map", futures.map)

    population_size = int(sys.argv[1])
    num_generations = int(sys.argv[2])
    pop = [creator.Individual(toolbox.individual()) for _ in range(population_size)]
    algorithms.eaSimple(pop, toolbox, cxpb=0.5, mutpb=0.2, ngen=num_generations, verbose=True)
    best_individual = tools.selBest(pop, k=1)[0] 
    add_advanced_leaks(best_individual, observers_net, output_net)
    os.system(f"{epanet_dir} {output_net} {output_report}")
    diff = compare_reports(model_report, output_report)
    # wykres zbieżności dla najlepszego osobnika
    for pair in best_individual :
        if pair["coeff"] > 0:
            print(pair)
    print("Difference:", diff)
