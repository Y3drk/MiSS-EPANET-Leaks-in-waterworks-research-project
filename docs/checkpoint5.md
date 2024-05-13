# Checkpoint 5 - Progress with the prototype

### Confirmed scope of work
As discussed, the work to be performed for this checkpoint includes the following tasks:
1. Finish the work regarding the addition of advanced leaks to the input file:
   * Check if junctions connected with valves are essentially two nodes in the same place. If yes, ignore such cases when adding leaks
   * Change the **"distance"** parameter from physical length in meters to a percentage of the length of the initial pipe (normalized to range (0,1))
   * Calculate the elevation of the fake nodes and clean-up the file so the simulation runs without errors
2. Run optimization algorithm with different kinds of **"individuals"**:
   * Where an **individual is a single junction** (as before). In this scenario we should also include some heuristic that "kills of" the nodes that do not contribute with their coefficients to the leak.
   * Where an **individual is a whole network** (new approach). This technique is meant to allow us to create a more sophisticated crossover function, thus allowing us to pass certain network characteristics better.

It is also important to mention that with the advanced leaks the format of the solution also changes from **[node_id, coefficient]** to **[node_1, node_2, distance from node1 to a leak, leak coefficient]**. 
This makes the problem harder to solve but also able to provide much more detailed results of the leakage search.
___

### Further work on advanced leaks
First of all it was confirmed that the junctions connected with valves are essentially the same node, thus such cases were ignored when adding advanced leaks, 
limiting the additions only to nodes that have a pipe between them.

Later the distance parameter was changed as described in the previous section, the new implementation also included the calculation of elevation of the fake nodes simulating the leakages. 

During the works we've discovered that there are several other sections fo the input file that need changing, namely **TAGS**, **REACTIONS** and **VERTICES**.
In the case of the first two it was necessary to remove the original pipe between passed nodes and replace them with newly created pipes, from node1 to the leakage (fake node) and from the leakage to the node2.
Those new pipes had their data, ex. material they are made of in TAGS, copied from the original ones. As for the last section, it's not necessary when running the simulation as a console application, thus it was simply omitted in the updated input file.

The function is named `add_advanced_leaks` and is located in [add_leaks.py](../scripts/add_leaks.py).

The function was tested for basic scenarios such as:
* non-existing node as one of the parent nodes of leakage
* no pipe between existing parent nodes
* correct input data

The script behaves as expected in all those cases, and the `runepanet` command runs without trouble with new input file.

___
### Testing optimization for advanced leaks and different kinds of "individuals"

New function of leaks addition needed few adjustments. First, we changed evaluation algorithm's individual from singular leak to a whole network, as the genetic algorithm needs to compare individuals with common genes. Secondly, as we decide to add leaks by choosing place on pipe between nodes, we now need to pass all possible pipes instead of nodes as input for optimization. Initially, we randomly assigned coeff and distance values to each pipe we read from base input net and then run EPANET simulation. The results were then used to evaluate the network.

Another thing was invliad crossover function. Average of two unrelated nodes from previous checkpoint was not the smartest thing we come up to. Now, having proper structure of arguments for algorithm, we tried two approaches:
* take the first half of the first network and the second half of the second network. This way we can see if the algorithm is able to pass some network characteristics to the next generation
* take the minimums of the both network for one offspring, and maximums for the other. This way we can see if the algorithm is able to find the best solution by combining the best parts of the networks.

Unfortunately the results were dire. First approach, no matter what population or number of iterations we chose, returned best solution between 500 and 700. Second one was much better with score around 0.0017, but neither of 'real leaks' was distinguished with proper coeff or distance (sometimes even the coeff was 0), while the all other potential leaks were highlighted with siginificant coeff values. 

Due to poor results, we decide to back to basic optimization algorithm from scipy lib and try it one more time. Initial positions for algorithm were randomly chosen coeff and distance for each possible pipe and the method was set to 'L-BFGS-B'. 

Unfortunately, the output was even worse. Despite script worked for few hours, the result diff was around 550 and none of real leaks were distinguished.

Results of the tests are stored in [knowledge_sources/checkpoint5_results](../knowledge_sources/checkpoint5_results/) folder.

Not gonna lie, we are a bit disappointed with the results. We are not sure if the problem lies in the optimization algorithm or in our objective function (diff between real and calculated leaks). We will try to find the solution in the next checkpoint.