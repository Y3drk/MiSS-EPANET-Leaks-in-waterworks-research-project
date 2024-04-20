def add_observers(observers: list[str], source_input_file_path: str, result_input_file_path: str) -> None:
    '''
    Adds observers to the input file REPORT section, to specify the nodes on which we want to monitor the measurements

    :param observers: a list of node (junction) IDs which we want to monitor throughout the simulation
    :param source_input_file_path: path to the original input file
    :param result_input_file_path: path where to the produced input file that includes the added observators

    If any of the observer nodes do not exist the function will throw an error.
    '''
    def collect_node(_line: str, _nodes: list[str]) -> None:
        node_id = _line.split("\t")[0].replace(" ", "")
        _nodes.append(node_id)

    input_file_format = "inp"
    nodes = []
    parse_section = {"junctions": False, "report": False}
    nodes_line_detected = False

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
                        for observer_placement in observers:
                            if observer_placement not in nodes:
                                raise Exception("One of the observers has an invalid junction id!")
                    else:
                        collect_node(line, nodes)

                if "[REPORT]" in line:
                    parse_section["report"] = True

                if parse_section["report"]:
                    if "Nodes" in line:
                        nodes_line_detected = True
                        res.write(f" Nodes\t")
                        for node in observers:
                            res.write(f"{node} ")

                        res.write("\n")

                    elif line == "\n":
                        parse_section["report"] = False
                        if not nodes_line_detected:
                            nodes_line_detected = True
                            res.write(f" Nodes\t")
                            for node in observers:
                                res.write(f"{node} ")

                        res.write("\n")

                if not parse_section["report"] or (parse_section["report"] and not nodes_line_detected):
                    res.write(line)