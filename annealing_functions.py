import copy
import math
import random # We will need this in order to pick a random state after we calculate the probability
# TODO: If not derivable from the game state in solitare.py, make a function that contains
#  all the legal moves available
#  1) Take the current game state, and find all legal moves
#  2) Return all legal moves in a list for our evaluate_position()
# -------------------------------------------------
def get_legal_moves(tableau, foundation, stock_waste):
    print("We are in get_legal_moves()")
    moves = []
    # we will use deep copies of the tableau, foundation, and stock_waste in order to test the game state

    # If there are cards in the stock that can be moved to the waste, that is a legal move.
    if len(stock_waste.deck) > 0 or len(stock_waste.waste) > 0:
        moves.append("mv")

    # If there is a card in the waste that can be moved to the foundation, that is a legal move.
    sw = copy.deepcopy(stock_waste)
    waste = sw.getWaste()
    if waste != 'empty':
        f = copy.deepcopy(foundation)
        try:
            if f.addCard(waste):  # test the move safely
                moves.append("wf")
        except IndexError:
            pass

    # If there is a card in the waste that can be moved to the tableau, that is a legal move.
    if waste != 'empty':
        for col in range(7):
            t = copy.deepcopy(tableau)
            if t.addCards([waste], col):
                moves.append(f'wt {col + 1}')

    # If there is a card  that can be put from the Tableau to the foundation, that is a legal move.
    for col in range(7):
        t = copy.deepcopy(tableau)
        f = copy.deepcopy(foundation)
        if t.flipped[col]:
            top = t.flipped[col][-1]
            try:
                if f.addCard(top):  # check return value
                    moves.append(f'tf {col + 1}')
            except IndexError:
                continue

    # If there is a card from 1 column we can move to another in the tableau, that is a legal move.
    for col_1 in range(7):
        t = copy.deepcopy(tableau)
        c1_cards = t.flipped[col_1]
        for index in range(len(c1_cards)):
            moving = c1_cards[index:]
            for col_2 in range(7):
                if col_1 == col_2: # Don't check the column we are already in!
                    continue
                if t.addCards(moving, col_2):
                    moves.append(f'tt {col_1 + 1} {col_2 + 1}')

    print('the legal moves so far are:', moves)
    return moves

# -------------------------------------------------

# TODO: Make the SA function that will evaulate the probability of going to each state that is possible
#  The function should:
#  1) Evaluate the cost for each move available to the user
#  2) Given the cost, calculate the probability of going to said mvoes
#  3) Save the probabilities of all the possible moves, and pass them onto choose_move()
# -------------------------------------------------
def evaluate_position(tableau, foundation, stock_waste,available_moves, current_temp):

    move_weights = []
    current_cost = get_cost(tableau, foundation, stock_waste)
    for move in available_moves:
        t_new, f_new, sw_new = simulate_move(tableau, foundation, stock_waste, move)
        new_cost = get_cost(t_new, f_new, sw_new)
        delta_E = new_cost - current_cost
        print("delta_E: ", delta_E,"cost", new_cost)

        w = math.exp(-delta_E / current_temp)
        # if delta_E <= 0:
        #     w = 1.0
        # else:
        #     if current_temp > 0:
        #         w = math.exp(-delta_E / current_temp)
        #     else:
        #         w = 0.0
        move_weights.append([move, w])
    print("results of SA: ", move_weights)
    return move_weights
    ''' SAMPLE CODE FOR THE SA FUNCTION:
        current = initial_state
    T = initial_temperature

    while T > minimum_temperature:
        next = random_neighbor(current)
        ΔE = get_cost(next) - get_cost(current) <-- Move this, dont calculate get_cost(current) every time

        if ΔE < 0:
            current = next            # Accept better move
        else:
            p = exp(-ΔE / T)         
            if random(0,1) < p:
                current = next        # Accept worse move with probability p

        T = decrease_temperature(T)   # Cooling schedule
    '''


# -------------------------------------------------

def simulate_move(tableau, foundation, stock_waste, move):
    f = copy.deepcopy(foundation)
    sw = copy.deepcopy(stock_waste)
    t = copy.deepcopy(tableau)
    parts = move.split()

    if move == "mv":
        sw.stock_to_waste()

    elif move == "wf":
        sw.pop_waste_card()

    elif parts[0] == "wt":
        col = int(parts[1]) - 1
        t.waste_to_tableau(sw, col)

    elif parts[0] == "tf":
        col = int(parts[1]) - 1
        t.tableau_to_foundation(f, col)
    elif parts[0] == "tt":
        c1 = int(parts[1]) - 1
        c2 = int(parts[2]) - 1
        t.tableau_to_tableau(c1, c2)

    return t, f, sw


# TODO: Get the cost of a given move, using a special cost function defined by us,
#  this make take some refinement.
#  This function should:
#  1) Given a move's outcome, it should evaluate the cost of a given move
#  2) Return the cost of that move

def get_cost(tableau, foundation, stock_waste):
    
    cost = 0

    # 1. Check the Foundation
    # We subtract 50 for every card in the foundation to reward the AI.
    # accessing the dictionary from the Foundation class
    for suit, stack in foundation.foundation_stacks.items():
        cost -= (len(stack) * 50)

    # 2. Check the Tableau for Unflipped cards
    # We add 20 points for every card that is still face-down (unflipped) because we want to uncover them.
    for col in range(7):
        # accessing the unflipped list from the Tableau class
        hidden_cards = tableau.unflipped[col]
        cost += (len(hidden_cards) * 20)

    # 3. Check Stock and Waste
    # We want to use the cards in the deck, so we add a small penalty if cards are stuck there.
    # accessing the deck and waste lists from StockWaste class
    cost += (len(stock_waste.deck) * 2)
    cost += (len(stock_waste.waste) * 2)

    return cost

# -------------------------------------------------

# TODO: Make a function that will use the random library, to select a state at random,
#  given the probability derived in the last function.
#  the given function should:
#  1) Returns the move it selects, passing it to solitaire.py
#  2) Uses random.py in order to select the moves
# -------------------------------------------------
def choose_move(possible_moves):
    moves = []
    weights = []
    for x in range(len(possible_moves)):
        moves.append(possible_moves[x][1])
        weights.append(possible_moves[x][2])

    move = random.choices(moves, weights=weights, k=1)[0]
    return move
# -------------------------------------------------
