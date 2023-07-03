import os
from datetime import datetime, date

# Function to register a new user
def reg_user():
    while True:
        new_username = input("New Username: ")
        if new_username in username_password.keys():
            print("Username taken!")
            continue
        new_password = input("New Password: ")
        confirm_password = input("Confirm Password: ")
        if new_password == confirm_password:
            print("New user added")
            username_password[new_username] = new_password
            
            with open("user.txt", "w") as out_file:
                user_data = []
                for k in username_password:
                    user_data.append(f"{k};{username_password[k]}")
                out_file.write("\n".join(user_data))
        else:
            print("Passwords do no match")
        break

# Function to add a new task
def add_task():
    task_username = input("Name of person assigned to task: ")
    if task_username not in username_password.keys():
        print("User does not exist. Please enter a valid username")
    task_title = input("Title of Task: ")
    task_description = input("Description of Task: ")
    while True:
        try:
            task_due_date = input("Due date of task (YYYY-MM-DD): ")
            due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
            break

        except ValueError:
            print("Invalid datetime format. Please use the format specified")


    # Get the current date.
    curr_date = date.today()
  
    # Create a new task with the provided information
    new_task = {
        "username": task_username,
        "title": task_title,
        "description": task_description,
        "due_date": due_date_time,
        "assigned_date": curr_date,
        "completed": False
    }
    # Add the task to the task_list and save it
    task_list.append(new_task)
    save_tasks()
    print("Task successfully added.")

# Function to save the tasks and changes to them to the file 
def save_tasks():
    with open("tasks.txt", "w") as task_file:
        task_list_to_write = []
        for t in task_list:
            str_attrs = [
                t['username'],
                t['title'],
                t['description'],
                t['due_date'].strftime(DATETIME_STRING_FORMAT),
                t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                "Yes" if t['completed'] else "No"
            ]
            task_list_to_write.append(";".join(str_attrs))
        task_file.write("\n".join(task_list_to_write))

# Function to view all tasks
def view_all():
    for t in task_list:
        disp_str = f"Task: \t\t {t['title']}\n"
        disp_str += f"Assigned to: \t {t['username']}\n"
        disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Task Description: \n {t['description']}\n"
        print(disp_str)

# Function to view tasks assigned to the current user
def view_mine():
    for i, t in enumerate(task_list):
        if t['username'] == curr_user:
            disp_str = f"Task Number: {i+1}\n"
            disp_str += f"Task: \t\t {t['title']}\n"
            disp_str += f"Assigned to: \t {t['username']}\n"
            disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Task Description: \n {t['description']}\n"
            disp_str += f"Task completed?: \t {t['completed']}\n"
            print(disp_str)

# Function to edit tasks 
def edit_task():
    task_number = input("Enter the number of the task you want to edit (-1 to return to the main menu): ")
    if task_number == "-1":
        return

    try:
        task_index = int(task_number) - 1
        if task_index < 0 or task_index >= len(task_list):
            print("Invalid task number")
            return

        selected_task = task_list[task_index]
        print("Selected Task:")
        print(f"Title: {selected_task['title']}")
        print(f"Assigned to: {selected_task['username']}")
        print(f"Due Date: {selected_task['due_date'].strftime(DATETIME_STRING_FORMAT)}")
        print(f"Description: {selected_task['description']}")
        print(f"Completed: {'Yes' if selected_task['completed'] else 'No'}")

        if selected_task['completed']:
            print("This task has been completed and cannot be edited.")
            return

        edit_choice = input("Enter 'U' to edit the username or 'D' to edit the due date: ").upper()

        if edit_choice == 'U':
            new_username = input("Enter the new username: ")
            if new_username in username_password.keys():
                selected_task['username'] = new_username
                save_tasks()
                print("Username updated.")
            else:
                print("Invalid username")

        elif edit_choice == 'D':
            if not selected_task['completed']:
                new_due_date = input("Enter the new due date (YYYY-MM-DD): ")
                try:
                    due_date = datetime.strptime(new_due_date, DATETIME_STRING_FORMAT)
                    selected_task['due_date'] = due_date
                    save_tasks()
                    print("Due date updated.")
                except ValueError:
                    print("Invalid datetime format. Please use the format specified.")
            else:
                print("Task is already completed. Cannot change the due date.")

        else:
            print("Invalid choice")

    except ValueError:
        print("Invalid input. Please enter a valid task number.")

# Function to mark tasks as completed   
def mark_task_complete():
    task_num = int(input("Enter the task number to mark as complete: "))
    task_index = task_num - 1

    if task_index < 0 or task_index >= len(task_list):
        print("Invalid task number.")
        return

    task = task_list[task_index]

    if task['completed']:
        print("This task is already marked as complete.")
    else:
        task['completed'] = True
        save_tasks()
        print("Task marked as complete.")

# Function to generate and display statistics
def display_statistics():
    # Read task data from file
    with open("tasks.txt", "r") as task_file:
        tasks = task_file.readlines()

    # Read user data from file
    with open("user.txt", "r") as user_file:
        users = user_file.readlines()

    # Calculate task statistics
    total_tasks = len(tasks)
    completed_tasks = sum(task.split(";")[5].strip() == "Yes" for task in tasks)
    incomplete_tasks = total_tasks - completed_tasks
    overdue_tasks = sum(datetime.strptime(task.split(";")[3].strip(), "%Y-%m-%d") < datetime.today() and task.split(";")[5].strip() == "No" for task in tasks)
    task_completion_percentage = ((total_tasks - completed_tasks) / total_tasks) * 100
    overdue_percentage = (overdue_tasks / total_tasks) * 100

    # Calculate user statistics
    total_users = len(users)
    assigned_tasks = [task for task in tasks if task.split(";")[0].strip()]
    user_stats = []
    for user in users:
        user_tasks = [task for task in assigned_tasks if task.split(";")[0].strip() == user.split(";")[0].strip()]
        user_completed = sum(task.split(";")[5].strip() == "Yes" for task in user_tasks)
        user_assigned_percentage = (len(user_tasks) / total_tasks) * 100
        if len(user_tasks) > 0:
            user_completed_percentage = (user_completed / len(user_tasks)) * 100
        else:
            user_completed_percentage = 0
        user_incomplete = len(user_tasks) - user_completed
        user_overdue = sum(datetime.strptime(task.split(";")[3].strip(), "%Y-%m-%d") < datetime.today() and task.split(";")[5].strip() == "No" for task in user_tasks)
        if len(user_tasks) > 0:
            user_overdue_percentage = (user_overdue / len(user_tasks)) * 100
        else:
            user_overdue_percentage = 0
        user_stats.append({
            "user": user.split(";")[0].strip(),
            "total_assigned": len(user_tasks),
            "assigned_percentage": user_assigned_percentage,
            "completed_percentage": user_completed_percentage,
            "incomplete": user_incomplete,
            "overdue": user_overdue,
            "overdue_percentage": user_overdue_percentage
        })

    # Display task statistics
    print("Task Overview")
    print("--------------")
    print(f"Total tasks generated and tracked using task_manager.py: {total_tasks}")
    print(f"Total completed tasks: {completed_tasks}")
    print(f"Total incomplete tasks: {incomplete_tasks}")
    print(f"Total tasks that haven't been completed and are overdue: {overdue_tasks}")
    print(f"Percentage of tasks that are incomplete: {task_completion_percentage:.2f}%")
    print(f"Percentage of tasks that are overdue: {overdue_percentage:.2f}%")
    print()

    # Display user statistics
    print("User Overview")
    print("--------------")
    print(f"Total users registered with task_manager.py: {total_users}")
    print(f"Total tasks generated and tracked using task_manager.py: {total_tasks}")
    print()
    for user_stat in user_stats:
        print(f"User: {user_stat['user']}")
        print(f"Total tasks assigned to the user: {user_stat['total_assigned']}")
        print(f"Percentage of total tasks assigned: {user_stat['assigned_percentage']:.2f}%")
        print(f"Percentage of assigned tasks completed: {user_stat['completed_percentage']:.2f}%")
        print(f"Tasks assigned but not completed: {user_stat['incomplete']}")
        print(f"Tasks assigned and overdue: {user_stat['overdue']}")
        print(f"Percentage of assigned tasks that are overdue: {user_stat['overdue_percentage']:.2f}%")
        print()

# Function to generate text files with reports about tasks and users
def generate_reports():
    # Read task data from file
    with open("tasks.txt", "r") as task_file:
        tasks = task_file.readlines()

    # Read user data from file
    with open("user.txt", "r") as user_file:
        users = user_file.readlines()

    # Calculate task statistics
    total_tasks = len(tasks)
    completed_tasks = sum(task.split(";")[5].strip() == "Yes" for task in tasks)
    incomplete_tasks = total_tasks - completed_tasks
    overdue_tasks = sum(datetime.strptime(task.split(";")[3].strip(), "%Y-%m-%d") < datetime.today() and task.split(";")[5].strip() == "No" for task in tasks)
    task_completion_percentage = (total_tasks - completed_tasks) / total_tasks * 100
    overdue_percentage = (overdue_tasks / total_tasks) * 100

    # Calculate user statistics
    total_users = len(users)
    assigned_tasks = [task for task in tasks if task.split(";")[0].strip()]
    user_stats = []
    for user in users:
        user_tasks = [task for task in assigned_tasks if task.split(";")[0].strip() == user.split(";")[0].strip()]
        user_completed = sum(task.split(";")[5].strip() == "Yes" for task in user_tasks)
        user_assigned_percentage = (len(user_tasks) / total_tasks) * 100
        if len(user_tasks) > 0:
            user_completed_percentage = (user_completed / len(user_tasks)) * 100
        else:
            user_completed_percentage = 0
        user_incomplete = len(user_tasks) - user_completed
        user_overdue = sum(datetime.strptime(task.split(";")[3].strip(), "%Y-%m-%d") < datetime.today() and task.split(";")[5].strip() == "No" for task in user_tasks)
        if len(user_tasks) > 0:
            user_overdue_percentage = (user_overdue / len(user_tasks)) * 100
        else:
            user_overdue_percentage = 0
        user_stats.append({
            "user": user.split(";")[0].strip(),
            "total_assigned": len(user_tasks),
            "assigned_percentage": user_assigned_percentage,
            "completed_percentage": user_completed_percentage,
            "incomplete": user_incomplete,
            "overdue": user_overdue,
            "overdue_percentage": user_overdue_percentage
        })

    # Generate task overview report
    with open("task_overview.txt", "w") as task_report:
        task_report.write("Task Overview\n")
        task_report.write("--------------\n")
        task_report.write(f"Total tasks generated and tracked using task_manager.py: {total_tasks}\n")
        task_report.write(f"Total completed tasks: {completed_tasks}\n")
        task_report.write(f"Total incomplete tasks: {incomplete_tasks}\n")
        task_report.write(f"Total tasks that haven't been completed and are overdue: {overdue_tasks}\n")
        task_report.write(f"Percentage of tasks that are incomplete: {task_completion_percentage:.2f}%\n")
        task_report.write(f"Percentage of tasks that are overdue: {overdue_percentage:.2f}%\n")

    # Generate user overview report
    with open("user_overview.txt", "w") as user_report:
        user_report.write("User Overview\n")
        user_report.write("--------------\n")
        user_report.write(f"Total users registered with task_manager.py: {total_users}\n")
        user_report.write(f"Total tasks generated and tracked using task_manager.py: {total_tasks}\n")
        user_report.write("\n")
        for user_stat in user_stats:
            user_report.write(f"User: {user_stat['user']}\n")
            user_report.write(f"Total tasks assigned to the user: {user_stat['total_assigned']}\n")
            user_report.write(f"Percentage of total tasks assigned: {user_stat['assigned_percentage']:.2f}%\n")
            user_report.write(f"Percentage of assigned tasks completed: {user_stat['completed_percentage']:.2f}%\n")
            user_report.write(f"Tasks assigned but not completed: {user_stat['incomplete']}\n")
            user_report.write(f"Tasks assigned and overdue: {user_stat['overdue']}\n")
            user_report.write(f"Percentage of assigned tasks that are overdue: {user_stat['overdue_percentage']:.2f}%\n")
            user_report.write("\n")


DATETIME_STRING_FORMAT = "%Y-%m-%d"

# Create tasks.txt if it doesn't exist
if not os.path.exists("tasks.txt"):
    with open("tasks.txt", "w") as default_file:
        pass

with open("tasks.txt", 'r') as task_file:
    task_data = task_file.read().split("\n")
    task_data = [t for t in task_data if t != ""]


task_list = []
for t_str in task_data:
    curr_t = {}

    # Split by semicolon and manually add each component
    task_components = t_str.split(";")
    curr_t['username'] = task_components[0]
    curr_t['title'] = task_components[1]
    curr_t['description'] = task_components[2]
    curr_t['due_date'] = datetime.strptime(task_components[3], DATETIME_STRING_FORMAT)
    curr_t['assigned_date'] = datetime.strptime(task_components[4], DATETIME_STRING_FORMAT)
    curr_t['completed'] = True if task_components[5] == "Yes" else False

    task_list.append(curr_t)


#====Login Section====
'''This code reads usernames and password from the user.txt file to 
    allow a user to login.
'''
# If no user.txt file, write one with a default account
if not os.path.exists("user.txt"):
    with open("user.txt", "w") as default_file:
        default_file.write("admin;password")

# Read in user_data
with open("user.txt", 'r') as user_file:
    user_data = user_file.read().split("\n")

# Convert to a dictionary
username_password = {}
for user in user_data:
    username, password = user.split(';')
    username_password[username] = password

logged_in = False
while not logged_in:

    print("LOGIN")
    curr_user = input("Username: ")
    curr_pass = input("Password: ")
    if curr_user not in username_password.keys():
        print("User does not exist")
        continue
    elif username_password[curr_user] != curr_pass:
        print("Wrong password")
        continue
    else:
        print("Login Successful!")
        logged_in = True


# Main operating loop of the program
while True:
    print()
    
    # If statement depending on which different menu is displayed
    if curr_user == 'admin':
        menu = input('''Select one of the following options below:
r - Register a user
a - Add a task
va - View all tasks
vm - View my tasks
gr - Generate reports
ds - Display statistics
e - Exit
''')
    else:
        menu = input('''Select one of the following options below:
r - Register a user
a - Add a task
va - View all tasks
vm - View my tasks
e - Exit
''')

    if menu == 'r':
        reg_user()

    elif menu == 'a':
        add_task()

    elif menu == 'va':
        view_all()

    elif menu == 'vm':
        view_mine()
        edit = input("Input C to mark the task as complete or E to edit the task: ")
        if edit.upper() == "E":
            edit_task()
        elif edit.upper() == "C":
            mark_task_complete()

    elif curr_user == 'admin':
        if menu == 'ds':
            display_statistics()

        elif menu == 'gr':
            generate_reports()

    elif menu == 'e':
        print('Goodbye!!!')
        exit()

    else:
        print("You have made a wrong choice. Please try again.")