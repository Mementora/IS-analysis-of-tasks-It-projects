import sqlite3

class DatabaseManager:
    def __init__(self, db_path='/Users/olegkuzo/Desktop/політех/2Курс/МПІС/Курсова/TaskManager/Database/database.db'):
        self.db_path = db_path

    def check_credentials(self, username, password):
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user_data = cursor.fetchone()

        connection.close()

        if user_data:
            user = {
                'username': user_data[1],
                'password': user_data[2],
                'role': user_data[3]
            }
            return user
        else:
            return None

    def get_user_role(self, user):
        return user["role"] if user else None

    def execute_query(self, query, params=None):
        with sqlite3.connect(self.db_path) as connection:
            cursor = connection.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            result = cursor.fetchall()
        return result

    def insert_project_and_users(self, project_name, users_with_roles):
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()

        try:
            cursor.execute("INSERT INTO projects (name) VALUES (?)", (project_name,))
            project_id = cursor.lastrowid
            print("Inserted project with ID:", project_id)

            for user_id, role in users_with_roles:
                cursor.execute("INSERT INTO project_users (project_id, user_id, role) VALUES (?, ?, ?)",
                               (project_id, user_id, role[2]))
                print(f"Inserted project_user: project_id={project_id}, user_id={user_id}, role={role[2]}")

            connection.commit()
        except sqlite3.Error as e:
            print("SQLite error:", e)
            connection.rollback()
        finally:
            connection.close()

    def get_tasks_for_list(self, list_name):
        query = "SELECT task_name FROM tasks WHERE status = ?"
        params = (list_name,)
        tasks = self.execute_query(query, params)
        return [task[0] for task in tasks]

    def get_programmers(self):
        query = "SELECT name FROM users WHERE role = 'Programmer'"
        programmer_names = self.execute_query(query)
        return [programmer[0] for programmer in programmer_names]

    def add_task(self, task_name, description, priority, deadline, project_id):
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()

        try:
            cursor.execute("""
                INSERT INTO tasks (task_name, description, priority, deadline, project_id)
                VALUES (?, ?, ?, ?, ?)
            """, (task_name, description, priority, deadline, project_id))

            task_id = cursor.lastrowid
            print("Inserted task with ID:", task_id)

            connection.commit()
            return task_id
        except sqlite3.Error as e:
            print("SQLite error:", e)
            connection.rollback()
            return None
        finally:
            connection.close()

    def add_task_to_project_by_name(self, project_name, task_id):
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()

        try:
            # Retrieve the project_id for the given project_name
            project_id = self.get_project_id(project_name)

            # Insert the task into the project_tasks table with the correct project_id
            cursor.execute("INSERT INTO project_tasks (project_id, task_id) VALUES (?, ?)", (project_id, task_id))
            print(f"Inserted project_task: project_id={project_id}, task_id={task_id}")

            connection.commit()
        except sqlite3.Error as e:
            print("SQLite error:", e)
            connection.rollback()
        finally:
            connection.close()

    def get_task_names_for_list(self, project_id, list_name):
        query = """
                  SELECT tasks.description
                  FROM project_tasks
                  JOIN tasks ON project_tasks.task_id = tasks.task_id
                  WHERE project_tasks.project_id = ? AND tasks.status = ?
              """
        params = (project_id, list_name)
        result = self.execute_query(query, params)
        return [task_name[0] for task_name in result]

    def get_project_id(self, project_name):
        query = "SELECT project_id FROM projects WHERE name = ?"
        params = (project_name,)
        result = self.execute_query(query, params)
        return result[0][0] if result else None

    def get_all_tasks_for_project(self, project_id):
        query = """
            SELECT tasks.task_id, tasks.description, project_tasks.status
            FROM project_tasks
            JOIN tasks ON project_tasks.task_id = tasks.task_id
            WHERE project_tasks.project_id = ?
        """
        params = (project_id,)
        print("Executing query:", query, "with params:", params)
        tasks = self.execute_query(query, params)
        print("Tasks for project:", tasks)
        return tasks

    def get_task_status(self, task_id, project_name):
        query = """
            SELECT tasks.status
            FROM project_tasks
            JOIN tasks ON project_tasks.task_id = tasks.task_id
            WHERE project_tasks.task_id = ? AND project_tasks.project_id = (SELECT project_id FROM projects WHERE name = ?)
        """
        result = self.execute_query(query, (task_id, project_name))
        return result.fetchone()[0] if result else None

    def move_task_to_list(self, task_id, target_status, project_name):

        try:
            # Update the task status in the database
            query = "UPDATE project_tasks SET status = ? WHERE task_id = ? AND project_id = ?"

            with sqlite3.connect(self.db_path) as connection:
                cursor = connection.cursor()
                cursor.execute(query, (target_status, task_id, project_name))
                connection.commit()

            print(f"Task {task_id} moved to {target_status} in the database.")

        except Exception as e:
            print(f"Error in move_task_to_list: {e}")

    def add_task_to_project(self, project_name, task_id):
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()

        try:
            # Retrieve the project_id for the given project_name
            project_id = self.get_project_id(project_name)

            # Insert the task into the project_tasks table with the correct project_id
            cursor.execute("INSERT INTO project_tasks (project_id, task_id) VALUES (?, ?)", (project_id, task_id))
            print(f"Inserted project_task: project_id={project_id}, task_id={task_id}")

            connection.commit()
        except sqlite3.Error as e:
            print("SQLite error:", e)
            connection.rollback()
        finally:
            connection.close()

    def move_task(self, task_ids, new_status):
        try:
            # Update the status of selected tasks in the tasks table
            with sqlite3.connect(self.db_path) as connection:
                cursor = connection.cursor()

                for task_id in task_ids:
                    # Update the status in the tasks table
                    update_task_query = "UPDATE tasks SET status = ? WHERE task_id = ?"
                    cursor.execute(update_task_query, (new_status, task_id))

                connection.commit()

        except sqlite3.Error as e:
            print("SQLite error:", e)
            # No need for connection.rollback() here because the 'with' statement handles it

    def update_task_status(self, task_id, project_name, new_status):
        try:
            # Update the status for 'tasks' table
            query = """
                   UPDATE tasks
                   SET status = ?
                   WHERE task_id = ? AND project_id = (SELECT project_id FROM projects WHERE name = ?)
               """
            self.execute_query(query, (new_status, task_id, project_name))
        except Exception as e:
            print(f"Exception in update_task_status: {e}")

    def get_task_details(self, task_id, project_id):
        query = """
            SELECT task_name, description, priority, deadline
            FROM tasks
            WHERE task_id = ? AND project_id = ?
        """
        params = (task_id, project_id)
        result = self.execute_query(query, params)

        if result:
            task_details = {
                'task_name': result[0][0],
                'description': result[0][1],
                'priority': result[0][2],
                'deadline': result[0][3],
            }
            return task_details
        else:
            return None  # Return None if the task does not exist