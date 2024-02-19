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


if __name__ == "__main__":
    # region Construct domino set and deal out tiles to players
    bones: DominoSet = DominoSet()
    bones.deal_pieces()

    # endregion

    # region Game Functions
    def build_player_list():
        """
        The player list establishes player order by size of set
        :rtype: list
        :return: Players in order, based on who started the snake.
        """
        players: list[str] = []
        if len(bones.player_set) > len(bones.computer_set):
            players.append("human")
            players.append("computer")
        else:
            players.append("computer")
            players.append("human")
        return players


    def display_current_playing_field():
        """
        Draw the current status of the board
        """
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
        """
        Determine the current player and whether a win/draw condition exists
        :rtype: int
        :param player: Pass in expected next player
        :return: Status of the game (win/lose/draw) based on board condition
        """
        game_status = {'player_turn': "It's your turn to make a move. Enter your command.",
                       'computer_turn':
                           "Computer is about to make a move. Press Enter to continue...",
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
            last_tile_right_pip = bones.snake[-1][-1]
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


    def validate_move(player, move):
        """
        Validate the proposed move to check for int type and
        whether the proposed move matches available moves
        on the board.
        :rtype: str
        :param player:
        :param move:
        :return: Whether the proposed move is valid.
        """
        tile_choice = abs(move) - 1
        snake_first_pip = bones.snake[0][0]
        snake_last_pip = bones.snake[-1][-1]
        match = False

        if move == 0:
            return "Valid"

        if player == 'human':
            if abs(move) > len(bones.player_set):
                raise ValueError

        tile = bones.player_set[tile_choice] \
            if player == 'human' else bones.computer_set[tile_choice]

        if move > 0:
            for pip in tile:
                if pip == snake_last_pip:
                    match = True
        if move < 0:
            for pip in tile:
                if pip == snake_first_pip:
                    match = True

        return "Valid" if match is True else "Invalid"


    def bust_a_move(player, move):
        """
        Apply the proposed move to the board and adjust the
        player's tiles accordingly.
        :param player:
        :param move:
        """
        snake_first_pip = bones.snake[0][0]
        snake_last_pip = bones.snake[-1][-1]

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
                if tile[-1] != snake_first_pip:
                    tile.reverse()
                bones.snake.insert(0, tile)
            else:
                if tile[0] != snake_last_pip:
                    tile.reverse()
                bones.snake.append(tile)


    def generate_current_pip_value():
        pip_values = []
        return pip_values


    def shall_we_play_a_game():
        """
        Main game logic.
        """
        player_list = build_player_list()
        current_player = player_list[0]
        game_state = "In Progress"

        while game_state == "In Progress":
            display_current_playing_field()
            check_status = check_game_status(current_player)
            player_move = 999
            # region Human player move logic
            if check_status == 111:
                move_status = "Invalid"

                while move_status == "Invalid":
                    try:
                        player_move = int(input())
                        move_status = validate_move(current_player, player_move)
                        if move_status == "Invalid":
                            print("Illegal move. Please try again..")
                    except ValueError:
                        print("Invalid input. Please try again.")
            # endregion
            # region Computer player move logic
            if check_status == 222:
                move_status = "Invalid"
                input()

                while move_status == "Invalid":
                    # Original random number generator
                    # player_move = (random.randint(-(len(bones.computer_set)),
                    #                               len(bones.computer_set)))
                    #
                    # TODO Replace random number generator with statistical analysis
                    # region Statistical Analysis
                    pip_count = generate_current_pip_value()
                    # endregion
                    move_status = validate_move(current_player, player_move)
            # endregion
            if check_status == 999:  # End game condition exists
                break
            bust_a_move(current_player, player_move)
            current_player = 'computer' if current_player == 'human' else 'human'


    # endregion

    # region Game In Progress
    shall_we_play_a_game()
    # endregion
    sys.exit(0)
