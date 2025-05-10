from gui_logic import *

def main() -> None:
    """
    Function to initialize the application and launch the main window.
    """
    application = QApplication([])
    window = GuiLogic()
    window.show()
    application.exec()

if __name__ == '__main__':
    main()
