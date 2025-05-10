import pygame
from PyQt6.QtWidgets import *
from PyQt6.QtGui import QImage, QPixmap
from game_logic import *
from gui import *

class GuiLogic(QMainWindow, Ui_MainWindow):
    """
    Class representing the GUI logic for the Pig dice game.
    """
    def __init__(self) -> None:
        """
        Method to initialize the GUI, connect buttons, and begin the first game.
        """
        super().__init__()
        self.setupUi(self)

        self.center_window()

        target_score = self.get_target_score()
        self.game_logic = GameLogic(target_score=target_score)
        self.dice_value = 1

        pygame.init()

        self.roll_button.clicked.connect(self.roll_die_gui)
        self.hold_button.clicked.connect(self.hold_gui)
        self.reset_button.clicked.connect(self.reset_game_gui)
        self.how_to_button.clicked.connect(self.how_to_play)

        self.update_labels()

    def update_dice(self) -> None:
        """
        Method to update the die with the current dice face image.
        """
        dice_image = self.create_dice_face(self.dice_value)
        self.dice_1.setPixmap(dice_image)

    def create_dice_face(self, value: int) -> QPixmap:
        """
        Method to create the dice face based on the rolled value.
        :param value: the rolled dice value
        :return: The dice face
        """
        surface = pygame.Surface((200, 200))
        surface.fill((250, 135, 210))
        pygame.draw.rect(surface, (225, 0, 124), (0, 0, 200, 200), 10)

        positions = {
            1: [(100, 100)],
            2: [(50, 50), (150, 150)],
            3: [(50, 50), (100, 100), (150, 150)],
            4: [(50, 50), (150, 50), (50, 150), (150, 150)],
            5: [(50, 50), (150, 50), (100, 100), (50, 150), (150, 150)],
            6: [(50, 50), (50, 100), (50, 150), (150, 50), (150, 100), (150, 150)],
        }

        for pos in positions.get(value, []):
            pygame.draw.circle(surface, (225, 0, 124), pos, 20)

        image_str = pygame.image.tostring(surface, 'RGB')
        q_image = QImage(image_str, surface.get_width(), surface.get_height(), QImage.Format.Format_RGB888)
        return QPixmap(q_image)

    def roll_die_gui(self) -> None:
        """
        Method to handle the roll button, updating dice, labels, and game.
        """
        roll = self.game_logic.roll_die()
        if roll is None:
            return

        self.dice_value = roll
        self.update_dice()

        if roll == 1:
            self.update_labels()
            self.show_message('Oh no! You rolled a 1. This turn\'s points are lost')
        else:
            self.update_labels()

    def hold_gui(self) -> None:
        """
        Method to handle the hold button, end current turn, and check for game over.
        """
        if not self.game_logic.game_over:
            self.game_logic.hold()
            self.update_labels()

            if self.game_logic.game_over:
                if self.game_logic.turn_count == 1:
                    self.show_message(f'WINNER! You reached {self.game_logic.target_score} points in {self.game_logic.turn_count} turn!',play_again_option=True)
                else:
                    self.show_message(f'WINNER! You reached {self.game_logic.target_score} points in {self.game_logic.turn_count} turns!', play_again_option=True)

    def update_labels(self) -> None:
        """
        Method to update all GUI labels with current game information.
        """
        total, turn = self.game_logic.get_scores()
        self.total_points_label.setText(f'TOTAL POINTS: {total}')
        self.turn_points_label.setText(f'POINTS THIS TURN: {turn}')
        self.turn_label.setText(f'TURN #: {self.game_logic.turn_count + 1}')
        self.target_score_label.setText(f'TARGET SCORE: {self.game_logic.target_score}')

    def show_message(self, text: str, play_again_option: bool = False) -> None:
        """
        Method to display a message box to the user and offer to play again or quit after winning.
        :param text: The message to display.
        :param play_again_option: Whether to show the Play Again/Quit buttons.
        """
        message = QMessageBox()
        message.setIcon(QMessageBox.Icon.Information)
        message.setText(text)
        message.setWindowTitle('PIG: The Dice Game')

        play_again = quit_button = None
        if play_again_option:
            play_again = message.addButton('Play Again', QMessageBox.ButtonRole.AcceptRole)
            quit_button = message.addButton('Quit', QMessageBox.ButtonRole.RejectRole)
        else:
            message.setStandardButtons(QMessageBox.StandardButton.Ok)

        message.move(self.frameGeometry().center() - message.rect().center())
        message.exec()

        if play_again_option:
            if message.clickedButton() == play_again:
                self.reset_game_gui()
            elif message.clickedButton() == quit_button:
                QApplication.quit()

    def get_target_score(self, default: int = 100) -> int:
        """
        Method to prompt the user to enter a target score.
        :param default: The default target score value if the user does not enter one.
        :return: The chosen or default target score.
        """
        intro = (
            'Welcome to PIG: The Dice Game\n'
            '----------------------------------\n'
            '\n'
            'Choose Target Score:\n'
            '\n'
            'Enter # between 10-1000 and select "Ok"\n'
            '\n'
            'OR\n'
            '\n'
            'Select "Cancel" for Default Target Score of 100\n'
            '\n'
        )

        target_score, ok = QInputDialog.getInt(
            self, 'PIG: Start Game', intro, default, 10, 1000, 1
        )
        return target_score if ok else default

    def reset_game_gui(self) -> None:
        """
        Method to reset the game logic and GUI to start a new game.
        """
        self.game_logic = GameLogic(target_score=self.get_target_score())
        self.dice_value = 1
        self.update_dice()
        self.update_labels()
        self.show_message('Game has been reset.')

    def how_to_play(self) -> None:
        """
        Method to display the instructions on how to play Pig.
        """
        instructions = (
            'HOW TO PLAY\n'
            '----------------------\n'
            '\n'
            'Select "ROLL" to roll a six-sided dice.\n'
            'You may roll the dice as many times as you wish per turn.\n'
            'Each roll\'s dice face value adds to your turn score - unless you roll a 1.\n'
            'If a 1 is rolled, lose your turn points and your turn ends.\n'
            'Select "HOLD" to bank your turn points into your total and end the turn.\n'
            'Once the target score is reached, YOU WIN!\n'
        )
        self.show_message(instructions)

    def center_window(self) -> None:
        """
        Method to center the window on the user's screen.
        """
        frame = self.frameGeometry()
        screen = QApplication.primaryScreen().availableGeometry().center()
        frame.moveCenter(screen)
        self.move(frame.topLeft())
