# This application simulates the game of craps and displays statistics about wins and loses.

import random
import argparse

# Specify flags that can be used to modify the applications functionalty
#   For more information: https://docs.python.org/3/library/argparse.html
parser = argparse.ArgumentParser(description="Simulate a set number of graps games")
parser.add_argument('-g', '--games', type=int, metavar='G', required=True, help="Specify the number of games to simulate")

group = parser.add_mutually_exclusive_group()
group.add_argument('-s', '--streaks', action='store_true', help='Display only data on longest win and lose streaks')
group.add_argument('-q', '--quiet', action='store_true', help="Display only win/lose data")

args = parser.parse_args()

# Simulates the roll of a die
#   @returns a random number between 1 and 6
def rollDie( ):
    return random.randint(1, 6)

# Simulates a roll of two dice
#   @returns sum of the two dice
def firstRoll():
    return rollDie() + rollDie()

# Checks to see if the roll results in an instant lose
#   If you roll either a 7 or 11 on the first roll, then the result is a loss
def instantLose(sum):
    if (sum == 7) or (sum == 11):
        return True
    else:
        return False

# Checks to see if the roll results in an instant win
#   If you roll either a 2 or a 3 on the first roll, then the result is a win
def instantWin(sum):
    if (sum == 2) or (sum == 3):
        return True
    else:
        return False

# Checks to see if the first roll won, lost, or made a point
#   @return -1 if the game was a loss, 0 is the game was a win, the point if a point was made
def getPoint(sum):
    if instantLose(sum):
        return -1
    if instantWin(sum):
        return 0
    return sum

# Simulates a game of craps
#   @return the result of the game in a string [Win | Lose]
def craps():
    roll = getPoint(firstRoll())
    if roll == 0:
        return "Win"
    elif roll == -1:
        return "Lose"
    else:
        " If a point has been made, roll over and over again until the point is matched or a 7 is made"
        gameOver = False
        while not gameOver:
            newRoll = firstRoll()
            if newRoll == 7:
                return "Win"
            elif roll == newRoll:
                return "Lose"

# Counts the wins/losses and the win/lose streaks
#   @args array: an array containing the results of craps games simulations
#   @return a tuple containing the aforementioned information in the following format:
#       (win, lose, longest_win_streak, longest_lose_streak)
def count(array):
    # Set all data to null and zero to start
    win, lose, current_win_streak, longest_win_streak, current_loss_streak, longest_loss_streak = 0, 0, 0, 0, 0, 0
    prev_result = None

    # Loop thought all game results and add them up to present meaningful data
    for i in range(len(array)):
        # Covers the base case where prev_result is null
        if prev_result is None:
            prev_result = array[i]
            if array[i] == "Win":
                win = win + 1
                current_win_streak = 1
            else:
                lose = lose + 1
                current_loss_streak = 1

        # Handles a win
        elif array[i] == "Win":
            win = win + 1

            # Check if we are in a streak
            if prev_result == "Win":
                current_win_streak = current_win_streak + 1
            else:
                current_win_streak = 1

        # Handles a loss
        else:
            lose = lose + 1

            # Check if we are in a streak
            if prev_result == "Lose":
                current_loss_streak = current_loss_streak + 1
            else:
                current_loss_streak = 1

        prev_result = array[i]

        # Check if the current streak is the new longest
        if current_win_streak > longest_win_streak:
            longest_win_streak = current_win_streak
        if current_loss_streak > longest_loss_streak:
            longest_loss_streak = current_loss_streak

    # Display the data we collected to the user
    return win, lose, longest_win_streak, longest_loss_streak

# Displays the results of the simulation ot the user
#   @param count_tuple: The tuple that contains the simulation data
#   @bool quiet: if true only display win/lose data
#   @bool streaks: if true only display streak data
def display(count_tuple, quiet, streaks):
    # Because streaks and quite are mutually exclusive, they cannot both be True at the same time
    #   but they can both be false at the same time
    if not (streaks):
        print("Wins: " + str(count_tuple[0]))
        print("Losses: " + str(count_tuple[1]))
    elif not (quiet):
        print("Longest win streak: " + str(count_tuple[2]))
        print("longest lose streak: " + str(count_tuple[3]))

# Run the craps simulation a set number of times
#   @return an array containing the results of the craps simulations in the form:
#       ["Win", "Lose", "Lose", "Win", "Win"]
def run(number_of_games):
    results = []
    for i in range(1, number_of_games + 1):
        results.append(craps())
    return results

# Main routine
if __name__ == '__main__':
    results = run(args.games)
    display(count(results), args.quiet, args.streaks)
