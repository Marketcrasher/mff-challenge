import random
import math

def single_challenge_simulation(win_rate=0.70):
    total_trades = 0
    consecutive_losses = 0

    def execute_trade(account_balance, risk_percent, reward_percent=0.5):
        rand_num = random.uniform(0, 1)
        trade_amount = account_balance * risk_percent
        reward_amount = trade_amount * reward_percent

        if rand_num <= win_rate:
            return account_balance + reward_amount, 0
        else:
            return account_balance - trade_amount, 1

    def eval_loop(account_balance, target_profit):
        trades = 0
        nonlocal consecutive_losses
        while account_balance - 200000 < target_profit and account_balance - 200000 > - 24000:
            risk_percent = 0.03 if consecutive_losses >= 2 else 0.045
            account_balance, loss_flag = execute_trade(account_balance, risk_percent)
            consecutive_losses = consecutive_losses + 1 if loss_flag else 0
            trades += 1
        return account_balance - 200000 >= target_profit, trades

    eval1_success, trades1 = eval_loop(200000, 16000)
    eval2_success, trades2 = eval_loop(200000, 10000)
    total_trades = trades1 + trades2

    return eval1_success and eval2_success, total_trades



def monte_carlo_simulation_200k(num_simulations=100):
    successful_challenges = 0
    failed_challenges = 0
    total_successful_trades = 0
    
    for _ in range(num_simulations):
        success, trades = single_challenge_simulation()
        if success:
            successful_challenges += 1
            total_successful_trades += trades
        else:
            failed_challenges += 1

    prob_success_single_challenge = successful_challenges / num_simulations
    avg_challenges_needed_for_200k_raw = 2 / prob_success_single_challenge
    avg_challenges_needed_for_200k = math.ceil(avg_challenges_needed_for_200k_raw) if avg_challenges_needed_for_200k_raw % 1 >= 0.1 else math.floor(avg_challenges_needed_for_200k_raw)

    # Average cost considering the refunds for successful challenges
    avg_total_cost = (avg_challenges_needed_for_200k - 2) * 675
    
    avg_trades_per_successful_challenge = total_successful_trades / successful_challenges if successful_challenges > 0 else "N/A"

    print(f"The probability of passing a single challenge (Evaluation 1 and 2) is {prob_success_single_challenge:.4f}")
    print(f"Average number of challenges needed to get $200,000 funded is {avg_challenges_needed_for_200k}")
    print(f"Average total cost to get $200,000 funded is ${avg_total_cost:.2f}")
    print(f"Average number of trades per successful challenge is {avg_trades_per_successful_challenge}")

monte_carlo_simulation_200k()


