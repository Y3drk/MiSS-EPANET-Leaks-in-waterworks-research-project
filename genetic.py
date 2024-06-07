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
import glob

min_leak_coefficient = 0.0 
max_leak_coefficient = 0.1

script_dir = str(pathlib.Path(__file__).parent.resolve())
files_dir = script_dir + "/knowledge_sources/real_life_network_data/"
# locally
epanet_dir = script_dir + "/EPANET-2.2.0-Linux/bin/runepanet"
# on plgrid cluster
# epanet_dir = "runepanet"
base_net = f"{files_dir}base.inp"
observers_net = f"{files_dir}observers.inp"
model_net = f"{files_dir}model.inp"
output_net = f"{files_dir}genetic-{threading.get_ident()}.inp"
model_report = f"{files_dir}model.txt"
output_report = f"{files_dir}genetic-{threading.get_ident()}.txt"
results_file = f"{files_dir}best_individual.txt"
plot_file = f"{files_dir}best_individuals.jpg"

def create_individual():
    network = []
    for pair in pipes:
        node1, node2 = pair
        distance = random.uniform(0.1, 0.9)
        coefficient = random.uniform(min_leak_coefficient, max_leak_coefficient)
        network.append({"node1": node1, "node2": node2, "distance": distance, "coeff": coefficient})
    return creator.Individual(network)

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

def main(population_size, num_generations):   
    observers = ["SW20", "HP12", "HP5", "SW/K01"]
    leaks = [{"node1": "AN4", "node2": "AN5", "distance": 0.5, "coeff": 0.05}, {"node1": "SW12", "node2": "SW13", "distance": 0.6, "coeff": 0.07}]
    add_observers(observers, base_net, observers_net)
    add_advanced_leaks(leaks, observers_net, model_net)
    os.system(f"{epanet_dir} {model_net} {model_report}")
    
    global pipes
    pipes = parse_pipes(base_net)
    creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMin)
    toolbox = base.Toolbox()
    toolbox.register("individual", create_individual)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    toolbox.register("evaluate", evaluate)
    toolbox.register("mate", custom_crossover)
    toolbox.register("mutate", custom_mutation, mutpb_d=0.2, mutpb_c=0.2, mu_d=0, sigma_d=0.40, mu_c=0, sigma_c=0.05)
    toolbox.register("select", tools.selBest)
    toolbox.register("map", futures.map)

    pop = toolbox.population(n=population_size)
    best_individuals = []

    for gen in range(num_generations):
        offspring = algorithms.varAnd(pop, toolbox, cxpb=0.5, mutpb=0.2)
        fits = toolbox.map(toolbox.evaluate, offspring)

        for fit, ind in zip(fits, offspring):
            ind.fitness.values = fit

        pop[:] = toolbox.select(offspring + pop,k=population_size)
        best_ind = tools.selBest(pop, k=1)[0]
        best_individuals.append(best_ind.fitness.values[0])

    plt.plot(range(num_generations), best_individuals)
    plt.xlabel('Generation')
    plt.ylabel('Best Individual Fitness')
    plt.title('Best Individual Fitness per Generation')
    plt.savefig(plot_file)

    best_individual = tools.selBest(pop, k=1)[0] 
    add_advanced_leaks(best_individual, observers_net, output_net)
    os.system(f"{epanet_dir} {output_net} {output_report}")
    diff = compare_reports(model_report, output_report)
    with open(results_file, "w") as f:
        for pair in best_individual:
            if pair["coeff"] > 0:
                f.write(f"{pair}\n")
    print("Results saved to results.txt")
    print("Difference:", diff)
    files_to_remove = glob.glob(f"{files_dir}/genetic*") + glob.glob(f"{files_dir}/model*") + glob.glob(f"{files_dir}/observers*")
    for file_path in files_to_remove:
        try:
            os.remove(file_path)
        except Exception as e:
            print(f"Error deleting file {file_path}: {e}")

if __name__ == "__main__":
    population_size = int(sys.argv[1])
    num_generations = int(sys.argv[2])
    main(population_size, num_generations)
