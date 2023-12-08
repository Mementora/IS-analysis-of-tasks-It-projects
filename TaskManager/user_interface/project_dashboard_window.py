from PyQt6.QtGui import QDrag
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout,
    QLabel, QListWidget, QListWidgetItem, QWidget, QPushButton, QDialog
)
from user_interface.add_task_dialog import AddTaskDialog
from user_interface.task_details_dialog import TaskDetailsDialog
from user_interface import projects_list_window
from logic.database_manager import DatabaseManager
from PyQt6.QtCore import Qt, QMimeData, QByteArray, QDataStream
import sys

class TrelloDashboard(QMainWindow):
    def __init__(self, project_name):
        super().__init__()

        self.project_name = project_name
        self.db_manager = DatabaseManager()  # Replace with your actual DatabaseManager instance
        self.task_details_dict = {}  # Initialize task_details_dict
        self.current_list = None  # Initialize the current_list
        self.lists = []
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle(f'Дошка проекту - {self.project_name}')

        # Create main layout
        main_layout = QHBoxLayout()

        # Create columns (lists) with QListWidgets and labels
        self.lists = [
            (QLabel("To-Do", self), QListWidget(self)),
            (QLabel("In Progress", self), QListWidget(self)),
            (QLabel("Done", self), QListWidget(self))
        ]

        for _, lst in self.lists:
            lst.setDragEnabled(True)
            lst.setAcceptDrops(True)
            lst.setDefaultDropAction(Qt.DropAction.MoveAction)
            lst.setDropIndicatorShown(True)

        for label, lst in self.lists:
            lst.itemClicked.connect(self.show_task_details)

        # Add labels and lists to the main layout
        for label, lst in self.lists:
            main_layout.addWidget(label)
            main_layout.addWidget(lst)

        # Create a central widget and set the main layout
        central_widget = QWidget(self)
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # Fetch and display all tasks from the "project_tasks" table for each list
        self.refresh_ui()


        # Create a vertical layout for the buttons
        button_layout = QVBoxLayout()

        back_button = QPushButton("Назад", self)
        back_button.clicked.connect(self.close_window)

        # Set the main layout for the central widget
        main_layout.addLayout(button_layout)

        # Create an add task button
        add_task_button = QPushButton("Добавити завдання", self)
        add_task_button.clicked.connect(self.show_add_task_dialog)

        # Add the add_task_button to the button_layout
        button_layout.addWidget(add_task_button)
        button_layout.addWidget(back_button)

    def close_window(self):
        self.close()
        self.list_window = projects_list_window.ProjectListMenu()
        self.list_window.show()

    def mousePressEvent(self, event):
        for label, lst in self.lists:
            if isinstance(lst, QListWidget):
                item = lst.itemAt(event.pos())
                if item and event.button() == Qt.MouseButton.LeftButton:
                    mime_data = QMimeData()
                    mime_data.setText(item.text())

                    drag = QDrag(self)
                    drag.setMimeData(mime_data)
                    drag.exec()

    def dragEnterEvent(self, event):
        if event.mimeData().hasText() and event.source() != self.current_list:
            # Print debug information
            print(f"Drag Enter: {event.mimeData().text()} from {event.source().objectName()} to {self.current_list.objectName()}")

            # Set the accepted action
            event.acceptProposedAction()

    def dropEvent(self, event):
        if event.mimeData().hasText():
            text = event.mimeData().text()

            source_list = event.source()
            target_list = self.current_list

            if source_list and target_list and source_list != target_list:

                # Get the task ID from the item's data
                task_id = event.mimeData().data(Qt.ItemDataRole.UserRole)

                # Update the task status in the database
                source_status = source_list.objectName()
                target_status = target_list.objectName()
                self.db_manager.move_task_to_list(task_id, target_status, self.project_name)

                # Refresh the UI
                self.refresh_ui()

    def set_current_list(self):
        sender_list = self.sender()
        self.current_list = sender_list

    def move_task(self, target_status):
        try:
            if self.current_list:
                # Get the task IDs of selected tasks in the current list
                task_ids = [self.current_list.indexFromItem(item).row() for item in self.current_list.selectedItems()]

                # Update the status of selected tasks in the database
                for task_id in task_ids:
                    self.db_manager.move_task_to_list(task_id, target_status, self.project_name)

                # Refresh the UI
                self.refresh_ui()
        except Exception as e:
            print(f"Exception in move_task: {e}")

    def refresh_ui(self):

        # Clear all lists
        for _, lst in self.lists:
            lst.clear()

        # Fetch all tasks for the project
        project_id = self.db_manager.get_project_id(self.project_name)
        all_tasks = self.db_manager.get_all_tasks_for_project(project_id)

        for task_id, task_name, status in all_tasks:
            # Find the list corresponding to the task status
            target_list = next((lst for _, lst in self.lists if lst.objectName() == status), None)

            if not target_list:
                # Use a default list (e.g., the first list) if the status is not found
                target_list = self.lists[0][1]

            item = QListWidgetItem(task_name)
            item.setData(Qt.ItemDataRole.UserRole, task_id)  # Set task ID as user data
            target_list.addItem(item)

    def show_add_task_dialog(self):
        # Fetch the list of programmers from the database
        programmers = self.db_manager.get_programmers()

        # Create a simple dialog to add a new task
        dialog = AddTaskDialog(self)
        result = dialog.exec()

        if result == QDialog.DialogCode.Accepted:
            new_task = dialog.get_task_data()

            # Get the project_id for the current project
            project_id = self.db_manager.get_project_id(self.project_name)

            # Insert the new task into the database with the project_id
            task_id = self.db_manager.add_task(new_task[0], new_task[1], new_task[2], new_task[3], project_id)

            # Update "project_tasks" table with the new task
            self.db_manager.add_task_to_project(self.project_name, task_id)

            # Update the UI
            current_list = self.lists[0][1]  # Assuming the task is added to the "To-Do" list
            current_list.addItem(QListWidgetItem(new_task[0]))

            # Refresh the UI to ensure consistency
            self.refresh_ui()
        else:
            print("Task addition canceled.")

    def show_task_details(self, item):
        task_id = item.data(Qt.ItemDataRole.UserRole)

        project_id = self.db_manager.get_project_id(self.project_name)

        task_details = self.db_manager.get_task_details(task_id, project_id)

        print("Task Details:", task_details)

        if task_details:
            dialog = TaskDetailsDialog({
                'Task Name': task_details.get('task_name', ''),
                'Description': task_details.get('description', ''),
                'Priority': task_details.get('priority', ''),
                'Deadline': task_details.get('deadline', ''),
            }, self)
            dialog.exec()
        else:
            print(f"Task with ID {task_id} does not exist in the project.")

    def fetch_task_details(self, task_id, project_id):
        task_details = self.db_manager.get_task_details(task_id, project_id)

        adjusted_task_details = {
            'Назва': task_details.get('task_name', ''),
            'Опис': task_details.get('description', ''),
            'Пріоритет': task_details.get('priority', ''),
            'Термін виконання': task_details.get('deadline', ''),
        }

        return adjusted_task_details


def create_and_show_window():
    app = QApplication(sys.argv)
    ex = TrelloDashboard("Default Project")
    ex.show()

    # Start the application event loop
    sys.exit(app.exec())
