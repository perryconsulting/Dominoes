"""
A simple dominoes game

"""
import copy
import random
import sys


class DominoSet:
    """

    A Domino Set
    """
    snake: list[list[int]]
    player_set: list[list[int]]
    computer_set: list[list[int]]
    stock_set: list[list[int]]
    full_set: list[list[int]]

    def __init__(self):
        """

        :rtype: DominoSet
        """
        self.full_set = []
        self.stock_set = []
        self.computer_set = []
        self.player_set = []
        self.snake = []
        self.generate_dominoes()

    def generate_dominoes(self):
        """
        Generate a full domino set and store it in self.full_set[].
        """
        i: int
        for i in range(0, 7):
            j: int
            for j in range(0, 7):
                if i == j:
                    singleton: list[int] = [i, j]
                    self.full_set.append(singleton)
                else:
                    if [j, i] not in self.full_set:
                        singleton = [i, j]
                        self.full_set.append(singleton)

    def deal_pieces(self):
        """
        Layout the board, distribute the full set into stock, computer, and player sets.

        """
        valid_deal: bool = False

        # Create potential board setup and check for a player with a double. If no player holds a
        # double, then re-deal.
        while not valid_deal:
            temp_full_set = copy.deepcopy(self.full_set)
            temp_stock_pieces = []
            temp_computer_pieces = []
            temp_player_pieces = []
            temp_snake = []

            _: int
            for _ in range(14):
                piece = temp_full_set.pop(random.randint(0, len(temp_full_set) - 1))
                temp_stock_pieces.append(piece)
            for _ in range(7):
                piece = temp_full_set.pop(random.randint(0, len(temp_full_set) - 1))
                temp_computer_pieces.append(piece)
            for _ in range(7):
                piece = temp_full_set.pop(random.randint(0, len(temp_full_set) - 1))
                temp_player_pieces.append(piece)

            potential_computer_snake: list[list[int]] = \
                [x for x in temp_computer_pieces if x[0] == x[1]]
            potential_player_snake: list[list[int]] = \
                [x for x in temp_player_pieces if x[0] == x[1]]
            if len(potential_computer_snake) == 0 and len(potential_player_snake) == 0:
                continue
            if len(potential_computer_snake) == 0 and len(potential_player_snake) != 0:
                player_snake = temp_player_pieces.pop(
                    temp_player_pieces.index(max(potential_player_snake)))
                temp_snake.append(player_snake)
            elif len(potential_computer_snake) != 0 and len(potential_player_snake) == 0:
                computer_snake = temp_computer_pieces.pop(
                    temp_computer_pieces.index(max(potential_computer_snake)))
                temp_snake.append(computer_snake)
            else:
                highest_computer_doubles = max(potential_computer_snake)
                highest_player_doubles = max(potential_player_snake)
                if highest_computer_doubles > highest_player_doubles:
                    computer_snake = temp_computer_pieces.pop(
                        temp_computer_pieces.index(highest_computer_doubles))
                    temp_snake.append(computer_snake)
                else:
                    player_snake = temp_player_pieces.pop(
                        temp_player_pieces.index(highest_player_doubles))
                    temp_snake.append(player_snake)

            self.stock_set = temp_stock_pieces
            self.computer_set = temp_computer_pieces
            self.player_set = temp_player_pieces
            self.snake = temp_snake
            valid_deal = True


def build_player_list(domino_set):
    """
    Calculate the starting player based on set size after the snake is started.

    :param domino_set:
    :return player list:
    """
    players: list[str] = []
    if len(domino_set.player_set) > len(domino_set.computer_set):
        players.append("human")
        players.append("computer")
    else:
        players.append("computer")
        players.append("human")
    return players


def display_current_playing_field():
    stock_count = len(bones.stock_set)
    computer_count = len(bones.computer_set)
    print('=' * 70)
    print(f"Stock size: {stock_count}")
    print(f"Computer pieces: {computer_count}\n")

    if len(bones.snake) > 6:
        print(bones.snake[0], end='')
        print(bones.snake[1], end='')
        print(bones.snake[2], end='...')
        print(bones.snake[-3], end='')
        print(bones.snake[-2], end='')
        print(bones.snake[-1], end='')
    else:
        for tile in bones.snake:
            print(tile, end='')
    print("\n\nYour pieces:")
    for i, piece in enumerate(bones.player_set):
        print(f'{i + 1}:{piece}')


def check_game_status(player):
    game_status = {'player_turn': "It's your turn to make a move. Enter your command.",
                   'computer_turn': "Computer is about to make a move. Press Enter to continue...",
                   'player_won': "The game is over. You won!",
                   'computer_won': "The game is over. The computer won!",
                   'draw_game': "The game is over. It's a draw!"}

    if player == 'human':
        current_status = game_status['player_turn']
        return_status = 111
    else:
        current_status = game_status['computer_turn']
        return_status = 222

    if player == 'human' and len(bones.computer_set) == 0:
        current_status = game_status['computer_won']
        return_status = 999
    elif player == 'computer' and len(bones.player_set) == 0:
        current_status = game_status['player_won']
        return_status = 999
    elif len(bones.snake) > 1:
        first_tile_left_pip = bones.snake[0][0]
        last_tile_right_pip = bones.snake[-1][0]
        pip_count = 0
        if first_tile_left_pip == last_tile_right_pip:
            for i in bones.snake:
                for j in i:
                    if j == first_tile_left_pip:
                        pip_count += 1
            if pip_count == 8:
                current_status = game_status['draw_game']
                return_status = 999

    print(f"\nStatus: {current_status}")
    return return_status


def bust_a_move(player, move):
    if move == 0:
        if len(bones.stock_set) != 0:
            tile = bones.stock_set.pop(random.randint(0, len(bones.stock_set) - 1))
            if player == 'human':
                bones.player_set.append(tile)
            else:
                bones.computer_set.append(tile)
    else:
        tile_choice = abs(move) - 1
        if player == 'human':
            tile = bones.player_set.pop(tile_choice)
        else:
            tile = bones.computer_set.pop(tile_choice)
        if move < 0:
            bones.snake.insert(0, tile)
        else:
            bones.snake.append(tile)
    return "Valid"


def shall_we_play_a_game():
    player_list = build_player_list(bones)
    current_player = player_list[0]
    game_state = "In Progress"

    while game_state == "In Progress":
        player_size = len(bones.player_set)
        display_current_playing_field()
        check_status = check_game_status(current_player)
        if check_status == 111:
            move_status = "Invalid"
            player_move = 999
            while move_status == "Invalid":
                try:
                    player_move = int(input())
                    if abs(player_move) < 0 or abs(player_move) > player_size:
                        raise ValueError
                    move_status = "Valid"
                except ValueError:
                    print("Invalid input. Please try again.")
            busted = bust_a_move(current_player, player_move)
            if busted == "Invalid":
                print("Illegal move. Please try again..")
                continue
            current_player = 'computer'
            continue
        if check_status == 222:
            input()
            if len(bones.computer_set) > 1:
                computer_move = random.randint(-(len(bones.computer_set) - 1), len(bones.computer_set) - 1)
            else:
                computer_move = random.randint(-1, 1)
            bust_a_move(current_player, computer_move)
            current_player = 'human'
            continue
        game_state = "Game Over"


if __name__ == "__main__":
    bones: DominoSet = DominoSet()
    bones.deal_pieces()
    shall_we_play_a_game()
    sys.exit(0)
