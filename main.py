from race_simulator import simulate_race
from probability_engine import calculate_probabilities
from monte_carlo import simulate_multiple_races
from statistics_analysis import dataset_stats

def main():
    file_path = "F1Drivers_Dataset.csv"

    # 📊 Dataset Stats
    print("📊 Dataset Stats:")
    stats = dataset_stats(file_path)
    for key, value in stats.items():
        print(f"{key}: {value}")

    # 🏁 Race Simulation
    print("\n🏁 Running Realistic Race Simulation...\n")
    race_results = simulate_race(file_path)

    print("\n🏁 TOP 10 RACE RESULTS:\n")
    for i, driver in enumerate(race_results[:10]):
        print(f"{i+1}. {driver.name} - {round(driver.total_time, 2)}s")

    print(f"\n🥇 Winner: {race_results[0].name}")

    # 📈 Probability Prediction
    print("\n📈 TOP 10 WIN PROBABILITIES:\n")

    df = calculate_probabilities(file_path)
    drivers = df['Driver'].tolist()
    probs = df['probability'].tolist()

    mc_results = simulate_multiple_races(drivers, probs, 5000)

    sorted_mc = sorted(mc_results.items(), key=lambda x: x[1], reverse=True)

    for i, (driver, prob) in enumerate(sorted_mc[:10]):
        print(f"{i+1}. {driver}: {round(prob*100, 2)}%")

    print(f"\n🔮 Predicted Champion: {sorted_mc[0][0]}")


if __name__ == "__main__":
    main()