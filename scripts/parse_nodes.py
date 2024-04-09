def parse_nodes(source: str) -> list[str]:

    file_format = "inp"
    nodes = []

    if source.split(".")[-1] != file_format:
        raise Exception("Extension of source should be '.inp' !")

    with open(source, 'r') as lines:
        src_content = lines.readlines()
        index = 0
        while index < len(src_content):
            line = src_content[index]
            if "[JUNCTIONS]" in line:
                index += 2
                line = src_content[index]
                while not line.isspace():
                    node, *rest = line.split()
                    nodes.append(node)
                    index += 1
                    line = src_content[index]
            index +=1 
    return nodes

    
