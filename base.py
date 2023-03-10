import pandas as pd
import random


class RockPaperScissorsChoice:
    def __init__(self, choice_chosen, number_of_times_chosen):
        self.choice_chosen = choice_chosen #string (for testing purposes): 'rock', 'paper', 'scissors'
        self.number_of_times_chosen = number_of_times_chosen #number of times this choice was chosen next

        if choice_chosen == "rock":
            self.location = 0
        elif choice_chosen == "paper":
            self.location = 1
        elif choice_chosen == "scissors":
            self.location = 2
        elif choice_chosen == "EMPTY":
            self.location = -1
        else:
            print("ERROR (line 19): unexpected RockPaperScissors.choice_chosen literal")
            exit()

    def update_choice(self, new_choice):
        self.choice_chosen = new_choice

        if new_choice == "rock":
            self.location = 0
        elif new_choice == "paper":
            self.location = 1
        elif new_choice == "scissors":
            self.location = 2

    def __gt__(self, other):
        return self.number_of_times_chosen > other.number_of_times_chosen
    
    def __lt__(self, other):
        return self.number_of_times_chosen < other.number_of_times_chosen
    
    def __eq__(self, other):
        return self.number_of_times_chosen == other.number_of_times_chosen

    def __ne__(self, other):
        return self.number_of_times_chosen != other.number_of_times_chosen

    def __ge__(self, other):
        return self.number_of_times_chosen >= other.number_of_times_chosen

    def __le__(self, other):
        return self.number_of_times_chosen <= other.number_of_times_chosen

    def __str__(self):
        return f"{self.choice_chosen}: {self.number_of_times_chosen}"

class NextMatchProbability:
    def __init__(self, number_of_times_rock_chosen_next, number_of_times_scissors_chosen_next, number_of_times_paper_chosen_next, total_number_matches_played_next):
        self.rock = RockPaperScissorsChoice('rock', number_of_times_rock_chosen_next)
        self.paper = RockPaperScissorsChoice('paper', number_of_times_paper_chosen_next)
        self.scissors = RockPaperScissorsChoice('scissors', number_of_times_scissors_chosen_next)
        self.total = total_number_matches_played_next

    def rock_prob(self):
        if self.total != 0:
            return self.rock.number_of_times_chosen / self.total
        else:
            return 0.33
    
    def paper_prob(self):
        if self.total != 0:
            return self.paper.number_of_times_chosen / self.total
        else:
            return 0.33
    
    def scissors_prob(self):
        if self.total != 0:
            return self.scissors.number_of_times_chosen / self.total
        else:
            return 0.33

    def get_prob_by_location(self, location):
        if location == 0:
            return self.rock
        elif location == 1:
            return self.paper
        elif location == 2:
            return self.scissors
        else:
            return None

    def __str__(self):
        return f"rock: {self.rock.number_of_times_chosen} / {self.rock_prob()}\
    \npaper: {self.paper.number_of_times_chosen} / {self.paper_prob()}\
    \nscissors: {self.scissors.number_of_times_chosen} / {self.scissors_prob()}\
    \ntotal: {self.total}"

starters = NextMatchProbability(0, 0, 0, 0) #number of times rock chosen as first choice, 
                                            #number of times scissors, 
                                            #number of times paper, 
                                            #total number of first matches catalogued


#next_chance_probability_matrix organized so: rock, paper, scissors (player)
                                    # rock      x     x       x
                                    # paper     x     x       x
                                    # scissors  x     x       x
                                    # (computer)
#where each location represents a potential match: computer's choice vs player's choice (organized matrix[player_choice][computer_choice])
#and the total_matches location is used as a 
#at each location is stored a NextMatchProbability object, which can be used to calculate the probability of each possible next choice 
#inputted by the player
probability_matrix = [[NextMatchProbability(0, 0, 0, 0), NextMatchProbability(0, 0, 0, 0), NextMatchProbability(0, 0, 0, 0)],
                      [NextMatchProbability(0, 0, 0, 0), NextMatchProbability(0, 0, 0, 0), NextMatchProbability(0, 0, 0, 0)],
                      [NextMatchProbability(0, 0, 0, 0), NextMatchProbability(0, 0, 0, 0), NextMatchProbability(0, 0, 0, 0)]]

#organized by location same as next_chance_probability_matrix
#                       user_rock     user_paper      user_scissors
#computer_rock          u_r vs c_r    u_p vs c_r       u_s vs c_r
#computer_paper         u_r vs c_p    u_p vs c_p       u_s vs c_p     
#computer_scissors      u_r vs c_s    u_p vs c_s       u_s vs c_s
winner_matrix = [["TIE", "USER WINS: paper beats rock", "COMPUTER WINS: rock beats scissors"],
                 ["COMPUTER WINS: paper beats rock", "TIE", "USER WINS: scissors beats paper"],
                 ["USER WINS: rock beats scissors", "COMPUTER WINS: scissors beats paper", "TIE"]]

user_wins = 0
computer_wins = 0

def predict_next_player_choice(probability_matrix, last_player_choice = RockPaperScissorsChoice("EMPTY", -1), last_computer_choice = RockPaperScissorsChoice("EMPTY", -1)):
    # using starters matrix
    if last_player_choice.choice_chosen == "EMPTY" and last_computer_choice.choice_chosen == "EMPTY":
        if probability_matrix.total == 0:
            rand = random.randrange(0,3)
            choice = probability_matrix.get_prob_by_location(rand)
            return choice
        else:
            rock = probability_matrix.rock
            paper = probability_matrix.paper
            sci = probability_matrix.scissors

            if rock >= paper and rock >= sci:
                return rock
            if paper >= rock and paper >= sci:
                return paper
            if sci >= rock and sci >= paper:
                return sci
    else:
        choice_probabilities = probability_matrix[last_computer_choice.location][last_player_choice.location]
        rock = choice_probabilities.rock
        paper = choice_probabilities.paper
        sci = choice_probabilities.scissors
        total = choice_probabilities.total

        if total == 0:
            rand = random.randrange(0,3)
            choice = probability_matrix.get_prob_by_location(rand)
            return choice
        elif rock >= paper and rock >= sci:
            return rock
        elif paper >= rock and paper >= sci:
            return paper
        else:
            return sci

def get_inputted_player_choice():
    player_choice = RockPaperScissorsChoice("EMPTY", -1)
    while True:
        rpc_text = input("rock, paper, scissors, SHOOT: ")
        rpc_text = rpc_text.lower()

        if rpc_text == "r" or rpc_text == "rock":
            player_choice.update_choice("rock")
            break
        elif rpc_text == "p" or rpc_text == "paper":
            player_choice.update_choice("paper")
            break
        elif rpc_text == "s" or rpc_text == "scissors":
            player_choice.update_choice("scissors")
            break
        elif rpc_text == "q" or rpc_text == "quit" or rpc_text == "exit" or rpc_text == "stop":
            print("Thank you for playing")
            return None
        else:
            print("Unexpected answer. Please enter 'rock', 'paper', or 'scissors' as your choice")
    return player_choice

def get_win_against_prediction(predicted_player_choice):
    computer_choice = RockPaperScissorsChoice("EMPTY", -1)

    if(predicted_player_choice.choice_chosen == 'rock'):
        computer_choice.update_choice("paper")
    elif(predicted_player_choice.choice_chosen == 'paper'):
        computer_choice.update_choice("scissors")
    elif(predicted_player_choice.choice_chosen == 'scissors'):
        computer_choice.update_choice("rock")
    else:
        print(f"ERROR (get_win_against_prediction): unexpected player prediction - {predicted_player_choice.choice_chosen}")
        return None
    
    return computer_choice

def update_starters(player_choice):
    starters.total += 1

    if player_choice.choice_chosen == 'rock':
        starters.rock.number_of_times_chosen += 1
    elif player_choice.choice_chosen == 'paper':
        starters.paper.number_of_times_chosen += 1
    elif player_choice.choice_chosen == 'scissors':
        starters.scissors.number_of_times_chosen += 1
    elif player_choice.choice_chosen == "EMPTY":
        print("ERROR in update_starters(): user_choice is EMPTY")
        exit()
    else:
        print("ERROR in update_starters(): unrecognized user_choice")

def update_probability_matrix(prev_player_choice, prev_computer_choice, player_choice):
    print(probability_matrix[prev_computer_choice.location][prev_player_choice.location])
    probability_matrix[prev_computer_choice.location][prev_player_choice.location].total += 1
    if player_choice.choice_chosen == 'rock':
        probability_matrix[prev_computer_choice.location][prev_player_choice.location].rock.number_of_times_chosen += 1
    elif player_choice.choice_chosen == 'paper':
        probability_matrix[prev_computer_choice.location][prev_player_choice.location].paper.number_of_times_chosen += 1
    elif player_choice.choice_chosen == 'scissors':
        probability_matrix[prev_computer_choice.location][prev_player_choice.location].scissors.number_of_times_chosen += 1
    elif player_choice.choice_chosen == "EMPTY":
        print("ERROR in update_probability_matrix(): player_choice is EMPTY")
        exit()
    else:
        print("ERROR in update_probability_matrix(): unrecognized player_choice")
    print(probability_matrix[prev_computer_choice.location][prev_player_choice.location], "\n")
    
        

def play_loop():
    predicted_player_choice = predict_next_player_choice(starters)
    print(f"predicted player choice: {predicted_player_choice}")

    computer_choice = get_win_against_prediction(predicted_player_choice)
    print(f"computer choice: {computer_choice}")

    player_choice = get_inputted_player_choice()
    print(f"player choice: {player_choice}")
    print(f"{winner_matrix[computer_choice.location][player_choice.location]}\n")

    update_starters(player_choice)
    prev_computer_choice = computer_choice
    prev_player_choice = player_choice

    while True:
        predicted_player_choice = predict_next_player_choice(starters)
        print(f"predicted player choice: {predicted_player_choice}")

        computer_choice = get_win_against_prediction(predicted_player_choice)
        print(f"computer choice: {computer_choice}")

        player_choice = get_inputted_player_choice()
        if player_choice is None:
            exit()
        print(f"player choice: {player_choice}")
        print(f"{winner_matrix[computer_choice.location][player_choice.location]}\n")

        update_probability_matrix(prev_player_choice, prev_computer_choice, player_choice)
        prev_player_choice = player_choice
        prev_computer_choice = computer_choice

def prefill_probabilities(filename):
    stats = pd.read_csv(filename)
    starters.rock.total_times_chosen = stats['rock'][0]
    starters.paper.total_times_chosen = stats['paper'][0]
    starters.scissors.total_times_chosen = stats['scissors'][0]
    starters.total = stats['total'][0]

    p = 0
    c = 0 

    for i in range(stats['rock'][1:].size):
        if p == 3:
            p = 0
            c += 1
        
        probability_matrix[c][p].rock.number_of_times_chosen = stats['rock'][i]
        probability_matrix[c][p].paper.number_of_times_chosen = stats['paper'][i]
        probability_matrix[c][p].scissors.number_of_times_chosen = stats['scissors'][i]
        probability_matrix[c][p].total = stats['total'][i]

        p += 1

prefill_probabilities("tester_prob_matrix.csv")
play_loop()



    



