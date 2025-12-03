import random # We will need this in order to pick a random state after we calculate the probability

# TODO: If not derivable from the game state in solitare.py, make a function that contains
#  all the legal moves available
#  1) Take the current game state, and find all legal moves
#  2) Return all legal moves in a list for our evaluate_position()
# -------------------------------------------------
def get_legal_moves(tableau, foundation, stock_waste):
    possible_moves = []
    return possible_moves

# -------------------------------------------------

# TODO: Make the SA function that will evaulate the probability of going to each state that is possible
#  The function should:
#  1) Evaluate the cost for each move available to the user
#  2) Given the cost, calculate the probability of going to said mvoes
#  3) Save the probabilities of all the possible moves, and pass them onto choose_move()
# -------------------------------------------------
def evaluate_position(available_moves):
    move_weights = []
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
    return move_weights

# -------------------------------------------------

# TODO: Get the cost of a given move, using a special cost function defined by us,
#  this make take some refinement.
#  This function should:
#  1) Given a move's outcome, it should evaluate the cost of a given move
#  2) Return the cost of that move
# -------------------------------------------------
def get_cost(board_state):
    move_weights = []
    return move_weights

# -------------------------------------------------

# TODO: Make a function that will use the random library, to select a state at random,
#  given the probability derived in the last function.
#  the given function should:
#  1) Returns the move it selects, passing it to solitaire.py
#  2) Uses random.py in order to select the moves
# -------------------------------------------------
def choose_move(move_probabilities):
    move = None
    return move
# -------------------------------------------------