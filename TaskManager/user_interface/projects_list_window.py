from PyQt6.QtWidgets import QWidget, QDialog, QLabel, QPushButton, QVBoxLayout, QGridLayout, QApplication, QListWidget, QListWidgetItem
from PyQt6.QtCore import Qt
from TaskManager.user_interface import authorization_window
from TaskManager.user_interface.create_project_dialog import CreateProjectWindow
from TaskManager.user_interface.project_dashboard_window import TrelloDashboard
from TaskManager.logic.database_manager import DatabaseManager

import sys

class ProjectListMenu(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ProjectWindow()

    def init_ProjectWindow(self):
        self.setWindowTitle('Вибір проекту')

        window_width = 800
        window_height = 600

        self.resize(window_width, window_height)

        # Widgets
        self.label_user_role = QLabel('Admin', self)
        self.label_project_list = QLabel('Список проектів', self)

        # Create list widget
        self.list_widget = QListWidget(self)

        # projects from db
        # Create an instance of the DatabaseManager
        self.db_manager = DatabaseManager()

        # Fetch projects from the database
        projects = self.fetch_projects_from_database()

        for project in projects:
            item = QListWidgetItem(project)
            self.list_widget.addItem(item)

        self.button_create_project = QPushButton('Створити новий проект', self)
        self.button_create_project.clicked.connect(self.create_new_project)
        self.button_logoff = QPushButton('Вийти з аккаунту', self)
        self.button_exit = QPushButton('Вихід', self)

        self.list_widget.itemDoubleClicked.connect(self.open_project)
        self.button_logoff.clicked.connect(self.logoff)
        self.button_exit.clicked.connect(QApplication.instance().quit)

        # Set the maximum width for the fields
        max_field_width = 200

        # Create a grid layout for labels and buttons
        grid_layout = QGridLayout()
        grid_layout.addWidget(self.label_user_role, 0, 0, 1, 2, alignment=Qt.AlignmentFlag.AlignCenter)
        grid_layout.addWidget(self.label_project_list, 1, 0, 1, 2, alignment=Qt.AlignmentFlag.AlignCenter)
        grid_layout.addWidget(self.list_widget, 2, 0, 11, 1)
        grid_layout.addWidget(self.button_create_project, 2, 1, 1, 1)
        grid_layout.addWidget(self.button_logoff, 3, 1, 1, 1)
        grid_layout.addWidget(self.button_exit, 4, 1, 1, 1)
        grid_layout.setHorizontalSpacing(5)  # Set horizontal spacing between items

        # Create a vertical layout for the entire window
        main_layout = QVBoxLayout()
        main_layout.addLayout(grid_layout)

        self.setLayout(main_layout)
        self.center()
    def center(self):
        screen = QApplication.primaryScreen()
        center_point = screen.availableGeometry().center()
        self.move(center_point - self.rect().center())

    def fetch_projects_from_database(self):
        projects = []

        query = "SELECT name FROM projects"
        project_names = self.db_manager.execute_query(query)

        for project_name in project_names:
            projects.append(str(project_name[0]))

        return projects

    def set_user_role(self, role):
        self.label_user_role.setText(role)

    def create_new_project(self):
        create_project_dialog = CreateProjectWindow()
        result = create_project_dialog.exec()

        if result == QDialog.DialogCode.Accepted:
            project_name, selected_users = create_project_dialog.get_project_data()

            item = QListWidgetItem(project_name)
            self.list_widget.addItem(item)

    def logoff(self):
        self.login_window = authorization_window.AuthorizationWindow()
        self.login_window.show()
        self.close()

    def open_project(self, item):
        self.close()
        project_name = item.text()
        self.trello_dashboard = TrelloDashboard(project_name)
        self.trello_dashboard.show()


def create_and_show_list(cls):
    window = cls()
    window.show()
    QApplication.instance().exec()
