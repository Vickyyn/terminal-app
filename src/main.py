# More packages in tasks.py
from tasks import *
from prettytable import PrettyTable

# Fun title
print("\n\n")
tprint("Task Tracker", font = 'modular')

# Create pickle file if it does not already exist (the first time program is run)
try:
    with open("tasks.pkl", "x") as file:
        pass 
except FileExistsError:
    pass 

while True:
    # Welcome /  Main Menu
    main_response = input("\nWelcome to Task Tracker! \nToday's date is "
        f"{datetime.datetime.now().date()} \n\nPlease select from options"
        " below: \n 1. View tasks \n 2. Add tasks \n 3. Edit tasks \n 4. "
        "Delete tasks \n 5. Complete tasks \n 6. Exit \n\n")

    # View and sort tasks
    if main_response.lower() in {"1", "v", "view"}:
        view_input = True
        while view_input: 
            # Unpickles data. If no data then prompt to add and exit
            task_list = read_pickle_msg_if_blank()
            if not task_list:
                break

            # Creates viewing table utilising PrettyTable
            table = PrettyTable()
            table.field_names = ["Name", "Time needed (minutes)", "Complete by"]
            for task in task_list:
                table.add_row([task.tname, task.tvalues[0], task.tvalues[1]])

            # Print table at entry page for convenience
            print(f"{table}\n\n")

            # View tasks via sorting by different variables
            sort_tasks(table)

            # Prompts user for next action they would like to take
            loop_page("sort")

    # Add tasks
    elif main_response.lower() in {"2", "a", "add"}:
        add_input = True
        while add_input:
            # Create task
            print("You are adding a new task!")
            named_task = Task()
            named_task.tname = input("What is the name of the task? ")

            # Ensure new task name is unique, and loop until so 
            # Unpickle data
            task_list = read_pickle()

            while True:
                i = 0
                for task in task_list:
                    i += 1
                    if named_task.tname.lower() == task.tname.lower():
                        named_task.edit_duplicate()
                        i = 0
                if i == len(task_list):
                    break

            # Set remaining attributes of task
            named_task.enter_tvalues(
                "Approximately how much time does it take to do the task? "
                    "Please input in HH:MM format. ",
                "When does the task need to be completed by? Please input in "
                    "DD/MM/YYYY format. ")

            # Update and pickle data
            task_list.append(named_task)
            write_pickle(task_list)

            # Confirm to user that task has been successfully created
            task_list[-1].print_confirmation("\nThe following task has been"
                " successfully added!")

            # Prompt user for next step
            add_input = loop_page("add")
            
    # Edit tasks
    elif main_response.lower() in {"3", "e", "edit"}:
        edit_input = True
        while edit_input:
            # Unpickles data. If no data then prompt to add and exit
            task_list = read_pickle_msg_if_blank()
            if not task_list:
                break

            edit_name = input("Please enter the name of the task you would "
                "like to edit: ")  
            # Check the name exists
            name_exists = False
            for i in task_list:
                if i.tname.lower() == edit_name.lower():
                    name_exists = True
                    # Show details of task to be edited, and edits task
                    i.print_confirmation("You are editing:")    
                    i.tname = input("What would you like the new name to be? "
                        "You can re-enter the same name. ")

                    # Check and loop until unique name
                    while True:
                        counter = 0
                        for task in task_list:
                            if i.tname.lower() == task.tname.lower():
                                counter += 1
                        if counter == 1:
                            break
                        if counter == 2:
                            i.edit_duplicate()

                    i.enter_tvalues("What is the new estimated time to complete the task? Please input in HH:MM format. ", 
                        "When is the new completion date? Please input in DD/MM/YYYY format. ")

                    # Confirms edited details and pickles data
                    i.print_confirmation("\nYou have edited to:")
                    write_pickle(task_list)
                    break
            if not name_exists:
                print("This task does not exist. Please try again. \n")

            # Prompt user for next step
            edit_input = loop_page("edit")
        
    # Delete tasks
    elif main_response.lower() in {"4", "d", "delete"}:
        delete_input = True
        while delete_input:
            # Unpickles data. If no data then prompt to add and exit 
            task_list = read_pickle_msg_if_blank()
            if not task_list:
                break

            delete_name = input("Please enter the name of the task you would "
                "like to delete: ")  
            # Check name exists
            name_exists = False
            for task in task_list:
                if task.tname.lower() == delete_name.lower():
                    name_exists = True
                    # Shows details of task 
                    task.print_confirmation("You are deleting:")
                    while delete_input != 'no':
                        try:
                            delete_input = input("Are you sure you want to "
                                "delete? ")
                            if delete_input.lower() in {"y", "yes"}:
                                # Delete task, print confirmation, pickles data
                                task_list.remove(task)
                                print("Deletion successful \n") 
                                write_pickle(task_list)   
                                delete_input = 'no'
                            elif delete_input.lower() in {"n", "no"}:
                                delete_input = 'no'
                            else:
                                raise ValueError("Please enter 'yes' or 'no'")
                        except ValueError as err:
                            print(err)
            if not name_exists:
                print("This task does not exist. Please try again. \n")

            # Prompt user for next step
            delete_input = loop_page("delete")

    # Complete tasks
    elif main_response.lower() in {"5", "c", "complete"}:
        complete_input = True
        while complete_input:
            # Unpickles data. If no data then prompt to add and exit 
            task_list = read_pickle_msg_if_blank()
            if not task_list:
                break

            # Complete task whilst checking the task exists
            complete_name = input("Please enter the name of the task you "
                "would like to complete: ")  
            name_exists = False          
            for task in task_list:
                if task.tname.lower() == complete_name.lower():
                    name_exists = True
                    # Confirm task to be completed
                    task.print_confirmation("You are completing:")
                    while complete_input != 'no':
                        complete_input = input("Is this the right task? ")
                        if complete_input.lower() in {"y", "yes"}:
                            # Complete task with bonus ASCII text art, remove task and pickle data
                            task.complete()
                            task_list.remove(task)
                            write_pickle(task_list)   
                            complete_input = 'no'
                        elif complete_input.lower() in {"n", "no"}:
                            complete_input = 'no'
                        else:
                            print("Please enter 'yes' or 'no' ")
            if not name_exists:
                print("This task does not exist. Please try again. \n")

            # Prompt user for next step
            complete_input = loop_page("complete")            

    # Quit option
    elif main_response.lower() in {"6", "exit", "quit"}:
        raise SystemExit

    else:
        input("NOTE: Please enter a number from 1 to 6. Press enter to continue. ")
