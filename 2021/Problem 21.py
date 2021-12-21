

p1_position = 10 - 1
p2_position = 2 - 1
#sample input
# p1_position = 4 - 1
# p2_position = 8 - 1

p1score = 0
p2score = 0

number_of_dice_rolls = 0
deterministic_die_value = -1
def get_die():
    global deterministic_die_value, number_of_dice_rolls
    deterministic_die_value += 1
    deterministic_die_value = deterministic_die_value % 100
    number_of_dice_rolls += 1
    return deterministic_die_value + 1

while True:
    p1_position += get_die() + get_die() + get_die()
    p1_position = p1_position % 10
    
    p1score += p1_position + 1 # positions are 1-indexed!
    
    if p1score >= 1000:
        print("Player 1 wins!")
        print("Score is %s" % (p2score * number_of_dice_rolls))
        break
        
        
    p2_position += get_die() + get_die() + get_die()
    p2_position = p2_position % 10
    
    p2score += p2_position + 1 # positions are 1-indexed!
    
    if p2score >= 1000:
        print("Player 2 wins!")
        print("Score is %s" % (p1score * number_of_dice_rolls))
        break
    
#############################################
"""
Thinking about distributions, there are 27 ways to roll 3 dice:
3=1+1+1 (1)
4=1+1+2, 1+2+1, 2+1+1 (3)
5=1+1+3 * 3, 1+2+2*3 (6)
6 (7)
7 (6)
8 (3)
9=3+3+3 (1)

When we roll the die, we can create a distribution map of scores.
A players score and position are a self-contained state, we need no additional
information to travel from there.

Therefore we can create a hash with:
player1pos * player2pos * player1score * player2score * whose_turn
= 10 * 10 * 21 * 21 * 2 = 88200 or so possibilities.

That's actually a hash we can store in memory.
"""
from collections import defaultdict, Counter
import itertools

dirac_three_dice_rolls = list(Counter([sum(x) for x in itertools.product([1,2,3],[1,2,3],[1,2,3])]).items())

class ProbabilisticGameState():
    def __init__(self, p1_pos, p2_pos):
        # positions are stored internally with a 0 index instead of a 1 index
        self.game_distribution = defaultdict(lambda: 0)
        # (p1_pos, p2_pos, p1_score, p2_score, whose_turn)
        self.game_distribution[(p1_pos - 1, p2_pos - 1, 0, 0, 0)] = 1
        self.p1_wins = 0
        self.p2_wins = 0
    
    def turn(self):
        next_distribution = defaultdict(lambda: 0)
        for (p1_pos, p2_pos, p1_score, p2_score, whose_turn), number_of_worlds in self.game_distribution.items():
            # print(p1_pos, p2_pos, p1_score, p2_score, whose_turn)
            if whose_turn == 0:
                for (value, number_of_scenarios) in dirac_three_dice_rolls:
                    # print("Testing", value, number_of_scenarios)
                    new_p1_pos = (p1_pos + value) % 10
                    new_p1_score = p1_score + (new_p1_pos + 1)
                    if new_p1_score >= 21:
                        # if a win, add to counter instead
                        # print("Winning", number_of_worlds, number_of_scenarios)
                        self.p1_wins += (number_of_worlds * number_of_scenarios)
                    else:
                        # print ("Adding", (new_p1_pos, p2_pos, new_p1_score, p2_score, 1) )
                        next_distribution[
                            (new_p1_pos, p2_pos, new_p1_score, p2_score, 1)
                        ] += (number_of_worlds * number_of_scenarios)
            else:
                for (value, number_of_scenarios) in dirac_three_dice_rolls:
                    new_p2_pos = (p2_pos + value) % 10
                    new_p2_score = p2_score + (new_p2_pos + 1)
                    if new_p2_score >= 21:
                        # if a win, add to counter instead
                        self.p2_wins += (number_of_worlds * number_of_scenarios)
                    else:
                        next_distribution[
                            (p1_pos, new_p2_pos, p1_score, new_p2_score, 0)
                        ] += (number_of_worlds * number_of_scenarios)
        self.game_distribution = next_distribution
    
    def all_games_are_finished(self):
        return len(self.game_distribution) == 0
        
state = ProbabilisticGameState(10, 2)
state = ProbabilisticGameState(4, 8)
while not state.all_games_are_finished():
    state.turn()
print (state.p1_wins, state.p2_wins)