""" A data management programme that allows users to register,
add tasks, view tasks and generate reports on task progress. """

# Importing modules to handle file management and date operations.
import os
from datetime import datetime, date

# Standard format for storing and displaying dates.
DATETIME_STRING_FORMAT = "%Y-%m-%d"

# As per good practice we will define all functions at the top.
# This function registers new users. 
def reg_user():
    # Keep asking for a unique username until provided.
    while True:
        new_username = input("New Username: ")
        # Check if the new username already exists in the system.
        if new_username in username_password:
            print("Username already exists. Try again.")
        else:
            break
    
    new_password = input("New Password: ")
    confirm_password = input("Confirm Password: ")

    # Check if the new password and confirmed password are the same.
    if new_password == confirm_password:
        print("New user added")
        username_password[new_username] = new_password

        # Update the user.txt file with the new user data.
        with open("user.txt", "w", encoding="utf-8") as out_file:
            user_data = []
            for username, password in username_password.items():
                    user_data.append(f"{username};{password}")
            out_file.write("\n".join(user_data))

       
    else:
            print("Passwords do not match")

# This function allows a user to add a new task to task.txt file
def add_task():
    # Get task details from user.
    task_username = input("Name of person assigned to task: ")
    if task_username not in username_password:
        print("User does not exist. Please enter a valid username")
        return
    task_title = input("Title of Task: ")
    task_description = input("Description of Task: ")

    # Enusre date is entered in the correct format.
    while True:
            try:
                task_due_date = input("Due date of task (YYYY-MM-DD): ")
                due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
                break

            except ValueError:
                print("Invalid datetime format. Please use the format specified")

    current_date = date.today()
    # Store task data in a dictionary for easier handling.
    new_task = {
            "username": task_username,
            "title": task_title,
            "description": task_description,
            "due_date": due_date_time,
            "assigned_date": current_date,
            "completed": False
        }
    # Update the task list and write to file.
    task_list.append(new_task)
    with open("tasks.txt", "w", encoding="utf-8") as task_file:
            task_list_to_write = []
            for task in task_list:
                str_attrs = [
                    task['username'],
                    task['title'],
                    task['description'],
                    task['due_date'].strftime(DATETIME_STRING_FORMAT),
                    task['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                    "Yes" if task['completed'] else "No"
                ]
                task_list_to_write.append(";".join(str_attrs))
            task_file.write("\n".join(task_list_to_write))
    print("Task successfully added.")

# This function allows a user to view all tasks in the system.
def view_all():
     # Iterate through tasks and display all task details.
     for task in task_list:
            display = (
                f"Task: \t\t {task['title']}\n"
                f"Assigned to: \t {task['username']}\n"
                f"Date Assigned: \t {task['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
                f"Due Date: \t {task['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
                f"Task Description: \n {task['description']}\n"
            )

            print(display)

# This function allows a user to view and manage their own tasks.
def view_mine():
      # Store only tasks assigned to the current user.
      user_tasks = []
      for task in task_list:
        if task['username'] == current_user:
            user_tasks.append(task)

      # Display user tasks with numbering for selection.
      for index, task in enumerate(user_tasks, start=1):
            display = (
                    f"\nTask Number: \t {index}\n"
                    f"Task: \t\t {task['title']}\n"
                    f"Assigned to: \t {task['username']}\n"
                    f"Date Assigned: \t {task['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
                    f"Due Date: \t {task['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
                    f"Task Description: \n {task['description']}\n"
                )
            print(display)

      # If the user has no tasks, return to main menu.      
      if not user_tasks:
        print("You have no tasks.")
        return

# User may select to edit or mark a task as complete
      while True:
        try:
                task_choice = int(
                input(
                    "Enter task number to edit/complete "
                    "(-1 to return to main menu): "))
                
            
                if task_choice == -1:
                    return

                if 1 <= task_choice <= len(user_tasks):
                    selected_task = user_tasks[task_choice - 1]
                    break

                else:
                    print("Invalid task number.")
        except ValueError:
                print("Please follow instructions.")

      # Task action menu
      print("\nSelected Task:")
      print(f"Title: {selected_task['title']}")
      edit_choice = input("Enter 'c' to mark complete or"
            "'e' to edit task: ").lower()          
      
      # Mark task as complete
      if edit_choice == 'c':
            selected_task['completed'] = True
            print("Task complete.")

      # Edit task details (username and due date)
      elif edit_choice == 'e':
            if selected_task['completed']:
                print("Completed tasks cannot be edited.")
                return

        # Edit username
            while True:
                edited_username = input(
                    "Enter new username "
                    "(leave blank to keep current): "
                    )

                if edited_username == "":
                    break

                if edited_username not in username_password:
                    print("User does not exist. Try again.")
                    continue

                selected_task['username'] = edited_username
                break

        # Edit due date
            edited_due_date = input("Enter new due date (YYYY-MM-DD) or"
            "press Enter to keep current: ")

            if edited_due_date:

                try:
                    selected_task['due_date'] = datetime.strptime(
                    edited_due_date,
                    DATETIME_STRING_FORMAT
                 )

                except ValueError:
                    print("Invalid date format.")
                    return

            print("Task updated successfully.")

      else:
            print("Invalid option.")
            return
      
      # Write updates to file after editing or marking complete.
      with open("tasks.txt", "w", encoding="utf-8") as task_file:

            edit_task_list = []

            for task in task_list:

                str_attrs = [
                task['username'],
                task['title'],
                task['description'],
                task['due_date'].strftime(DATETIME_STRING_FORMAT),
                task['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                "Yes" if task['completed'] else "No"
                ]

                edit_task_list.append(";".join(str_attrs))

            task_file.write("\n".join(edit_task_list))

# This function generates reports and writes them to text files.
def generate_reports():

    # Count number of tasks and users for report generation.
    total_tasks = len(task_list)
    completed_tasks = 0
    incomplete_tasks = 0
    overdue_tasks = 0

    today = date.today()

    # Calculate completed, incomplete and overdue tasks.
    for task in task_list:

        if task['completed']:
            completed_tasks += 1

        else:
            incomplete_tasks += 1

            if task['due_date'].date() < today:
                overdue_tasks += 1

    # Calculate percentages for incomplete and overdue tasks.
    incomplete_percentage = (
        (incomplete_tasks / total_tasks) * 100
        if total_tasks > 0 else 0
    )
    overdue_percentage = (
        (overdue_tasks / total_tasks) * 100
        if total_tasks > 0 else 0
    )

    # Write task overview to file
    with open("task_overview.txt", "w", encoding="utf-8") as task_report:

        task_report.write("TASK OVERVIEW\n")
        task_report.write("-" * 40 + "\n")

        task_report.write(
            f"Total tasks: {total_tasks}\n"
        )

        task_report.write(
            f"Completed tasks: {completed_tasks}\n"
        )

        task_report.write(
            f"Incomplete tasks: {incomplete_tasks}\n"
        )

        task_report.write(
            f"Overdue tasks: {overdue_tasks}\n"
        )

        task_report.write(
            f"Percentage incomplete: "
            f"{incomplete_percentage:.2f}%\n"
        )

        task_report.write(
            f"Percentage overdue: "
            f"{overdue_percentage:.2f}%\n"
        )

    total_users = len(username_password)
    # Create user-specific statistics for report generation.
    with open("user_overview.txt", "w", encoding="utf-8") as user_report:

        user_report.write("USER OVERVIEW\n")
        user_report.write("-" * 40 + "\n")

        user_report.write(
            f"Total users: {total_users}\n"
        )

        user_report.write(
            f"Total tasks: {total_tasks}\n\n"
        )

        # Calculate user-specific statistics
        for username in username_password:

            user_task_total = 0
            completed = 0
            incomplete = 0
            overdue = 0

            for task in task_list:

                if task['username'] == username:

                    user_task_total += 1

                    if task['completed']:
                        completed += 1

                    else:
                        incomplete += 1

                        if task['due_date'].date() < today:
                            overdue += 1

            # Percentages
            user_task_percentage = (
                (user_task_total / total_tasks) * 100
                if total_tasks > 0 else 0
            )

            user_completed_percentage = (
                (completed / user_task_total) * 100
                if user_task_total > 0 else 0
            )

            user_incomplete_percentage = (
                (incomplete / user_task_total) * 100
                if user_task_total > 0 else 0
            )

            user_overdue_percentage = (
                (overdue / user_task_total) * 100
                if user_task_total > 0 else 0
            )

            # Write user stats
            user_report.write(
                f"Username: {username}\n"
            )

            user_report.write(
                f"Tasks assigned: {user_task_total}\n"
            )

            user_report.write(
                f"Percentage of total tasks: "
                f"{user_task_percentage:.2f}%\n"
            )

            user_report.write(
                f"Tasks completed: "
                f"{user_completed_percentage:.2f}%\n"
            )

            user_report.write(
                f"Tasks incomplete: "
                f"{user_incomplete_percentage:.2f}%\n"
            )

            user_report.write(
                f"Overdue incomplete tasks: "
                f"{user_overdue_percentage:.2f}%\n"
            )

            user_report.write("-" * 40 + "\n")

    print("Reports generated successfully.")    

# This function displays statistics from generated report files.
def display_statistics():
    # Check if user is admin before displaying statistics.
    if current_user != 'admin':
        print("You do not have permission to view statistics.")
        return

    # Generate reports if missing
    if (
        not os.path.exists("task_overview.txt")
        or
        not os.path.exists("user_overview.txt")
    ):
        generate_reports()

    print("\nTASK OVERVIEW")
    print("-" * 40)

    # Read and display task overview report.
    with open(
        "task_overview.txt",
        "r",
        encoding="utf-8"
    ) as task_report:

        print(task_report.read())

    print("\nUSER OVERVIEW")
    print("-" * 40)

    with open(
        "user_overview.txt",
        "r",
        encoding="utf-8"
    ) as user_report:

        print(user_report.read())

# This function exits the programme.
def exit_programme():
    print('Goodbye!!!')
    exit()



#==== MAIN PROGRAM STARTS HERE ====
# Check if tasks.txt file exists, if not create it.
if not os.path.exists("tasks.txt"):
    with open("tasks.txt", "w", encoding="utf-8") as default_file:
        pass
with open("tasks.txt", 'r', encoding="utf-8") as task_file:
    task_data = task_file.read().split("\n")
    # Remove any empty lines from task_data
    task_data = [task for task in task_data if task != ""]

task_list = []
# Convert task data into a list of dictionaries for easier handling.
for task in task_data:
    current_task = {}
    task_components = task.split(";")
    current_task['username'] = task_components[0]
    current_task['title'] = task_components[1]
    current_task['description'] = task_components[2]
    current_task['due_date'] = datetime.strptime(task_components[3], DATETIME_STRING_FORMAT)
    current_task['assigned_date'] = datetime.strptime(task_components[4], DATETIME_STRING_FORMAT)
    current_task['completed'] = task_components[5] == "Yes"

    task_list.append(current_task)


#==== LOGIN SECTION ====

# If no user.txt file, write one with a default account.
if not os.path.exists("user.txt"):
    with open("user.txt", "w", encoding="utf-8") as default_file:
        default_file.write("admin;password")

# Read in user_data
with open("user.txt", 'r', encoding="utf-8") as user_file:
    user_data = user_file.read().split("\n")

# Convert user data into a dictionary for easier handling during login.
username_password = {}
for user in user_data:
    username, password = user.split(';')
    username_password[username] = password

# Keep asking for login credentials until a valid login is achieved.
while True:
    print("LOGIN")
    current_user = input("Username: ")
    current_pass = input("Password: ")
    if current_user not in username_password:
        print("User does not exist")
        continue
    if username_password[current_user] != current_pass:
        print("Wrong password")
        continue
    print("Login Successful!")
    break

#==== MAIN MENU ====
while True:
    print()
    menu = input("Select one of the following Options below:\n"
                 "r - Registering a user\n"
                 "a - Adding a task\n"
                 "va - View all tasks\n"
                 "vm - View my task\n"
                 "gr - Generate reports\n"
                 "ds - Display statistics\n"
                 "e - Exit\n"
                 ": ").lower()

    # Call the appropriate function based on user menu choice.
    if menu == 'r':
        reg_user()
    elif menu == 'a':
        add_task()
    elif menu == 'va':
        view_all()
    elif menu == 'vm':
        view_mine()
    elif menu == 'gr':
        generate_reports()
    elif menu == 'ds':
        display_statistics()
    elif menu == 'e':
        exit_programme()
    else:
        print("Invalid option, please try again.")