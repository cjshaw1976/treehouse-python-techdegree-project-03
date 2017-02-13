# Clears the screen
def clear_screen():
    print("\033c", end="")


# Clears the screen and displays the headline
def header_line(text):
    clear_screen()
    print(text)
    print("=" * len(text) + "\n")


# Displays message if exists
def display_message(message):
    if message.strip() != "":
        print(message + "\n")


# Display a user menu
def menu(title, *args):
    message = ""
    while True:
        # Clear screen
        header_line(title)

        # Display menu options
        item = 1
        for arg in args:
            print("{}. {}".format(item, arg))
            item += 1

        print("")

        # Display any messages
        display_message(message)

        # Display input line
        menu_select = input("1-{} : ".format(str(item - 1)))

        # Check the enty is numeric and in the correct range provided
        if (not menu_select.isnumeric() or
                int(menu_select) not in range(1, item)):
            message = ("Sorry, your entry was not valid. Please select from "
                       "options provided.")
            continue

        return menu_select
