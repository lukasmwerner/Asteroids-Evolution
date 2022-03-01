import simulation
from objects import *
import NeuralNet as nn

if __name__ == "__main__":
    import sys 
    import pickle
    args = sys.argv[1]
    with open(args, "rb") as f:
        player = pickle.load(f)
    simulation.run(player)