import sqlite3

# Connect to the database
with sqlite3.connect('/Users/olegkuzo/Desktop/політех/2Курс/МПІС/Курсова/TaskManager/Database/database.db') as db:
    cursor = db.cursor()

    # Insert data into the "users" table
    user_data = (0, 'Kuzo', 'Oleh', 'Admin', 'a', 'd')
    cursor.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?, ?)", user_data)

    # # Insert data into the "tasks" table for a specific project (e.g., "Project1")
    # task_data = (1, 'Task description', 1, '2023-12-31', 'Incomplete')
    # cursor.execute("INSERT INTO Project1_tasks VALUES (?, ?, ?, ?, ?)", task_data)

    # project_data = (2, "TestC")
    # cursor.execute("INSERT INTO projects VALUES (?,?)", project_data)

    # Commit the changes to the database
    db.commit()

print("Data added successfully.")
