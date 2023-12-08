from PyQt6.QtWidgets import QApplication
from user_interface.authorization_window import AuthorizationWindow
import sys

if __name__ == '__main__':
    app = QApplication(sys.argv)

    authorization = AuthorizationWindow()
    authorization.show()

    sys.exit(app.exec())
