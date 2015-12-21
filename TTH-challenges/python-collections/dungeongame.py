import random

CELLS = [(0, 3), (1, 3), (2, 3), (3, 3),
         (0, 2), (1, 2), (2, 2), (3, 2),
         (0, 1), (1, 1), (2, 1), (3, 1),
         (0, 0), (1, 0), (2, 0), (3, 0)]


def get_locations():
    """
    will randomize locations of door, player and monster
    :return:
    """
    monster = random.choice(CELLS)
    door = random.choice(CELLS)
    player = random.choice(CELLS)
    if monster == player or monster == door or door == player:
        return get_locations()
    # player = (3, 0)
    return monster, door, player


def move_player(player, move):
    # player  (x,y)
    x, y = player
    if move == 'LEFT':
        x -= 1
    elif move == 'RIGHT':
        x += 1
    elif move == 'DOWN':
        y -= 1
    elif move == 'UP':
        y += 1
    return x, y


def get_moves(player):  # far from being complete # 0,2
    MOVES = ['RIGHT', 'LEFT', 'UP', 'DOWN']
    if player[0] == 0:
        MOVES.remove('LEFT')
    if player[0] == 3:
        MOVES.remove('RIGHT')
    if player[1] == 0:
        MOVES.remove('DOWN')
    if player[1] == 3:
        MOVES.remove('UP')
    return MOVES


monster, door, player = get_locations()

while True:
    moves = get_moves(player)
    print("You hear a hungry growling nearby...")
    print("you are currently in a room {} ".format(player))  # fill in with player position
    print("you can move {}".format(moves))  # fill in available moves
    # move = input("> ")
    move = raw_input("> ")
    move = move.upper()
    if move == 'QUIT':
        break
    if move in moves:
        player = move_player(player, move)
    else:
        print("You bumped into a wall ! ")
        continue
    if player == door:
        print("You escaped!")
        break
    if player == monster:
        print("You were eaten by a Dragonlich !")
        break
