def collect_node(_line: str, _nodes: list[str], elev: bool = False) -> None:
    node_info = _line.split("\t")
    node_id = node_info[0].replace(" ", "")
    if elev:
        _elev = float(node_info[1].replace(" ", ""))
        _nodes.append([node_id, _elev])
    else:
        _nodes.append(node_id)

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
