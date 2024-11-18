# Import necessary libraries for system operations, time handling, date management, holidays, requests, and notifications
import os
import time
from datetime import datetime, date, timedelta
import holidays
import requests
from plyer import notification
import platform

# Initialize an empty list to store tasks
tasks = []

# Define a dictionary to map country and region codes to their respective provinces/states
provinces_dict = {
    "AU": {
        "Australian Capital Territory": "ACT",
        "New South Wales": "NSW",
        "Northern Territory": "NT",
        "Queensland": "QLD",
        "South Australia": "SA",
        "Tasmania": "TAS",
        "Victoria": "VIC",
        "Western Australia": "WA"
    },
    "AT": {
        "Burgenland": "B",
        "Carinthia": "K",
        "Lower Austria": "N",
        "Upper Austria": "O",
        "Salzburg": "S",
        "Styria": "ST",
        "Tyrol": "T",
        "Vorarlberg": "V",
        "Vienna": "W"
    },
    "CA": {
        "Alberta": "AB",
        "British Columbia": "BC",
        "Manitoba": "MB",
        "New Brunswick": "NB",
        "Newfoundland and Labrador": "NL",
        "Nova Scotia": "NS",
        "Northwest Territories": "NT",
        "Nunavut": "NU",
        "Ontario": "ON",
        "Prince Edward Island": "PE",
        "Quebec": "QC",
        "Saskatchewan": "SK",
        "Yukon": "YU"
    },
    "FRA": {
        "Metropolitan France": "Métropole",
        "Alsace-Moselle": "Alsace-Moselle",
        "Guadeloupe": "Guadeloupe",
        "Guyane": "Guyane",
        "Martinique": "Martinique",
        "Mayotte": "Mayotte",
        "New Caledonia": "Nouvelle-Calédonie",
        "La Réunion": "La Réunion",
        "French Polynesia": "Polynésie Française",
        "Saint Barthélemy": "Saint-Barthélémy",
        "Saint Martin": "Saint-Martin",
        "Wallis and Futuna": "Wallis-et-Futuna"
    },
    "DE": {
        "Baden-Württemberg": "BW",
        "Bavaria": "BY",
        "Berlin": "BE",
        "Brandenburg": "BB",
        "Bremen": "HB",
        "Hamburg": "HH",
        "Hesse": "HE",
        "Mecklenburg-Vorpommern": "MV",
        "Lower Saxony": "NI",
        "North Rhine-Westphalia": "NW",
        "Rhineland-Palatinate": "RP",
        "Saarland": "SL",
        "Saxony": "SN",
        "Saxony-Anhalt": "ST",
        "Schleswig-Holstein": "SH",
        "Thuringia": "TH"
    },
    "NZ": {
        "Northland": "NTL",
        "Auckland": "AUK",
        "Taranaki": "TKI",
        "Hawke's Bay": "HKB",
        "Wellington": "WGN",
        "Marlborough": "MBH",
        "Nelson": "NSN",
        "Canterbury": "CAN",
        "South Canterbury": "STC",
        "West Coast": "WTL",
        "Southland": "STL",
        "Chatham Islands": "CIT"
    },
    "ES": {
        "Andalusia": "AND",
        "Aragon": "ARG",
        "Asturias": "AST",
        "Canary Islands": "CAN",
        "Cantabria": "CAM",
        "Castilla-La Mancha": "CAL",
        "Catalonia": "CAT",
        "Castilla y León": "CVA",
        "Extremadura": "EXT",
        "Galicia": "GAL",
        "Balearic Islands": "IBA",
        "Madrid": "ICA",
        "Madrid": "MAD",
        "Murcia": "MUR",
        "Navarre": "NAV",
        "Basque Country": "PVA",
        "La Rioja": "RIO"
    },
    "CH": {
        "Aargau": "AG",
        "Appenzell Ausserrhoden": "AR",
        "Appenzell Innerrhoden": "AI",
        "Basel-Landschaft": "BL",
        "Basel-Stadt": "BS",
        "Bern": "BE",
        "Fribourg": "FR",
        "Geneva": "GE",
        "Glarus": "GL",
        "Grisons": "GR",
        "Jura": "JU",
        "Lucerne": "LU",
        "Neuchâtel": "NE",
        "Nidwalden": "NW",
        "Obwalden": "OW",
        "St. Gallen": "SG",
        "Schaffhausen": "SH",
        "Schwyz": "SZ",
        "Solothurn": "SO",
        "Thurgau": "TG",
        "Ticino": "TI",
        "Uri": "UR",
        "Vaud": "VD",
        "Valais": "VS",
        "Zug": "ZG",
        "Zurich": "ZH"
    },
    "US": {
        "Alabama": "AL",
        "Alaska": "AK",
        "American Samoa": "AS",
        "Arizona": "AZ",
        "Arkansas": "AR",
        "California": "CA",
        "Colorado": "CO",
        "Connecticut": "CT",
        "Delaware": "DE",
        "District of Columbia": "DC",
        "Florida": "FL",
        "Georgia": "GA",
        "Guam": "GU",
        "Hawaii": "HI",
        "Idaho": "ID",
        "Illinois": "IL",
        "Indiana": "IN",
        "Iowa": "IA",
        "Kansas": "KS",
        "Kentucky": "KY",
        "Louisiana": "LA",
        "Maine": "ME",
        "Maryland": "MD",
        "Marshall Islands": "MH",
        "Massachusetts": "MA",
        "Michigan": "MI",
        "Federated States of Micronesia": "FM",
        "Minnesota": "MN",
        "Mississippi": "MS",
        "Missouri": "MO",
        "Montana": "MT",
        "Nebraska": "NE",
        "Nevada": "NV",
        "New Hampshire": "NH",
        "New Jersey": "NJ",
        "New Mexico": "NM",
        "New York": "NY",
        "North Carolina": "NC",
        "North Dakota": "ND",
        "Northern Mariana Islands": "MP",
        "Ohio": "OH",
        "Oklahoma": "OK",
        "Oregon": "OR",
        "Palau": "PW",
        "Pennsylvania": "PA",
        "Puerto Rico": "PR",
        "Rhode Island": "RI",
        "South Carolina": "SC",
        "South Dakota": "SD",
        "Tennessee": "TN",
        "Texas": "TX",
        "Utah": "UT",
        "Vermont": "VT",
        "Virginia": "VA",
        "Virgin Islands": "VI",
        "Washington": "WA",
        "West Virginia": "WV",
        "Wisconsin": "WI",
        "Wyoming": "WY"
    }
}

# Function to clear the terminal screen based on the operating system (Windows or Unix)
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')
clear()

# Read tasks from a file and check their due dates
def read():
    global tasks
    while True:
        try:
            with open("data.txt", "r") as file:
                tasks = file.readlines()
            row = 0
            for line in tasks:
                task = line[:55].strip()
                date = line[55:].strip()
                if datetime.now().date().strftime("%Y-%m-%d") == date:
                    tasks[row] = f"{task}{' ' * (55 - len(task))}     Today\n"
                elif (datetime.now() + timedelta(days=1)).date().strftime("%Y-%m-%d") == date:
                    tasks[row] = f"{task}{' ' * (55 - len(task))}  Tomorrow\n"
                row += 1
            break
        except:
            # Handle file-related errors and ask user to restore files if needed
            user_input = input("Error: A file cannot be found. Restore all missing files? (y/n): ")
            if user_input == "y":
                print("Restoring all missing files...")
                time.sleep(2)
                with open("data.txt", "x") as file:
                    file.write("")
                    clear()
                    read()
            elif user_input == "n":
                clear()
                print("Error: Application cannot proceed without a required file.")
                quit()
            else:
                clear()
                print("Invalid input, please try again.")
read()

# Notify user about a task for today
def notifications():
    try:
        if platform.system() == "Windows":
            # Open the task data file and read lines
            with open("data.txt", "r") as file:
                tasks = file.readlines()
            row = 0
            # Process each task
            for line in tasks:
                task = line[:55].strip()
                date = line[55:].strip()
                # Check if the task is due today
                if datetime.now().date().strftime("%Y-%m-%d") == date:
                    notification.notify(title='To Do', message=f"{task} - My Day")
                row += 1
        elif platform.system() == "Darwin":
            # Open the task data file and read lines
            with open("data.txt", "r") as file:
                tasks = file.readlines()
            row = 0
            # Process each task
            for line in tasks:
                task = line[:55].strip()
                date = line[55:].strip()
                # Check if the task is due today
                if datetime.now().date().strftime("%Y-%m-%d") == date:
                    command = f'''
                    osascript -e 'display notification "{task} - My Day" with title "To Do"'
                    '''
                    os.system(command)
                row += 1
        elif platform.system() == "Linux":
            # Open the task data file and read lines
            with open("data.txt", "r") as file:
                    asks = file.readlines()
            row = 0
            # Process each task
            for line in tasks:
                task = line[:55].strip()
                date = line[55:].strip()
                # Check if the task is due today
                if datetime.now().date().strftime("%Y-%m-%d") == date:
                    command = f'''
                    notify-send "To Do" "{task} - My Day"
                    '''
                    os.system(command)
                row += 1
        else:
            pass
    except:
        pass
notifications()

# Sort the tasks by their due dates
def sort():
    with open("data.txt", "r") as file:
        lines = file.readlines()
    sort_list = []
    # Parse each line into task and date tuples
    for line in lines:
        task = line[:55].strip()
        date = line[55:].strip()
        sort_list.append((task, date))
    # Sort tasks by date
    sort_list.sort(key=lambda x: datetime.strptime(x[1], "%Y-%m-%d"))
    # Write sorted tasks back to the file
    with open("data.txt", "w") as file:
        for task, date in sort_list:
            file.write(f"{task:<55}{date}\n")

# Write a new task to the file
def write(new_task, new_date):
    with open('data.txt', 'a') as file:
        file.write(f"{new_task}{' ' * (55 - len(new_task))}{new_date}\n")
    sort()  # Re-sort tasks after adding a new one
    read()  # Re-read tasks to update the task list

# Function to check if any holidays exist for the user's region and add them to the tasks
def check_holiday():
    try:
        # Get the user's country and region from an external IP service
        response = requests.get('https://ipinfo.io')
        data = response.json()
        country = data.get('country', 'Unknown')
        state = data.get('region', 'Unknown')
    except:
        # Handle failure to fetch holiday information due to lack of internet
        print("Error: No internet, holiday calendar is unavailible.")
        time.sleep(2)
        clear()
        user_interaction()
    with open('data.txt') as file:
        lines = [line.rstrip() for line in file]
        try:
            province = provinces_dict[country].get(state)  # Get region code
            # Fetch holidays for the region and check if they are already in the task list
            for date, name in sorted(holidays.country_holidays(country, subdiv=province, years=(datetime.now().year)).items()):
                holiday_check = f"{name}{' ' * (55 - len(name))}{date}"
                if holiday_check not in lines:
                    if datetime.date(datetime.now()) <= date:
                        write(name, date)
                        read()
        except:
            # Handle errors when holiday data is unavailable
            print("Error: Holiday calendar is unavailible in this region.")
            time.sleep(2)
            clear()
            pass
check_holiday()

# Function to print all the tasks to the terminal
def print_tasks():
    clear()
    print("Tasks")
    if tasks != []:
        # Loop through all tasks and print them
        n = 0
        while n < len(tasks):
            print(f"{n+1}.",tasks[n], end="")
            n += 1
    else:
        print("No new tasks")

# Function to add a new task
def add_a_task():
    print_tasks()
    print("\n")
    while True:
        new_task = input("Add a task (50 characters max): ")
        # Validate task length
        if len(new_task) > 50:
            print_tasks()
            print("\nThe input is more than 50 characters, please try again.")
        else:
            break
    print("")
    while True:
        date_format = input("Add due date (yyyy-mm-dd): ")
        try:
            # Validate the date input
            date_remove_time = date(int(date_format.split('-')[0]), int(date_format.split('-')[1]), int(date_format.split('-')[2]))
            if datetime.date(datetime.now()) <= date_remove_time:
                break
            else:
                print_tasks()
                print(f"\n\nAdd a task (50 characters max): {new_task}\nInvalid input, please try again.")
        except:
            print_tasks()
            print(f"\n\nAdd a task (50 characters max): {new_task}\nInvalid input, please try again.")
    new_date = str(date_remove_time).split(" ")[0]
    write(new_task, new_date)  # Write new task to the file
    if datetime.now().date().strftime("%Y-%m-%d") == new_date:
        notifications()
    clear()
    user_interaction()  # Return to user interaction menu

# Function to remove a task based on its index
def remove_a_task():
    numbers = '/'.join(map(str, range(1, len(tasks) + 1)))
    if numbers != "":
        new_task = input(f"Remove a task ({numbers}): ")
        # Validate input to ensure it is within the range of tasks
        if new_task.isdigit() == True and int(new_task) in range(1, len(tasks) + 1):
            with open('data.txt', 'r') as file:
                lines = file.readlines()
            with open('data.txt', 'w') as file:
                for i, line in enumerate(lines):
                    if i != int(new_task) - 1:
                        file.write(line)
            read()
            clear()
            user_interaction()
        else:
            print_tasks()
            print("\nInvalid input, please try again.")
            remove_a_task()
    else:
        print_tasks()
        print("\nThere are no tasks to remove.")
        pass
# Main function to interact with the user and provide task management options
def user_interaction():
    print_tasks()
    print("\n")
    while True:
        user_input = input("a. Add a task\nb. Remove a task\nEnter a choice (a/b): ")
        if user_input == "a":
            add_a_task()  # Option to add a task
        elif user_input == "b":
            print_tasks()
            print("\n")
            remove_a_task()  # Option to remove a task
        else:
            print_tasks()
            print("\nInvalid input, please try again.")
# Start the user interaction
user_interaction()