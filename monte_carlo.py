import numpy as np

def simulate_multiple_races(drivers, probabilities, simulations=1000):
    results = {driver: 0 for driver in drivers}

    for _ in range(simulations):
        winner = np.random.choice(drivers, p=probabilities)
        results[winner] += 1

    for driver in results:
        results[driver] /= simulations

    return results