We have implemented the following changes to our algorithm:
- we introduced concurrency using the scoop library (parallelizing the evaluation function across all logical processor cores)
- we changed the crossover function: for each attribute of an individual, we draw two division points (one for distance, one for coefficient) and according to this we copy the values from the parents to the two descendants (symmetrically, of course)
- we added saving the best score of an individual in the population after each iteration 