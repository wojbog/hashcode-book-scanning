# Combinatorial optimization

## Authors:
### Wojciech Bogacz 156034, Krzysztof Skrobała 156039
#### student group 2

## Python version
Python 3.11.3

## Method outline
Firstly, we tried local search algorithm, but for obious reason, the results weren't satisfactory - one neighbour was defined as swap between 2 neigbouring libraries. As a result, the neigbourhood size was 10^6 in the worst case, what was very slow and ineffective.

Then, we tried genetic approach. The results were better, however, after profiling the times of executions of different functions we came to conlusion that our score counting funtion was the slowest part of the allgorithm and in genetic approach heavly uses this function. 

Then, we tried a simple heauristic, which worked pretty well. Because it was very fast, we decided to make it more precise. It resulted in the best scores. Sometimes if the time of calculation exceeds 5 minutes, we finished the solutiuon with first heuristic. At the end, for tunning the score we perform local search starting from the heuristic generated solution.

## Implementation part
In heuristic function we used greedy approach. First, We have to choose the best library for the days left, then we update days left by adding time of the signup process of chosen library and at the end we mark chosen library and books as taken to not duplicate them in the next iteration. We perform this algorithm in loop for all libraries. We rank libraries according to: *the best available books / signup process*.

## Conlusions
We are surprised that different alghorithms give worse results than the greedy approach. From this project, We learned that it is worth to test different aproaches including simple one. We can't apply the algorithm and see the results. Different problems require different solutions, therefore we have to learn as many as posible different algorithms, because we don't know what type of the problem might happen in the future.