import json
import datetime
import os

# Clear terminal function
def clear_terminal():
    os.system("cls" if os.name == "nt" else "clear")

# Add food function
def add_food(food, calories, protein):
    data = load_data()

    food = {"food": food, "calories": calories, "protein": protein}
    data.append(food)

    save_data(data)
    print("Food added successfully.")

# Remove food function
def remove_food(food):
    data = load_data()

    found = False
    for item in data:
        if item["food"] == food:
            data.remove(item)
            found = True
            break

    if found:
        save_data(data)
        print("Food '{}' removed successfully.".format(food))
    else:
        print("Food '{}' does not exist.".format(food))

# Daily total function
def daily_total():
    data = load_data()

    total_calories = sum(food["calories"] for food in data)
    total_protein = sum(food["protein"] for food in data)

    return total_calories, total_protein

# Reset data function
def reset_data():
    confirm = input("Are you sure you want to reset Data? (y/n): ")
    if confirm.lower() == "y":
        data = []
        save_data(data)
        print("Data reset successfully.")
    else:
        print("Reset cancelled.")

# Stored Data (json file)
def load_data():
    try:
        with open("tracker_data.json", "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        data = []

    return data

def save_data(data):
    with open("tracker_data.json", "w") as file:
        json.dump(data, file)

# Daily total function
def daily_food_report():
    data = load_data()

    if not data:
        print("Report not avaliable. (Please add some foods)")
        return

    today = datetime.datetime.now().date()

    print("Daily Food Report ({})\n".format(today))
    print("{:<20} {:<10} {:<10}".format("Food", "Calories", "Protein"))
    print("-" * 40)
    for food in data:
        print("{:<20} {:<10} {:<10}".format(food["food"], food["calories"], food["protein"]))

# Weekly total function
def weekly_total():
    data = load_data()

    if not data:
        print("Report not available. (Please add some foods)")
        return

    week_start = datetime.datetime.now().date() - datetime.timedelta(days=datetime.datetime.now().date().weekday())
    week_end = week_start + datetime.timedelta(days=6)

    total_calories = 0
    total_protein = 0

    print("Weekly Total ({} - {})\n".format(week_start, week_end))
    print("{:<20} {:<10} {:<10}".format("Food", "Calories", "Protein"))
    print("-" * 40)
    for food in data:
        print("{:<20} {:<10} {:<10}".format(food["food"], food["calories"], food["protein"]))
        total_calories += food["calories"]
        total_protein += food["protein"]

    print("-" * 40)
    print("{:<20} {:<10} {:<10}".format("Total", total_calories, total_protein))



# Test 1 (Adding food)
def test_add_food():
    add_food("Beef", 165, 31)
    add_food("Fish", 206, 22)

    data = load_data()
    assert len(data) == 2
    assert data[0]["food"] == "Beef"
    assert data[0]["calories"] == 165
    assert data[0]["protein"] == 31
    assert data[1]["food"] == "Fish"
    assert data[1]["calories"] == 206
    assert data[1]["protein"] == 22

    print("Test: Adding Food - PASSED")

#(Removing food)
def test_remove_food():
    add_food("Beef", 165, 31)
    add_food("Fish", 206, 22)

    remove_food("Fish")
    data = load_data()
    assert len(data) == 2
    assert data[0]["food"] == "Beef"
    assert data[0]["calories"] == 165
    assert data[0]["protein"] == 31

    remove_food("Tofu")
    data = load_data()
    assert len(data) == 2

    print("Test: Removing Food - PASSED")

# Test 2 (Daily Total)
def test_daily_total():
    add_food("Beef", 165, 31)
    add_food("Fish", 206, 22)
    add_food("Eggs", 78, 6)

    total_calories, total_protein = daily_total()
    assert total_calories == 449
    assert total_protein == 59

# (After adding food)
    add_food("Tofu", 94, 10)
    total_calories, total_protein = daily_total()
    assert total_calories == 543
    assert total_protein == 69

# (After removing food)
    remove_food("Beef")
    total_calories, total_protein = daily_total()
    assert total_calories == 378
    assert total_protein == 28

    print("Test: Daily Total - PASSED")

# Start Application (Home Page)
def run_tracker():
    while True:
        clear_terminal()
        print("--- Protein and Calorie Data ---")
        print("1. Add Food")
        print("2. Remove Food")
        print("3. Daily Total")
        print("4. Weekly Total")
        print("5. Reset Data")
        print("6. Exit")

        choice = input("Enter your choice: ")
        # Add food
        if choice == "1":
            clear_terminal()
            food = input("Enter the food: ")
            try:
                calories = int(input("Enter the calorie amount: "))
                protein = int(input("Enter the protein amount: "))
                add_food(food, calories, protein)
            except ValueError:
                print("--- Enter numbers only ---")
            input("Press Enter to continue...")
        # Remove food
        elif choice == "2":
            clear_terminal()
            food = input("Enter the food to remove: ")
            remove_food(food)
            input("Press Enter to continue...")
        # Daily Total
        elif choice == "3":
            clear_terminal()
            daily_food_report()
            total_calories, total_protein = daily_total()
            print("Total Calories: {}".format(total_calories))
            print("Total Protein: {}".format(total_protein))
            input("Press Enter to continue...")
        # Weekly total
        elif choice == "4":
            clear_terminal()
            weekly_total()
            input("Press Enter to continue...")
        # Reset data
        elif choice == "5":
            clear_terminal()
            reset_data()
            input("Press Enter to continue...")
        # Exit
        elif choice == "6":
            clear_terminal()
            print("--- Tracker exited. ---")
            print("Have a nice day! :)")
            break

# Run the application
run_tracker()
