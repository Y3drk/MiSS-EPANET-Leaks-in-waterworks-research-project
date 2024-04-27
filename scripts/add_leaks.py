def collect_node(_line: str, _nodes: list[str], elev: bool = False) -> None:
    node_info = _line.split("\t")
    node_id = node_info[0].replace(" ", "")
    if elev:
        _elev =  float(node_info[1].replace(" ", ""))
        _nodes.append([node_id, _elev])
    else:
        _nodes.append(node_id)


def get_fake_node_id(idx: int) -> str:
    return f"FAKE/{idx}"

def add_remaining_emitters(file_handle, remaining_emitters: dict[str, float]) -> None:
    for node_id, coeff in remaining_emitters.items():
        file_handle.write(f"{node_id}\t{coeff}\n")

def parse_emitters(file_handle, _line: str, _emitters: dict[str, float]) -> None:
    node_id, curr_coeff = _line.split("\t")
    node_id = node_id.replace(" ", "")
    if node_id in list(_emitters.keys()):
        matching_emitter_coeff = _emitters.pop(node_id.replace(" ", ""))
        new_coeff = float(curr_coeff.strip().replace(" ", "")) + matching_emitter_coeff
        file_handle.write(f"{node_id}\t{new_coeff}\n")
    else:
        file_handle.write(_line)

def add_leaks(leaks: dict[str, float], source_input_file_path: str, result_input_file_path: str) -> None:
    '''Adds emitters that simulate leaks to the current contents of the EPANET input file, creating a new one that the user can pass as an argument to the runepanet CLI command.

     :param leaks: dictionary of emitters where the key is the ID of a node (junction) we want to add the emitter to and the value is the flow coefficient of the emitter
     :param source_input_file_path: path to the original input file
     :param result_input_file_path: path where to the produced input file that includes the emitters

     If any of the emitters is assigned to a non-existing node, the function will throw an error.
    '''

    input_file_format = "inp"
    nodes = []
    parse_section = {"junctions": False, "emitters": False}

    if source_input_file_path.split(".")[-1] != input_file_format or result_input_file_path.split(".")[
        -1] != input_file_format:
        raise Exception("Extension of source and result file should be '.inp' !")

    with open(result_input_file_path, 'w') as res:
        with open(source_input_file_path, 'r') as src:
            src_content = src.readlines()
            for line in src_content:
                if "[JUNCTIONS]" in line:
                    parse_section["junctions"] = True

                if parse_section["junctions"]:
                    if line == "\n":
                        parse_section["junctions"] = False
                        for emitter_placement in leaks.keys():
                            if emitter_placement not in nodes:
                                raise Exception("One of the emitters has an invalid junction id!")
                    else:
                        collect_node(line, nodes)

                if parse_section["emitters"] and ";" not in line:
                    if line == "\n":
                        parse_section["emitters"] = False
                        add_remaining_emitters(res, leaks)
                    else:
                        parse_emitters(res, line, leaks)

                if "[EMITTERS]" in line:
                    parse_section["emitters"] = True
                    res.write(line)
                    res.write(";Junction\tCoefficient\n")

                if not parse_section["emitters"]:
                    if len(leaks) > 0 and "[END]" in line:
                        res.write("[EMITTERS]\n;Junction\tCoefficient\n")
                        add_remaining_emitters(res, leaks)
                        res.write("\n")

                    res.write(line)


def add_advanced_leaks(leaks: list[dict], source_input_file_path: str, result_input_file_path: str) -> None:
    '''Adds an advanced version of leaks, by adding a fake node with an emitter in a specified distance between two nodes passed as arguments to the current contents of the EPANET input file,
    creating a new one that the user can pass as an argument to the runepanet CLI command.

    Important: We assume that those fake nodes only exist to be a hole and nothing more. Therefore, they have no pattern attached and their demand is equal to 0.
    Also, if between the nodes was a valve, we create a pipe from the node1 to fake node, and then we copy the valve from the fake node to the node2. <- TBD

     :param leaks: list of where a fake node should be placed. The list consists of dicts, where each contains:
        * two IDs of a nodes (junctions) we want to add the fake node in between,
        * the distance from the first of nodes to the newly created first node,
        the value of the emitters flow coefficient to be added to the fake node
     :param source_input_file_path: path to the original input file
     :param result_input_file_path: path where to the produced input file that includes the emitters

     If any of the emitters is assigned to a non-existing node, the function will throw an error.
    '''
    input_file_format = "inp"
    nodes = []
    new_pipes, new_valves = [], []
    parse_section = {"junctions": False, "pipes": False, "valves":False, "emitters": False}
    average_elevations = []

    if source_input_file_path.split(".")[-1] != input_file_format or result_input_file_path.split(".")[
        -1] != input_file_format:
        raise Exception("Extension of source and result file should be '.inp' !")

    for leak in leaks:
        leak.update({"pipe_found": False})


    with open(source_input_file_path, 'r') as src:
        src_content = src.readlines()
        for line in src_content:
            if "[JUNCTIONS]" in line:
                parse_section["junctions"] = True

            if parse_section["junctions"]:
                if line == "\n":
                    parse_section["junctions"] = False
                    node_names = [node[0] for node in nodes]
                    for leak in leaks:
                        node1 = leak["node1"]
                        node2 = leak["node2"]
                        if node1 not in node_names or node2 not in node_names:
                            raise Exception("One of the fake nodes' parents has an invalid junction id")
                else:
                    collect_node(line, nodes, elev=True)

            if "[PIPES]" in line:
                parse_section["pipes"] = True

            if parse_section["pipes"]:
                # TODO: when reading source delete current pipe/valve between two nodes and insert two pipes node1----fake_node and fake_node---node2
                # TODO count average elevations
                pipe_info = line.split("\t")
                node1, node2 = pipe_info[1].replace(" ", ""), pipe_info[2].replace(" ", "")
                for leak in leaks:
                    if (leak["node1"] == node1 and leak["node2"] == node2) or (leak["node1"] == node2 and leak["node2"] == node1):
                        src_content.remove(line)
                        pipe_length = float(pipe_info[3].replace(" ", ""))

                        if pipe_length < leak["distance"]:
                            raise Exception(f"The pipe between nodes {node1} and {node2} is to short ({pipe_length}m) to apply a fake node in a given distance ({leak['distance']}m)")

                        new_pipes.append({"id": f"FP{len(new_pipes)}", "node1": node1, "node2": node2, "length": pipe_length, "diameter": 0}) #TODO: complete this

                if line == "\n":
                    for leak in leaks:
                        if not leak["pipe_found"]:
                            raise Exception("There is no pipe or valve between parent nodes of one of the proposed leaks")

            if "[VALVES]" in line:
                parse_section["valves"] = True

            if parse_section["valves"]:
                # TODO: when reading source delete current pipe/valve between two nodes and insert two pipes node1----fake_node and fake_node---node2
                # TODO count average elevations
                pass


    with open(result_input_file_path, 'w') as res:
        for line in src_content:
            if "[JUNCTIONS]" in line:
                parse_section["junctions"] = True
                res.write(line)

            if parse_section["junctions"]:
                if line == "\n":
                    for num, leak in enumerate(leaks):
                        res.write(f"{get_fake_node_id(num)}\t{average_elevations[num]}\t0\t \t;\n")

                    res.write("\n")

                else:
                    res.write(line)

            if "[PIPES]" in line:
                parse_section["pipes"] = True
                res.write(line)

            if parse_section["pipes"]:
                if line == "\n":
                    for pipe in new_pipes:
                        res.write(f"{pipe["id"]}\t{pipe["node1"]}\t{pipe["node2"]}\t{pipe["length"]}\t{pipe["diameter"]}\t{pipe["roughness"]}\t{pipe["minor_loss"]}\t{pipe["status"]}\t;\n")

                else:
                    res.write(line)

            if "[VALVES]" in line:
                parse_section["valves"] = True
                res.write(line)

            if parse_section["valves"]:
                if line == "\n":
                    for valve in new_valves:
                        res.write(f"{valve["id"]}\t{valve["node1"]}\t{valve["node2"]}\t{valve["diameter"]}\t{valve["type"]}\t{valve["setting"]}\t{valve["minor_loss"]}\t;\n")

                else:
                    res.write(line)

            if "[EMITTERS]" in line:
                parse_section["emitters"] = True
                res.write(line)

            if parse_section["emitters"]:
                if line == "\n":
                    parse_section["emitters"] = False
                    add_remaining_emitters(res, {f"{get_fake_node_id(idx)}": node["coeff"] for idx, node in enumerate(leaks)})
                else:
                    res.write(line)

            if not (parse_section["junctions"] or parse_section["emitters"] or parse_section["pipes"] or parse_section["valves"]):
                res.write(line)



