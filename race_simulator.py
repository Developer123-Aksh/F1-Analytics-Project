import numpy as np
import pandas as pd
import random
from config import *

class Driver:
    def __init__(self, name, skill, consistency):
        self.name = name
        self.skill = skill
        self.consistency = consistency
        self.total_time = 0
        self.dnf = False
        self.pitted = False
        self.tire_wear = 0

    def lap_time(self):
        base_time = 90

        skill_effect = self.skill * random.uniform(0.01, 0.03)
        noise = random.gauss(0, (1 - self.consistency) * 2)
        degradation = self.tire_wear * TIRE_DEGRADATION

        return base_time - skill_effect + noise + degradation


def simulate_race(file_path):
    df = pd.read_csv(file_path)

    # ✅ KEEP ONLY TOP 20 DRIVERS (REALISTIC GRID)
    df = df.sort_values(by="Points", ascending=False).head(20)

    drivers = []

    for _, row in df.iterrows():

        # 🔥 SKILL FROM REAL DATA
        skill = (
            row['Race_Wins'] * 6 +
            row['Podiums'] * 4 +
            row['Fastest_Laps'] * 2 +
            row['Points'] * 0.05 +
            row['Win_Rate'] * 100 +
            row['Podium_Rate'] * 50
        )

        consistency = min(0.95, 0.5 + row['Start_Rate'] * 0.5)

        drivers.append(
            Driver(
                row['Driver'],
                skill,
                consistency
            )
        )

    safety_car = False

    for lap in range(TOTAL_LAPS):

        # 🚨 Safety Car
        if not safety_car and random.random() < SAFETY_CAR_PROB:
            safety_car = True
            print(f"🚨 Safety Car deployed on lap {lap}")

        for driver in drivers:
            if driver.dnf:
                continue

            # 💥 DNF
            dnf_prob = BASE_DNF_PROB * (1.2 - driver.consistency)

            if random.random() < dnf_prob:
                driver.dnf = True
                print(f"❌ {driver.name} DNF on lap {lap}")
                continue

            # 🛞 Pit Stop
            if (not driver.pitted and 
                PIT_WINDOW[0] <= lap <= PIT_WINDOW[1] and 
                random.random() < 0.12):

                driver.total_time += PIT_STOP_TIME
                driver.pitted = True
                driver.tire_wear = 0
                print(f"🔧 {driver.name} pitted on lap {lap}")
                continue

            lap_time = driver.lap_time()

            if safety_car:
                lap_time += 8

            driver.total_time += lap_time
            driver.tire_wear += 1

        # 🟢 End Safety Car
        if safety_car and random.random() < 0.25:
            safety_car = False
            print(f"🟢 Safety Car ended on lap {lap}")

    # 🏁 Final Results
    finished = [d for d in drivers if not d.dnf]

    results = sorted(finished, key=lambda x: x.total_time)

    return results