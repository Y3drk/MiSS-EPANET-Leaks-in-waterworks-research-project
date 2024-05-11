def collect_node(_line: str, _nodes: list[str], elev: bool = False) -> None:
    node_info = _line.split("\t")
    node_id = node_info[0].replace(" ", "")
    if elev:
        _elev = float(node_info[1].replace(" ", ""))
        _nodes.append([node_id, _elev])
    else:
        _nodes.append(node_id)


def get_fake_node_id(idx: int) -> str:
    return f"FAKE.{idx}"


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
        * the distance from the first of nodes to the newly created first node, it's a percentage of the length of initial pipe normalized to range (0, 1)
        * the value of the emitters flow coefficient to be added to the fake node
     :param source_input_file_path: path to the original input file
     :param result_input_file_path: path where to the produced input file that includes the emitters

     If any of the emitters is assigned to a non-existing node, the function will throw an error.
    '''
    input_file_format = "inp"
    nodes = []
    new_pipes = []
    parse_section = {"junctions": False, "pipes": False, "emitters": False, "tags": False, "reactions": False, "vertices": False}
    fake_nodes = {}
    previous_pipes = []
    tags, reactions = [], []
    reactions_written = False

    if source_input_file_path.split(".")[-1] != input_file_format or result_input_file_path.split(".")[-1] != input_file_format:
        raise Exception("Extension of source and result file should be '.inp' !")

    for leak in leaks:
        leak.update({"pipe_found": False})

    with open(source_input_file_path, 'r') as src:
        src_content = src.readlines()
        for line in src_content:
            if "[JUNCTIONS]" in line:
                parse_section["junctions"] = True
                continue

            if parse_section["junctions"]:
                if line == "\n":
                    parse_section["junctions"] = False
                    node_names = [node[0] for node in nodes]
                    for leak in leaks:
                        node1 = leak["node1"]
                        node2 = leak["node2"]
                        if node1 not in node_names or node2 not in node_names:
                            raise Exception(f"One of the fake nodes' parents has an invalid junction id: {node1} or {node2}!")
                else:
                    if line[0] != ";":
                        collect_node(line, nodes, elev=True)

            if "[PIPES]" in line:
                parse_section["pipes"] = True
                continue

            if parse_section["pipes"] and line[0] != ";":
                if line == "\n":
                    parse_section["pipes"] = False
                    for leak in leaks:
                        if not leak["pipe_found"]:
                            # raise Exception("There is no pipe or valve between parent nodes of one of the proposed leaks")
                            print(f"There is no pipe between nodes {leak['node1']} and {leak['node2']}")

                else:
                    pipe_info = line.split("\t")
                    node1, node2 = pipe_info[1].replace(" ", ""), pipe_info[2].replace(" ", "")
                    for idx, leak in enumerate(leaks):
                        if (leak["node1"] == node1 and leak["node2"] == node2) or (
                                leak["node1"] == node2 and leak["node2"] == node1):

                            src_content.remove(line)
                            leak["pipe_found"] = True

                            pipe_id = pipe_info[0].replace(" ", "")
                            pipe_length = float(pipe_info[3].replace(" ", ""))
                            pipe_diameter = float(pipe_info[4].replace(" ", ""))
                            pipe_roughness = float(pipe_info[5].replace(" ", ""))
                            pipe_minor_loss = float(pipe_info[6].replace(" ", ""))
                            pipe_status = pipe_info[7].replace(" ", "")
                            fake_node = get_fake_node_id(idx)
                            node1_elev, node2_elev = None, None

                            previous_pipes.append(pipe_id)

                            new_pipes.append({"id": f"FP{len(new_pipes)}", "node1": node1, "node2": fake_node,
                                              "length": pipe_length * leak["distance"], "diameter": pipe_diameter,
                                              "roughness": pipe_roughness, "minor_loss": pipe_minor_loss,
                                              "status": pipe_status})

                            new_pipes.append({"id": f"FP{len(new_pipes)}", "node1": fake_node, "node2": node2,
                                              "length": pipe_length * (1 - leak["distance"]), "diameter": pipe_diameter,
                                              "roughness": pipe_roughness, "minor_loss": pipe_minor_loss,
                                              "status": pipe_status})

                            for node, elev in nodes:
                                if node == node1:
                                    node1_elev = elev

                                elif node == node2:
                                    node2_elev = elev

                                if node1_elev is not None and node2_elev is not None:
                                    fake_nodes.update({fake_node: round(node1_elev - (node1_elev - node2_elev)* leak["distance"], 2)})
                                    break

            if "[TAGS]" in line:
                parse_section["tags"] = True
                continue

            if parse_section["tags"]:
                if line == "\n":
                    parse_section["tags"] = False

                else:
                    tag_info = line.strip().split("\t")
                    pipe_id = tag_info[1].replace(" ", "")

                    for num, removed_pipe in enumerate(previous_pipes):
                        if removed_pipe == pipe_id:
                            src_content.remove(line)
                            tags.append({"type": tag_info[0].replace(" ", ""), "pipe_id": new_pipes[2*num]["id"], "material": tag_info[2].replace(" ", "")})
                            tags.append({"type": tag_info[0].replace(" ", ""), "pipe_id": new_pipes[2 * num + 1]["id"],
                                         "material": tag_info[2].replace(" ", "")})
                            break

            if "[REACTIONS]" in line:
                parse_section["reactions"] = True
                continue

            if parse_section["reactions"] and line[0] != ";":
                if line == "\n":
                    parse_section["reactions"] = False

                else:
                    reaction_info = line.strip().split("\t")
                    pipe_id = reaction_info[1].replace(" ", "")

                    for num, removed_pipe in enumerate(previous_pipes):
                        if removed_pipe == pipe_id:
                            src_content.remove(line)
                            reactions.append({"type": reaction_info[0].replace(" ", ""), "pipe_id": new_pipes[2*num]["id"], "coefficient": reaction_info[2].replace(" ", "")})
                            reactions.append({"type": reaction_info[0].replace(" ", ""), "pipe_id": new_pipes[2 * num + 1]["id"],
                                         "coefficient": float(reaction_info[2].replace(" ", ""))})
                            break

            # if "[VERTICES]" in line:
            #     parse_section["vertices"] = True
            #     continue
            #
            # if parse_section["vertices"] and line[0] != ";":
            #     if line == "\n":
            #         parse_section["vertices"] = False
            #
            #     else:
            #         vertex_info = line.strip().split("\t")
            #         pipe_id = vertex_info[0].replace(" ", "")
            #
            #         if pipe_id in previous_pipes:
            #             src_content.remove(line)


    with open(result_input_file_path, 'w') as res:
        for line in src_content:
            if "[JUNCTIONS]" in line:
                parse_section["junctions"] = True

            if parse_section["junctions"]:
                if line == "\n":
                    parse_section["junctions"] = False
                    for _id, elev in fake_nodes.items():
                        res.write(f"{_id}\t{elev}\t0\t \t;\n")

                    res.write("\n")

                else:
                    res.write(line)

            if "[PIPES]" in line:
                parse_section["pipes"] = True

            if parse_section["pipes"]:
                if line == "\n":
                    parse_section["pipes"] = False
                    for pipe in new_pipes:
                        res.write(
                            f'{pipe["id"]}\t{pipe["node1"]}\t{pipe["node2"]}\t{pipe["length"]}\t{pipe["diameter"]}\t{pipe["roughness"]}\t{pipe["minor_loss"]}\t{pipe["status"]}\t;\n')

                    res.write("\n")

                else:
                    res.write(line)

            if "[EMITTERS]" in line:
                parse_section["emitters"] = True

            if parse_section["emitters"]:
                if line == "\n":
                    parse_section["emitters"] = False
                    emitters = {f"{node_name}": leak["coeff"] for node_name, leak in zip(fake_nodes.keys(), leaks)}
                    add_remaining_emitters(res, emitters)

                    res.write("\n")

                else:
                    res.write(line)

            if "[TAGS]" in line:
                parse_section["tags"] = True

            if parse_section["tags"]:
                if line == "\n":
                    parse_section["tags"] = False
                    for tag in tags:
                        res.write(f'{tag["type"]}\t{tag["pipe_id"]}\t{tag["material"]}\n')

                    res.write("\n")

                else:
                    res.write(line)

            if "[REACTIONS]" in line:
                parse_section["reactions"] = True

            if parse_section["reactions"]:
                if line == "\n":
                    parse_section["reactions"] = False
                    if not reactions_written:
                        for reaction in reactions:
                            res.write(f'{reaction["type"]}\t{reaction["pipe_id"]}\t{reaction["coefficient"]}\n')

                        res.write("\n")
                        reactions_written = True

                else:
                    res.write(line)

            if "[VERTICES]" in line:
                parse_section["vertices"] = True

            if parse_section["vertices"]:
                if line == "\n":
                    parse_section["vertices"] = False

            if not (parse_section["junctions"] or parse_section["emitters"] or parse_section["pipes"] or parse_section["tags"] or parse_section["reactions"] or parse_section["vertices"]):
                res.write(line)
