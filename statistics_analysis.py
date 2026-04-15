import pandas as pd

def dataset_stats(file_path):
    df = pd.read_csv(file_path)

    # ✅ Create skill using REAL columns
    df['Skill'] = (
        df['Race_Wins'] * 6 +
        df['Podiums'] * 4 +
        df['Fastest_Laps'] * 2 +
        df['Points'] * 0.05 +
        df['Win_Rate'] * 100 +
        df['Podium_Rate'] * 50
    )

    return {
        "Total Drivers": len(df),
        "Avg Skill": round(df['Skill'].mean(), 2),
        "Max Skill": round(df['Skill'].max(), 2)
    }