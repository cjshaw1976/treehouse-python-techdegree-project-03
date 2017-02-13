import functions
import reports
import task

# Call the main function if run directly
if __name__ == '__main__':
    # Main lookup
    while True:
        # 1 Prompted with a menu to choose whether to add a new entry, lookup
        # previous entries or quit the program.
        menu_choice = functions.menu(
            "Main Menu:",
            "Record a new timesheet entry.",
            "Lookup previous timesheet entries.",
            "Exit the program."
        )

        if int(menu_choice) == 1:
            task.new()

        if int(menu_choice) == 2:
            # 3 Display 4 search options
            # Extra Credit date range
            menu_search = functions.menu(
                "Lookup previous timesheet entries:",
                "Find by date.",
                "Find by time spent.",
                "Find by exact search.",
                "Find by pattern.",
                "Find by date range.",
                "Return to main menu."
            )

            if int(menu_search) == 1:
                reports.find_by_date()

            if int(menu_search) == 2:
                reports.find_by_minutes()

            if int(menu_search) == 3:
                reports.find_by_exact()

            if int(menu_search) == 4:
                reports.find_by_regex()

            if int(menu_search) == 5:
                reports.find_by_date_range()

        if int(menu_choice) == 3:
            functions.clear_screen()
            break
