import constants
import csv
import datetime
import functions
import os
import re

from collections import OrderedDict


# Read a csv file
def entry_reader():
    with open(constants.FILE_NAME, newline="") as csvfile:
        taskreader = csv.DictReader(csvfile, constants.FILE_HEADER)
        return list(taskreader)[1:]


class Task():
    def edit(self, title, type="text", required=True, value=""):
        message = ""
        while True:
            functions.header_line(self.header_line)
            functions.display_message(message)
            if  value!="":
                print("Leave empty for current: {}".format(value))
            text = input("Enter the task {}: ".format(title))
            if text.strip() == "":
                if value != "":
                    text = value
                elif required is True:
                    message = "Task {} cannot be empty.".format(title)
                    continue
            if type == "number" and not text.isnumeric():
                message = "Task {} must be a number.".format(title)
                continue
            if (type == "date" and (not re.match(r'\d{4}-\d{2}-\d{2}', text) or
                                    int(text[5:7]) > 12 or
                                    int(text[8:10]) > 31)):
                message = ("Invalid date {}. Date must be in the format "
                           "YYYY-MM-DD.".format(text))
                continue
            return text

    def display(self):
        functions.header_line(self.header_line)
        print("Date: {}".format(self.date))
        print("Name: {}".format(self.name))
        print("Minutes Taken: {}".format(self.minutes))
        print("Additional Notes: {}\n".format(self.notes))

    def save_entry(self, *args):
        # Check if file exists
        file_exists = os.path.isfile(constants.FILE_NAME)
        with open(constants.FILE_NAME, 'a') as csvfile:
            taskwriter = csv.DictWriter(csvfile,
                                        fieldnames=constants.FILE_HEADER)

            # Write headline if a new file
            if not file_exists:
                taskwriter.writeheader()

            # Write entry
            if len(args) == 0:
                taskwriter.writerow({
                    'date': self.date, 'name': self.name,
                    'minutes': self.minutes, 'notes': self.notes
                })
            else:
                taskwriter.writerow({
                    'date': args[0], 'name': args[1],
                    'minutes': args[2], 'notes': args[3]
                })

    def __init__(self, **kwargs):
        if len(kwargs) == 0:
            self.new_entry()
        else:
            self.date = kwargs['date']
            self.name = kwargs['name']
            self.minutes = kwargs['minutes']
            self.notes = kwargs['notes']
            self.header_line = ""

    def new_entry(self):
        """Adds a new entry to the timesheet"""
        # 2 Provide a task name, number of minutes spent, additional notes.
        self.header_line = "Add new task."
        self.name = self.edit("name")
        self.minutes = self.edit("minutes", "number")
        self.notes = self.edit("notes", "text", False)
        self.date = datetime.date.today().strftime('%Y-%m-%d')

        # Confirm screen
        message = ""
        while True:
            self.display()
            functions.display_message(message)
            confirm = input("Confirm the above task is correct to save Y/N: ")
            if confirm.strip().lower() not in ("yn"):
                message = "Invalid seclection. Try again."
                continue
            break

        if confirm.strip().lower() == "y":
            self.save_entry()

    def delete_entry(self, data=""):
        if data == "":
            data = OrderedDict([('date', self.date),
                               ('name', self.name),
                               ('minutes', self.minutes),
                               ('notes', self.notes)])

        # get file contents into memory
        csv_data = entry_reader()

        # delete file
        os.remove(constants.FILE_NAME)

        # save entry except delete line
        for entry in csv_data:
            if entry != data:
                self.save_entry(entry['date'],
                                entry['name'],
                                entry['minutes'],
                                entry['notes'])

    def edit_entry(self):
        """Edits an existing entry in the timesheet"""
        old_entry = OrderedDict([('date', self.date),
                                ('name', self.name),
                                ('minutes', self.minutes),
                                ('notes', self.notes)])

        self.header_line = "Edit existing task: {}.".format(self.name)
        self.date = self.edit("date", "date", True, self.date)
        self.name = self.edit("name", "text", True, self.name)
        self.minutes = self.edit("minutes", "number", True, self.minutes)
        self.notes = self.edit("notes", "text", False, self.notes)

        # Confirm screen
        message = ""
        while True:
            self.display()
            functions.display_message(message)
            confirm = input("Confirm the above task is correct to save Y/N: ")
            if confirm.strip().lower() not in ("yn"):
                message = "Invalid seclection. Try again."
                continue
            break

        if confirm.strip().lower() == "y":
            self.delete_entry(old_entry)
            self.save_entry()
