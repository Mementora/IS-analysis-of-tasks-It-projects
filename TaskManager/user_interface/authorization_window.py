import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QGridLayout, QMessageBox
from PyQt6.QtCore import Qt
from TaskManager.user_interface import projects_list_window
from TaskManager.logic import database_manager

class AuthorizationWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Авторизація')

        window_width = 250
        window_height = 250

        self.resize(window_height, window_width)

        # Widgets
        self.label_username = QLabel('Логін:')
        self.label_password = QLabel('Пароль:')
        self.edit_username = QLineEdit(self)
        self.edit_password = QLineEdit(self)
        self.edit_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.button_login = QPushButton('Авторизуватись', self)
        self.button_exit = QPushButton('Вихід', self)
        self.button_login.clicked.connect(self.login)
        self.button_exit.clicked.connect(QApplication.instance().quit)

        # Set the maximum width for the fields
        max_field_width = 200
        self.edit_username.setMaximumWidth(max_field_width)
        self.edit_password.setMaximumWidth(max_field_width)

        # Create a grid layout for username and password
        grid_layout = QGridLayout()
        grid_layout.addWidget(self.label_username, 0, 1, alignment=Qt.AlignmentFlag.AlignCenter)
        grid_layout.addWidget(self.edit_username, 1, 1)
        grid_layout.addWidget(self.label_password, 2, 1, alignment=Qt.AlignmentFlag.AlignCenter)
        grid_layout.addWidget(self.edit_password, 3, 1)
        grid_layout.setHorizontalSpacing(5)  # Set horizontal spacing between items

        # Create a vertical layout for the entire window
        main_layout = QVBoxLayout()
        main_layout.addLayout(grid_layout)
        main_layout.addWidget(self.button_login, alignment=Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.button_exit, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(main_layout)

        # Center the window on the screen
        self.center()

    def center(self):
        screen = QApplication.primaryScreen()
        center_point = screen.availableGeometry().center()
        self.move(center_point - self.rect().center())

    def login(self):
        username = self.edit_username.text()
        password = self.edit_password.text()
        db_manager = database_manager.DatabaseManager()

        user = db_manager.check_credentials(username, password)

        if user:
            self.close()
            role = db_manager.get_user_role(user)
            self.project_list = projects_list_window.ProjectListMenu()
            self.project_list.set_user_role(role)
            self.project_list.show()
        else:
            QMessageBox.warning(self, 'Авторизація скасована', 'неправильний логін і/або пароль, повіторіть ще раз.')

    @staticmethod
    def create_and_show_login():
        app = QApplication(sys.argv)
        window = AuthorizationWindow()
        window.show()
        sys.exit(app.exec())