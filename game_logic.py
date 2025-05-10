import random

class GameLogic:
    """
    Class representing the game logic for the Pig dice game (single-player).
    """
    def __init__(self, target_score: int = 100) -> None:
        """
        Method to initialize the game logic with a target score.
        :param target_score: The score required to win the game.
        """
        self.target_score = target_score
        self.reset_game()

    def reset_game(self) -> None:
        """
        Method to reset the game.
        """
        self.total_score = 0
        self.turn_score = 0
        self.turn_count = 0
        self.game_over = False

    def roll_die(self) -> int | None:
        """
        Method to roll a six-sided die.
        :return: The number rolled, or None if the game is over.
        """
        if self.game_over:
            return None
        roll = random.randint(1,6)
        if roll == 1:
            self.turn_score = 0
            self.turn_count += 1
        else:
            self.turn_score += roll
        return roll

    def hold(self) -> None:
        """
        Method to end the current turn, bank the turn score to
        the total score, and check if the user has won the game.
        """
        if self.game_over:
            return
        self.total_score += self.turn_score
        self.turn_score = 0
        self.turn_count += 1

        if self.total_score >= self.target_score:
            self.game_over = True

    def get_scores(self) -> tuple[int, int]:
        """
        Method to return the total score and turn score.
        :return: total score, turn score
        """
        return self.total_score, self.turn_score
