# Imports the python library "random" which allow random item selection

import random

# Asks user to choose rock, paper or scissors, ensures valid input. 
# Intakes user input and makes sure it is valid within the rules of the game:
# Passes user input to the play function when called.

def get_valid_user_choice():
    while True:
        user_input = input("What is your choice? Choose 'r' for rock, 'p' for paper, or 's' for scissors\n") 

        if user_input in ['r', 'p', 's']:
            return user_input
    
        else:
            print("invalid key pressed. Please choose again!")

# Defines win condition, that is when the user has won vs a tie or the user losing.
# If user chooses 'r' and computer chooses 's' player wins.
# If user chooses 's' and computer chooses 'p' player wins.
# If user chooses 'p' and computer chooses 'r' player wins.
# If user chooses the same as computer, it's a tie.
# If anyting else happesn, the user loses.

def is_win(player, opponent):
    # return true if player wins
    # r > s, s > p, p > r
    return (
        (player == 'r' and opponent == 's') or 
        (player == 's' and opponent == 'p') or 
        (player == 'p' and opponent == 'r')
    )

# Converts choice from 'r' to 'Rock" from 'p' to paper, from 's' to Scissors.
# Passes converted choice to play function.

def convert_choice(choice):
    if choice == 'r':
        return "Rock"
    if choice == 'p':
        return "Paper"
    if choice == 's':
        return "Scissors"
    
# Defines the game, takes valid user input and calls the convert_choice function 
# for both player and computer. Prints user choice and computer choice. Decides 
# the winner, either the player wins ("You won!"), it's a tie ("It's a tie") or 
# player loses ("you lost!").    
def play():
    user = get_valid_user_choice()
    computer = random.choice(['r', 'p', 's'])
    user_full = convert_choice(user)
    computer_full = convert_choice(computer)

    print(f"You chose: {user_full}.")
    print(f"The computer chose: {computer_full}.")

    if user == computer:
        return 'It\'s a tie'

    if is_win(user, computer):
        return 'You won!'

    return 'You lost!'

# Creates game loop, declares win lose or Tie and asks user if they would like to play again, 
# validates input of yes or no, other choices result in user being asked to try again, 
# and based on user input the game either stops or starts again!

def main():
    while True:
        result = play()
        print(result)

        while True:
            play_again = input('Would you like to play again? (y/n): ').strip().lower()

            if play_again in ['y', 'n']:
                break
            else:
                print("Invalid key pressed. Please type 'y' for yes, or 'n' for no.")

        if play_again == 'n':
            print("Thanks for playing! Goodbye!")
            break
        
# Checks if the current script is being run directly.
# When you run this script, Python sets __name__ to "__main__".
if __name__ == "__main__":
    # If the script is run directly, call the main() function to start the game.
    main()
