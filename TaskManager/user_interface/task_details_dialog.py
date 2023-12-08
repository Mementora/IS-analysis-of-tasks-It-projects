from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton

class TaskDetailsDialog(QDialog):
    def __init__(self, task_details, parent=None):
        super().__init__(parent)

        self.setWindowTitle('Деталі завдання')

        # Display task details
        label_task_name = QLabel('Назва:')
        self.line_edit_task_name = QLineEdit(task_details.get('Task Name', ''))
        self.line_edit_task_name.setReadOnly(True)

        label_description = QLabel('Опис:')
        self.line_edit_description = QLineEdit(task_details.get('Description', ''))
        self.line_edit_description.setReadOnly(True)

        label_priority = QLabel('Пріоритет:')
        self.line_edit_priority = QLineEdit(str(task_details.get('Priority', '')))
        self.line_edit_priority.setReadOnly(True)

        label_deadline = QLabel('Термін виконання:')
        self.line_edit_deadline = QLineEdit(str(task_details.get('Deadline', '')))
        self.line_edit_deadline.setReadOnly(True)

        # Add OK button to close the dialog
        ok_button = QPushButton('OK', self)
        ok_button.clicked.connect(self.accept)

        # Set up the layout
        layout = QVBoxLayout()
        layout.addWidget(label_task_name)
        layout.addWidget(self.line_edit_task_name)
        layout.addWidget(label_description)
        layout.addWidget(self.line_edit_description)
        layout.addWidget(label_priority)
        layout.addWidget(self.line_edit_priority)
        layout.addWidget(label_deadline)
        layout.addWidget(self.line_edit_deadline)
        layout.addWidget(ok_button)

        self.setLayout(layout)
