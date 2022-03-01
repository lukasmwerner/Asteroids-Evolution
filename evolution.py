import simulation
from objects import *
import NeuralNet as nn
import copy
import multiprocessing
from multiprocessing import Pool
from functools import partial
import json
import pickle

if __name__ == "__main__":
    scoresOverTime = []
    generation = 1
    populationCount = 50
    population = [AISpaceship(brain=nn.Brain([0 for i in range(24)], [0,0,0,0,0])) for _ in range(0,populationCount)]
    mode = "m"
    while mode == "m" or mode == "s":
        try:
            results = []
            print(f"Generation: {generation}")
            if mode == "m":
                pool = Pool(2)
                results = pool.map(simulation.run, population)
                pool.close()
                pool.join()
            else:
                for player in population:
                    results.append(simulation.run(player))
            results = sorted(results, key=lambda k: k['score'], reverse=True)
            best = results[0]
            maxScore = best['score']
            print(f"Best Score: {best['score']}")
            newPopulation = [copy.deepcopy(best['player']) for player in results]
            for player in newPopulation:
                player.mutate(random.randrange(0,3))
            newPopulation[0] = best['player']
            population = newPopulation
            if maxScore <= 60:
                mode = "m"
            elif maxScore >= 100:
                mode = "s"
            if maxScore >= 100:
                mode = input("Mode ((s)ingle/(M)ulti/(q)uit): ").lower() or "m"
            scoresOverTime.append(maxScore)
            with open(f"checkpoints/checkpoint-gen-{generation}.pk", "wb") as f:
                pickle.dump(best['player'], f)
            with open("socresOverTime.json", 'w') as f:
                json.dump(scoresOverTime, f)
            generation +=1
        except KeyboardInterrupt as e:
            break