# Notes: 
# 1. Use the following username and password to access the admin rights 
# username: admin
# password: password
# 2. Ensure you open the whole folder for this task in VS Code otherwise the 
# program will look in your root directory for the text files.

#=====importing libraries===========
import os
from datetime import datetime, date

DATETIME_STRING_FORMAT = "%Y-%m-%d"

def reg_User(new_username ,new_password, confirm_password,):

    # - Check if the user name is not used before for registration

    with open("user.txt","r") as users_file:
        users = users_file.read()
        users = users.replace("\n",";")
        list_users = users.split(";")  
        if new_username in list_users:
            print("There is already an existing user with this name!")
            return False

    # - Check if the new password and confirmed password are the same.

    if new_password == confirm_password:
        # - If they are the same, add them to the user.txt file

        print("New user added")
        username_password[new_username] = new_password
        
        with open("user.txt", "w") as out_file:
            user_data = []
            for k in username_password:
                user_data.append(f"{k};{username_password[k]}")
            out_file.write("\n".join(user_data))

    # - Otherwise you present a relevant message.
    else:
        print("Passwords do no match")
        return False


def add_task(task_username):
        
        '''Allow a user to add a new task to task.txt file
            Prompt a user for the following: 
             
             - A title of a task,
             - A description of the task and 
             - the due date of the task.'''
        
        task_title = input("Title of Task: ")
        task_description = input("Description of Task: ")
        while True:
            try:
                task_due_date = input("Due date of task (YYYY-MM-DD): ")
                due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
                break

            except ValueError:
                print("Invalid datetime format. Please use the format specified")
                return False
            
    # Then get the current date.
        curr_date = date.today()
        ''' Add the data to the file task.txt and
            Include 'No' to indicate if the task is complete.'''
        new_task = {
            "username": task_username,
            "title": task_title,
            "description": task_description,
            "due_date": due_date_time,
            "assigned_date": curr_date,
            "completed": False
        }

        task_list.append(new_task)
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
        print("Task successfully added.")


def view_all():
        
        '''Reads the task from task.txt file and prints to the console in the 
           format of Output 2 presented in the task pdf (i.e. includes spacing
           and labelling) 
        '''
        for t in task_list:
            disp_str = f"Task: \t\t {t['title']}\n"
            disp_str += f"Assigned to: \t {t['username']}\n"
            disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Task Description: \n {t['description']}\n"
            print(disp_str)


def view_mine():
        '''
        Prints all the tasks that are assigned to the current logged in user. It then prompts them
        to change details of a non completed task or return to the main menu. They can choose to change
        date, username the task is assigned to or the completion status of the task.  
        '''
        count = 0
        

        for t in task_list:
            if t['username'] == curr_user:
                count += 1
                disp_str = f"Task: \t\t {t['title']} number ({count})\n"
                disp_str += f"Assigned to: \t {t['username']}\n"
                disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
                disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
                disp_str += f"Task Description: \n {t['description']}\n"
                print(disp_str)
                print()

        # List of all tasks of the current logged in user
        user_task_list = [task for task in task_list if task['username'] == curr_user]
        range = len(user_task_list)

        # Asks the user to return to menu or choose a task
        while True:
            feedback = input("Please type number of specific task or return to main menu by pressing -1: ")
            # This is to avoid the user to press 0 for choosing the first task
            feedback = int(feedback) - 1
            if feedback == -2:
                break
            
            elif feedback >= 0 and feedback < range:
                # Unmodified task is saved separately so its position in the list can be found
                # and then replaced with new one later on without changing order of tasks list

                task = user_task_list[feedback]
                unmodified_task = task
                try:
                    choice = int(input("If you want to change completion status of the task, press 1 " \
                            "otherwise, if you want to edit the task, press 2: "))
                except ValueError:
                    print("You must type either 1 or 2: ")
                    continue
                
                if choice == 1:
                    # Change completion status of the task

                    print(f'Current status of the task: {task["completed"]}')
                    completion = input("Type 'yes' or 'no' if task is completed: ")
                    if completion.lower() == "yes":
                        task["completed"] = True
                        modify_file(unmodified_task,task,"tasks.txt")
                        break
                        
                    elif completion.lower() == "no":
                        task["completed"] = False
                        modify_file(unmodified_task,task,"tasks.txt")
                        break
                    else:
                        print("You did not type 'yes' or 'no'. ")
                        continue

                elif choice == 2 and not task["completed"]:
                    # Edit tasks' details unless task is completed

                    print(f"\n {task['username']}")
                    print(f"{task['due_date']}\n")
                    choice = input("Choose to change either the username by typing 1 or the date " \
                                "by typing 2: ")
                    if choice == "1":
                        # Change username the task is assigned to

                        new_username = input("Type the new username you want to assign the task to: ")
                        if new_username not in username_password.keys():
                            print("Username is not amongst registered users")
                            break
                        task["username"] = new_username
                        modify_file(unmodified_task,task,"tasks.txt")
                        print("Task assigned successfully!")
                        break

                    elif choice == "2":
                        # Change due date of the task
                        try:
                            new_date = input("Type the new date the task will be assigned for: ")
                            task["due_date"] = datetime.strptime(new_date, DATETIME_STRING_FORMAT)
                        except ValueError:
                            print("Not correct date format (YYYY-MM-DD) ")
                            break
                        modify_file(unmodified_task,task,"tasks.txt")
                        break
                    else:
                        print("You did not type 1 or 2")
                        continue
                elif choice == 2 and task["completed"]:
                    print("Task has already been completed. You cannot modify it.\n")

# Method used for generating and displaying task and user overviews files
def generate_reports(tasks):
    """
    It iterates through the tasks list that contain information of the tasks stored as dictionaries
    and counts number of completed, uncompleted, uncompleted and overdue tasks. It then writes them in
    a file called "task_overview.txt" and displays them.  
    """
    current_date = date.today()
    number_tasks = len(tasks)

    with open("task_overview.txt","w+") as task_overview:

        task_overview.write(f"Total number of tasks: {number_tasks}\n")

        task_count1 = 0
        task_count2 = 0
        task_count3 = 0
        task_count4 = 0

        for task in tasks:
            if task["completed"]:
                task_count1 += 1
            else:
                task_count2 += 1
            if not task["completed"] and current_date > task["due_date"].date():
                task_count3 += 1
            if current_date > task["due_date"].date():
                task_count4 += 1
        try:
            percentage_incomplete_tasks = round((task_count2/number_tasks),2)*100
            percentage_overdue_tasks = round((task_count4/number_tasks),2)*100

        except ZeroDivisionError:
            percentage_incomplete_tasks = 0
            percentage_overdue_tasks = 0

        task_overview.write(f"Total number of completed tasks are: {task_count1} \n"
            f"Total number of uncompleted tasks: {task_count2}\n"
            f"Total number of uncompleted and overdue tasks : {task_count3} \n"
            f"Percentage of tasks that are incomplete: {percentage_incomplete_tasks}% \n"
            f"Percentage of tasks that are overdue: {percentage_overdue_tasks}% \n")
        task_overview.seek(0)
        print(task_overview.read())

    # It iterates through all tasks and identifies which one is assigned to each user. It counts
    # number of total assigned, completed, uncompleted, uncompleted and overdue tasks for every user.
    # It writes them in a file called "user_overview.txt" and displays them.

    with open("user_overview.txt","w+") as user_overview:
        
        user_count1 = 0
        user_count2 = 0
        user_count3 = 0
        user_count4 = 0

        num_users = len(username_password.keys())
        user_overview.write(f"Total number of users: {num_users} \n"
                    f"Total number of tasks assigend: {number_tasks} \n\n" )
        user_overview.seek(0,2)

        for user in username_password.keys():
            for task in tasks:
                if user == task["username"]:
                    user_count1 += 1
                if user == task["username"] and task["completed"]:
                    user_count2 += 1
                elif user == task["username"] and not task["completed"]:
                    user_count3 += 1
                if user == task["username"] and not task["completed"] and current_date > task["due_date"].date():
                    user_count4 += 1
            # If there are no tasks, user_count1 is set to 1 to avoid zero division error. 
            # when that is the case, all other user_count will be zero regardless
            #   
            number_tasks_per_user = user_count1
            if user_count1 == 0:
                user_count1 = 1
            try:
                percentage_tasks_assigned = round((user_count1/number_tasks)*100,2)
            except ZeroDivisionError:
                percentage_tasks_assigned = 0
                
            user_overview.write(f"User {user} has {number_tasks_per_user} assigned tasks\n" 
                f" Percentage of tasks assigned to the user: {percentage_tasks_assigned}% \n"
                f" Percentage of tasks that are completed by the user: {round((user_count2/user_count1)*100,2)}%\n"
                f" Percentage of tasks that are not completed by the user: {round((user_count3/user_count1)*100,2)}%\n"
                f" Percentage of tasks that are not completed and are overdue by the user: {round((user_count4/user_count1)*100,2)}%\n\n")
            number_tasks_per_user = user_count1 = user_count2 = user_count3 = user_count4 = 0
        user_overview.seek(0)
        print(user_overview.read())

# Used to change the task.txt file whenever a change is made.
def modify_file(unmodified_task, modified_task, name_of_file):
    
    index_tasks_list = task_list.index(unmodified_task)
    task_list[index_tasks_list] = modified_task
    with open(name_of_file, "w") as task_file:
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
    print("File modified successfully!")


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


while True:
    # presenting the menu to the user and 
    # making sure that the user input is converted to lower case.
    print()
    menu = input('''Select one of the following Options below:
r - Registering a user
a - Adding a task
va - View all tasks
vm - View my task
gr - Generate reports
ds - Display statistics
e - Exit
: ''').lower()

    if menu == 'r':
        '''Add a new user to the user.txt file'''
            # - Request input of a new username
        new_username = input("New Username: ")

        # - Request input of a new password
        new_password = input("New Password: ")

        # - Request input of password confirmation.
        confirm_password = input("Confirm Password: ")
        reg_User(new_username, new_password, confirm_password)

    elif menu == 'a':

        '''Allow a user to add a new task to task.txt file
            Prompt a user for the following: 
             - A username of the person whom the task is assigned to,
             - A title of a task,
             - A description of the task and 
             - the due date of the task.'''
        
        task_username = input("Name of person assigned to task: ")
        if task_username not in username_password.keys():
            print("User does not exist. Please enter a valid username")
            continue
        
        add_task(task_username)

    elif menu == 'va':

        view_all()
            

    elif menu == 'vm':
       
       view_mine()
                
    elif menu == "gr":

        generate_reports(task_list)

    elif menu == 'ds' and curr_user == 'admin': 
        '''If the user is an admin they can display statistics about number of users
            and tasks.'''
        
        num_users = len(username_password.keys())
        num_tasks = len(task_list)

        print("-----------------------------------")
        print(f"Number of users: \t\t {num_users}")
        print(f"Number of tasks: \t\t {num_tasks}")
        print("-----------------------------------")    

    elif menu == 'e':
        print('Goodbye!!!')
        exit()

    else:
        print("You have made a wrong choice, Please Try again")