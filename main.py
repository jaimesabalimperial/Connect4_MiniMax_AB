import sys

import simulation as sim

if __name__ == '__main__':
    simulations = [
        sim.ManualVsManualSimulation(),
        sim.ManualVsMiniMaxSimulation(),
        sim.ManualVsAlphaBetaSimulation(),
        sim.AutomaticVsAutomaticSimulation(),
    ]
    
    index = 0
    
    # read index from command line. Defaults to 0 (manual)
    if len(sys.argv) > 1:
        try:
            index = int(sys.argv[1])
        except ValueError:
            index = 0
            
    simulation = simulations[index]
    simulation.run()
