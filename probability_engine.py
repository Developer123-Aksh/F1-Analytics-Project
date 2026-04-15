import pandas as pd

def calculate_probabilities(file_path):
    df = pd.read_csv(file_path)

    # 🔥 Create skill using REAL dataset columns
    df['score'] = (
        df['Race_Wins'] * 6 +
        df['Podiums'] * 4 +
        df['Fastest_Laps'] * 2 +
        df['Points'] * 0.05 +
        df['Win_Rate'] * 100 +
        df['Podium_Rate'] * 50
    )

    # Normalize into probability
    total_score = df['score'].sum()
    df['probability'] = df['score'] / total_score

    return df[['Driver', 'probability']]