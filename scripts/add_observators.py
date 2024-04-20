def add_observators(observators: list[str], source_input_file_path: str, result_input_file_path: str) -> None:
    '''
    Adds observators to the input file REPORT section, to specify the nodes on which we want to monitor the measurements

    :param observators: a list of node (junction) IDs which we want to monitor throughout the simulation
    :param source_input_file_path: path to the original input file
    :param result_input_file_path: path where to the produced input file that includes the added observators

    If any of the observator nodes do not exist the function will throw an error.
    '''
    pass