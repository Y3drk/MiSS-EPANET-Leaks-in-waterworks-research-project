from scripts.add_leaks import add_leaks

if __name__ == "__main__":
    source = "D:\sem8\MiSS\projekt\MiSS-EPANET-Leaks-in-waterworks-research-project\knowledge_sources\\real_life_network_data\\1_1.inp"
    result = "D:\sem8\MiSS\projekt\MiSS-EPANET-Leaks-in-waterworks-research-project\knowledge_sources\\real_life_network_data\\add_emitters_test.inp"
    emitters = {"RED1":0.02, "SW2": 0.05}
    add_leaks(emitters, source, result)