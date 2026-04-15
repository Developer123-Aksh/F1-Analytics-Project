def risk_of_ruin(bankroll, bet_size, win_prob):
    loss_prob = 1 - win_prob
    return (loss_prob / win_prob) ** (bankroll / bet_size)