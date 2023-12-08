import sqlite3

with sqlite3.connect('/Users/olegkuzo/Desktop/політех/2Курс/МПІС/Курсова/TaskManager/Database/database.db') as db:
    cursor = db.cursor()
    query = """
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY NOT NULL,
            surname STRING,
            name STRING,
            role STRING,
            username STRING,
            password STRING
        );

        CREATE TABLE IF NOT EXISTS projects (
            project_id INTEGER PRIMARY KEY NOT NULL,
            name INTEGER
        );
        
        CREATE TABLE IF NOT EXISTS tasks (
            task_id INTEGER PRIMARY KEY NOT NULL,
            task_name STRING,
            description STRING,
            priority INTEGER,
            deadline STRING,
            project_id INTEGER,
            FOREIGN KEY (project_id) REFERENCES projects(project_id)
        );


        CREATE TABLE IF NOT EXISTS project_users (
            project_id INTEGER,
            user_id INTEGER,
            role STRING,
            PRIMARY KEY (project_id, user_id),
            FOREIGN KEY (project_id) REFERENCES projects(id),
            FOREIGN KEY (user_id) REFERENCES users(id)
        );

        CREATE TABLE IF NOT EXISTS project_tasks (
            project_id INTEGER,
            task_id INTEGER,
            status STRING,
            PRIMARY KEY (project_id, task_id),
            FOREIGN KEY (project_id) REFERENCES projects(id),
            FOREIGN KEY (task_id) REFERENCES tasks(task_id)
        );
    """
    cursor.executescript(query)

