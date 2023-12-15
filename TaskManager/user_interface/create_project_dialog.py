from PyQt6.QtWidgets import QDialog, QHBoxLayout, QComboBox, QLineEdit, QLabel, QPushButton, QVBoxLayout, QListWidget, QListWidgetItem
from TaskManager.logic.database_manager import DatabaseManager

class CreateProjectWindow(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Створити новий проект")
        self.setGeometry(100, 100, 500, 300)

        self.layout = QVBoxLayout(self)

        self.project_name_label = QLabel("Назва проекту:")
        self.project_name_edit = QLineEdit(self)

        # Fetch users from the database
        self.available_users = self.fetch_users_from_database()

        user_combo_items = [str(user_id) for user_id in self.available_users.keys()]
        self.user_combo_label = QLabel("Виберіть користувачів:")
        self.user_combo = QComboBox(self)
        self.user_combo.addItems(user_combo_items)

        self.add_user_button = QPushButton("+", self)
        self.add_user_button.clicked.connect(self.add_user_to_list)

        self.remove_user_button = QPushButton("-", self)
        self.remove_user_button.clicked.connect(self.remove_user_from_list)

        self.selected_users_label = QLabel("Вибрані користувачі:")
        self.selected_users_list = QListWidget(self)
        self.selected_users_list.setSelectionMode(QListWidget.SelectionMode.SingleSelection)

        self.create_button = QPushButton("Створити проект", self)
        self.create_button.clicked.connect(self.create_new_project)

        user_selection_layout = QHBoxLayout()
        user_selection_layout.addWidget(self.user_combo_label)
        user_selection_layout.addWidget(self.user_combo)
        user_selection_layout.addWidget(self.add_user_button)
        user_selection_layout.addWidget(self.remove_user_button)

        self.layout.addWidget(self.project_name_label)
        self.layout.addWidget(self.project_name_edit)
        self.layout.addLayout(user_selection_layout)
        self.layout.addWidget(self.selected_users_label)
        self.layout.addWidget(self.selected_users_list)
        self.layout.addWidget(self.create_button)

        self.selected_users_with_roles = []

    def fetch_users_from_database(self):
        self.db_manager = DatabaseManager()
        users = {}

        query = "SELECT user_id, surname, name, role FROM users"
        user_data = self.db_manager.execute_query(query)

        for user_id, surname, name, role in user_data:
            users[user_id] = (surname, name, role)

        return users

    def add_user_to_list(self):
        selected_user = int(self.user_combo.currentText())
        user_role = self.available_users[selected_user]

        self.selected_users_with_roles.append((selected_user, user_role))
        self.selected_users_list.addItem(f"{selected_user} - {user_role}")

    def remove_user_from_list(self):
        selected_item = self.selected_users_list.currentItem()

        if selected_item is not None:
            selected_index = self.selected_users_list.row(selected_item)
            self.selected_users_with_roles.pop(selected_index)
            self.selected_users_list.takeItem(selected_index)

    def create_new_project(self):
        project_name = self.project_name_edit.text()

        if not self.selected_users_with_roles:
            print("No selected users for the project.")
            return

        self.db_manager.insert_project_and_users(project_name, self.selected_users_with_roles)

        item = QListWidgetItem(project_name)
        self.selected_users_list.addItem(item)

        print(f"New project created: {project_name}")
        print("Selected Users with Roles:", self.selected_users_with_roles)

        self.accept()

    def get_project_data(self):
        project_name = self.project_name_edit.text()
        return project_name, self.selected_users_with_roles
