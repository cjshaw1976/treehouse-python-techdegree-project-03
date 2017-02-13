import datetime
import functions
import re
import task


def find_by_date():
    # Get data from csv file
    data = task.entry_reader()

    # Use a set to get unique dates
    # Convert to list for indexing
    date_list = list(set(val['date'] for val in data))
    date_list.sort()
    menu_dates = functions.menu(
        "Select a date to view timesheets",
        "Return to main menu.",
        *date_list
    )
    if int(menu_dates) != 1:
        # Create a list of only data that matches
        sample_list = list(val for val in data
                           if val['date'] == date_list[int(menu_dates) - 2])
        display_tasks(sample_list)


def find_by_minutes():
    # Get data from csv file
    data = task.entry_reader()

    message = ""
    while True:
        functions.header_line("Lookup tasks by time spent.")
        functions.display_message(message)

        minutes = input("Enter the number minutes to match: ")
        if minutes.strip() == "" or not minutes.isnumeric():
            message = "Minutes must be a number."
            continue
        break

    # Create a list of only data that matches
    sample_list = list(val for val in data
                       if int(val['minutes']) == int(minutes))
    if len(sample_list) > 0:
        display_tasks(sample_list)
    else:
        print("\nThere are no tasks that took {} minutes.".format(minutes))
        input("Press Enter to continue.")


def find_by_exact():
    # Get data from csv file
    data = task.entry_reader()

    message = ""
    while True:
        functions.header_line("Lookup tasks by exact phrase.")
        functions.display_message(message)

        phrase = input("Enter the phrase to search for: ").strip()
        if phrase == "":
            message = "Phrase cannot be empty."
            continue
        break

    # Create a list of only data that matches
    sample_list = list(val for val in data
                       if phrase in val['name'] or
                       phrase in val['notes'])
    if len(sample_list) > 0:
        display_tasks(sample_list)
    else:
        print("\nThere are no tasks that contain the phrase: '{}'."
              .format(phrase))
        input("Press Enter to continue.")


def find_by_regex():
    # Get data from csv file
    data = task.entry_reader()

    message = ""
    while True:
        functions.header_line("Lookup tasks by regex pattern.")
        functions.display_message(message)

        pattern = input("Enter the pattern to search for: ").strip()
        if pattern == "":
            message = "Pattern cannot be empty."
            continue
        break

    # Create a list of only data that matches
    sample_list = list(val for val in data
                       if re.findall(r'{}'.format(pattern), val['name']) or
                       re.findall(r'{}'.format(pattern), val['notes']))
    if len(sample_list) > 0:
        display_tasks(sample_list)
    else:
        print("\nThere are no tasks found that match the regex pattern: '{}'."
              .format(phrase))
        input("Press Enter to continue.")


def find_by_date_range():
    # Get data from csv file
    data = task.entry_reader()

    message = ""
    while True:
        functions.header_line("Lookup tasks by date range.")
        functions.display_message(message)

        print("Enter the start date  in the format YYYY-MM-DD.")
        start_date = input("Leave blank for today: ").strip()
        if start_date == "":
            start_date = datetime.date.today().strftime('%Y-%m-%d')
        elif (not re.match(r'\d{4}-\d{2}-\d{2}', start_date) or
              int(start_date[5:7]) > 12 or int(start_date[8:10]) > 31):
            message = ("Invalid date {}. Date must be in the format "
                       "YYYY-MM-DD.".format(start_date))
            continue
        break

    while True:
        functions.header_line("Lookup tasks by date range.")
        functions.display_message(message)

        print("Enter the end date  in the format YYYY-MM-DD.")
        end_date = input("Leave blank for today: ").strip()
        if end_date == "":
            end_date = datetime.date.today().strftime('%Y-%m-%d')
        elif (not re.match(r'\d{4}-\d{2}-\d{2}', end_date) or
              int(end_date[5:7]) > 12 or int(end_date[8:10]) > 31):
            message = ("Invalid date {}. Date must be in the format "
                       "YYYY-MM-DD.".format(end_date))
            continue

        if (datetime.datetime.strptime(end_date, "%Y-%m-%d").date() <
                datetime.datetime.strptime(start_date, "%Y-%m-%d").date()):
            message = ("End date ({}) cannot be before start date ({})."
                       .format(end_date, start_date))
            continue
        break

    # Create a list of only data that matches
    sample_list = list(val for val in data
                       if val['date'] >= start_date and
                       val['date'] <= end_date)
    if len(sample_list) > 0:
        display_tasks(sample_list)
    else:
        print("\nThere are no tasks found in the period from {} to {}."
              .format(start_date, end_date))
        input("Press Enter to continue.")


def display_tasks(data):
    task_position = 0
    error = ""

    while True:
        # Display task info
        functions.header_line("Displaying task {} of {}."
                              .format(task_position + 1, len(data)))
        print("Date: {}".format(data[task_position]['date']))
        print("Title: {}".format(data[task_position]['name']))
        print("Minutes Spent: {}".format(data[task_position]['minutes']))
        print("Additional Notes: {}\n".format(data[task_position]['notes']))

        # Display options
        if task_position != 0:
            print("P: Previous task.")
        if task_position < len(data) - 1:
            print("N: Next Task.")
        print("D: Delete Task.")
        print("E: Edit Task.")
        print("Q: Return to Main Menu.\n")

        # Display error message
        functions.display_message(error)

        # Get user choice
        select = input("Select an option: ").lower()
        if select not in ('pndeq'):
            error = "Invalid option. Please select from options provided."
            continue

        # Exit menu
        if select == "q":
            break

        # Handle previous and next
        if select == "p" and task_position > 0:
            task_position -= 1
        if select == "n" and task_position < len(data) - 1:
            task_position += 1

        # Handle delete
        if select == "d":
            task.delete_entry(data[task_position])
            break

        # Handle editing
        if select == "e":
            task.edit_entry(data[task_position])
            break
