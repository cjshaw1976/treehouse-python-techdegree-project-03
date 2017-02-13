import constants
import csv
import datetime
import functions
import os
import re

from collections import OrderedDict


def new():
    """Adds a new entry to the timesheet"""
    # 2 Provide a task name, number of minutes spent, additional notes.
    message = ""
    while True:
        # Task Name
        functions.header_line("Add new task.")
        functions.display_message(message)
        name = input("Enter the task name: ")
        if name.strip() == "":
            message = "Task name cannot be empty."
            continue
        break

    message = ""
    while True:
        # Task time
        functions.header_line("Add new task ({}).".format(name))
        functions.display_message(message)
        minutes = input("Enter the number minutes the task {} took: "
                        .format(name))
        if minutes.strip() == "" or not minutes.isnumeric():
            message = "Minutes must be a number."
            continue
        break

    # Task optional notes
    functions.header_line("Add new task ({}).".format(name))
    notes = input("Enter any addition notes for the task {}: "
                  .format(name))

    # Confirm screen
    message = ""
    while True:
        functions.header_line("Add new task - Confirmation.")

        # Current date
        date = datetime.date.today()

        # Display entered options
        print("Date: {}".format(date))
        print("Name: {}".format(name))
        print("Minutes Taken: {}".format(minutes))
        print("Additional Notes: {}\n".format(notes))
        functions.display_message(message)
        confirm = input("Confirm the above task is correct to save Y/N: ")
        if confirm.strip().lower() not in ("yn"):
            message = "Invalid seclection. Try again."
            continue
        break

    if confirm.strip().lower() == "y":
        save_entry(date, name, minutes, notes)


def save_entry(date, name, minutes, notes):
    # Check if file exists
    file_exists = os.path.isfile(constants.FILE_NAME)
    with open(constants.FILE_NAME, 'a') as csvfile:
        taskwriter = csv.DictWriter(csvfile, fieldnames=constants.FILE_HEADER)

        # Write headline if a new file
        if not file_exists:
            taskwriter.writeheader()

        # Write entry
        taskwriter.writerow({
            'date': date,
            'name': name,
            'minutes': minutes,
            'notes': notes
        })


# Delete a matching line
def delete_entry(delete_data):
    # get file contents into memory
    data = entry_reader()

    # delete file
    os.remove(constants.FILE_NAME)

    # save entry except delete line
    for entry in data:
        if entry != delete_data:
            save_entry(entry['date'],
                       entry['name'],
                       entry['minutes'],
                       entry['notes'])


# Read a csv file
def entry_reader():
    with open(constants.FILE_NAME, newline="") as csvfile:
        taskreader = csv.DictReader(csvfile, constants.FILE_HEADER)
        return list(taskreader)[1:]


# Edit an existing task
def edit_entry(data):
    """Edits an existing entry in the timesheet"""

    # Task date
    message = ""
    while True:
        functions.header_line("Edit existing task: {}.".format(data['name']))
        functions.display_message(message)
        print("Enter the task date in the format YYYY-MM-DD.")
        date = input("Leave blank for current ({}): "
                     .format(data['date'])).strip()
        if date == "":
            date = data['date']
            break
        elif (not re.match(r'\d{4}-\d{2}-\d{2}', date) or
              int(date[5:7]) > 12 or int(date[8:10]) > 31):
            message = ("Invalid date {}. Date must be in the format "
                       "YYYY-MM-DD.".format(date))
            continue
        break

    # Task Name
    functions.header_line("Edit existing task: {}.".format(data['name']))
    functions.display_message(message)
    print("Enter a new task name.")
    name = input("Leave blank for current ({}): ".format(data['name']))
    if name.strip() == "":
        name = data['name']

    message = ""
    while True:
        # Task time
        functions.header_line("Edit existing task: {}.".format(data['name']))
        functions.display_message(message)
        print("Enter a new task time in minutes.")
        minutes = (input("Leave blank for current ({}): "
                         .format(data['minutes'])))
        if minutes.strip() == "":
            minutes = data['minutes']
            break
        elif not minutes.isnumeric():
            message = "Minutes must be a number."
            continue
        break

    # Task optional notes
    functions.header_line("Edit existing task: {}.".format(data['name']))
    print("Enter any addition notes.")
    print("Current: {}".format(data['notes']))
    notes = input("Leave blank for current: ")
    if notes.strip() == "":
        notes = data['notes']

    # Confirm screen
    message = ""
    while True:
        functions.header_line("Edit existing task - Confirmation.")

        # Display entered options
        print("New Date: {}".format(date))
        print("Old Date: {}\n".format(data['date']))
        print("New Name: {}".format(name))
        print("Old Name: {}\n".format(data['name']))
        print("New Minutes Taken: {}".format(minutes))
        print("Old Minutes Taken: {}\n".format(data['minutes']))
        print("New Additional Notes: {}".format(notes))
        print("Old Additional Notes: {}\n".format(data['notes']))
        functions.display_message(message)
        confirm = input("Confirm to update with the new task Y/N: ")
        if confirm.strip().lower() not in ("yn"):
            message = "Invalid seclection. Try again."
            continue
        break

    if confirm.strip().lower() == "y":
        delete_entry(OrderedDict([('date', data['date']),
                                  ('name', data['name']),
                                  ('minutes', data['minutes']),
                                  ('notes', data['notes'])]))
        save_entry(date, name, minutes, notes)
