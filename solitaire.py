from annealing_functions import *
from solitaire_classes import *
import time
BREAK_STRING = "-------------------------------------------------------------------"
temperature = 1.0
MIN_T = 0.01
ALPHA = 0.99
def printValidCommands():
    """ Provides the list of commands, for when users press 'h' """
    print("Valid Commands: ")
    print("\tmv - move card from Stock to Waste")
    print("\twf - move card from Waste to Foundation")
    print("\twt #T - move card from Waste to Tableau")
    print("\ttf #T - move card from Tableau to Foundation")
    print("\ttt #T1 #T2 - move card from one Tableau column to another")
    print("\th - help")
    print("\tq - quit")
    print("\t*NOTE: Hearts/diamonds are red. Spades/clubs are black.")

def printTable(tableau, foundation, stock_waste):
    """ Prints the current status of the table """
    print(BREAK_STRING)
    print("Waste \t Stock \t\t\t\t Foundation")
    print("{}\t{}\t\t{}\t{}\t{}\t{}".format(stock_waste.getWaste(), stock_waste.getStock(),
        foundation.getTopCard("C"), foundation.getTopCard("H"),
        foundation.getTopCard("S"), foundation.getTopCard("D")))
    print("\nTableau\n\t1\t2\t3\t4\t5\t6\t7\n")
    # Print the cards, first printing the unflipped cards, and then the flipped.
    for x in range(tableau.pile_length()):
        print_str = ""
        for col in range(7):
            hidden_cards = tableau.unflipped[col]
            shown_cards = tableau.flipped[col]
            if len(hidden_cards) > x:
                print_str += "\tx"
            elif len(shown_cards) + len(hidden_cards) > x:
                print_str += "\t" + str(shown_cards[x-len(hidden_cards)])
            else:
                print_str += "\t"
        print(print_str)
    print("\n"+BREAK_STRING)

if __name__ == "__main__":
    move_count = 0
    d = Deck()
    t = Tableau([d.deal_cards(x) for x in range(1,8)])
    f = Foundation()
    sw = StockWaste(d.deal_cards(24))

    print("\n" + BREAK_STRING)
    print("Welcome to Danny's Solitaire!\n")
    printValidCommands()
    printTable(t, f, sw)

    while not f.gameWon():
        print(">>> Current Board Cost:", get_cost(t, f, sw))
        available_moves = evaluate_position(t, f, sw, get_legal_moves(t, f, sw,), temperature)
        move = choose_move(available_moves)
        print("Move chosen is: ", move)
        command = move
        command = command.lower().replace(" ", "")
        if command == "h":
            printValidCommands()
        elif command == "q":
            print("Game exited.")
            break
        elif command == "mv":
            if sw.stock_to_waste():
                printTable(t, f, sw)
        elif command == "wf":
            if f.addCard(sw.getWaste()):
                sw.pop_waste_card()
                printTable(t, f, sw)
            else:
                print("Error! No card could be moved from the Waste to the Foundation.")
        elif "wt" in command and len(command) == 3:
            col = int(command[-1]) - 1
            if t.waste_to_tableau(sw, col):
                printTable(t, f, sw)
            else:
                print("Error! No card could be moved from the Waste to the Tableau column.")
        elif "tf" in command and len(command) == 3:
            col = int(command[-1]) - 1
            if t.tableau_to_foundation(f, col):
                printTable(t, f, sw)
            else:
                print("Error! No card could be moved from the Tableau column to the Foundation.")
        elif "tt" in command and len(command) == 4:
            c1, c2 = int(command[-2]) - 1, int(command[-1]) - 1
            if t.tableau_to_tableau(c1, c2):
                printTable(t, f, sw)
            else:
                print("Error! No card could be moved from that Tableau column.")
        else:
            print("Sorry, that is not a valid command.")

        temperature = max(temperature * ALPHA, MIN_T)
        time.sleep(.05)
        move_count += 1
    if f.gameWon():
        print("Congratulations! You've won!")
        print("Move Count: ", move_count)
