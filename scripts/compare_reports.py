from math import sqrt
from statistics import mean

def compare_reports(first_report: str, second_report: str) -> float:

    file_format = "txt"
    first_nodes = {}
    second_nodes = {}

    if first_report.split(".")[-1] != file_format or second_report.split(".")[-1] != file_format:
        raise Exception("Extension of first and second file should be '.txt' !")

    with open(first_report, 'r') as first, open(second_report, 'r') as second:
        src_content = first.readlines()
        index = 0
        while index < len(src_content):
            line = src_content[index]
            if "L/s" in line:
                index += 2
                line = src_content[index]
                while not line.isspace() or "Reservoir" in line:
                    node, demand, head, pressure, *rest = line.split()
                    if(first_nodes.get(node) is None):
                        first_nodes[node] = []
                    first_nodes[node].append(float(pressure))
                    index += 1
                    line = src_content[index]
            index +=1 
        src_content = second.readlines()
        index = 0
        while index < len(src_content):
            line = src_content[index]
            if "L/s" in line:
                index += 2
                line = src_content[index]
                while not line.isspace() or "Reservoir" in line:
                    node, demand, head, pressure, *rest = line.split()
                    if(second_nodes.get(node) is None):
                        second_nodes[node] = []
                    second_nodes[node].append(float(pressure))
                    index += 1
                    line = src_content[index]
            index +=1 
    
    diff = {}
    for node in first_nodes:
        if second_nodes.get(node) is not None:
            diff[node] = sum([(first_nodes[node][i] - second_nodes[node][i])**2 for i in range(len(first_nodes[node]))])/len(first_nodes[node])
        else:
            print(f"Node {node} not found in second report")
            exit(1)
    return sum(diff.values())/len(diff) if len(diff) > 0 else 0