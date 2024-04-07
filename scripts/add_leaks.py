def add_leaks(leaks: dict[str, float], source_input_file_path:str, result_input_file_path:str) -> None:
    '''Adds emitters that simulate leaks to the current contents of the EPANET input file, creating a new one that the user can pass as an argument to the runepanet CLI command.

     :param leaks: dictionary of emitters where the key is the ID of a node (junction) we want to add the emitter to and the value is the flow coefficient of the emitter
     :param source_input_file_path: path to the original input file
     :param result_input_file_path: path where to the produced input file that includes the emitters

     If any of the emitters is assigned to a non-existing node, the function will throw an error.
    '''
    nodes = []
    emitters_section_present = False

    with open(source_input_file_path, 'r', encoding="utf-8") as src:
        with open(result_input_file_path, 'w', encoding="utf-8") as res:
            pass
        pass
