def parse_pipes(source: str) -> list[tuple]:

    file_format = "inp"
    pipes = []
    reservoirs = []

    if source.split(".")[-1] != file_format:
        raise Exception("Extension of source should be '.inp' !")

    with open(source, 'r') as lines:
        src_content = lines.readlines()
        index = 0
        while index < len(src_content):
            line = src_content[index]
            if "[RESERVOIRS]" in line:
                index += 2
                line = src_content[index]
                while not line.isspace():
                    reservoirs.append(line.split()[0])
                    index += 1
                    line = src_content[index]
            if "[PIPES]" in line:
                index += 2
                line = src_content[index]
                while not line.isspace():
                    pipe, node1, node2, *rest = line.split()
                    if node1 not in reservoirs and node2 not in reservoirs:
                        pipes.append((node1, node2))
                    index += 1
                    line = src_content[index]
            index +=1 
    return pipes