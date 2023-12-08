from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton

class AddTaskDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle('Додати завдання')

        self.task_name_line_edit = QLineEdit(self)
        self.description_line_edit = QLineEdit(self)
        self.deadline_line_edit = QLineEdit(self)
        self.priority_line_edit = QLineEdit(self)

        ok_button = QPushButton('Ок', self)
        ok_button.clicked.connect(self.accept)

        cancel_button = QPushButton('Скасувати', self)
        cancel_button.clicked.connect(self.reject)

        layout = QVBoxLayout()
        layout.addWidget(QLabel('Назва завдання:'))
        layout.addWidget(self.task_name_line_edit)
        layout.addWidget(QLabel('Опис:'))
        layout.addWidget(self.description_line_edit)
        layout.addWidget(QLabel('Термін виконання:'))
        layout.addWidget(self.deadline_line_edit)
        layout.addWidget(QLabel('Пріоритет:'))
        layout.addWidget(self.priority_line_edit)
        layout.addWidget(ok_button)
        layout.addWidget(cancel_button)

        self.setLayout(layout)

    def get_task_data(self):
        task_name = self.task_name_line_edit.text()
        description = self.description_line_edit.text()
        deadline = self.deadline_line_edit.text()
        priority = self.priority_line_edit.text()

        return task_name, description, deadline, priority

