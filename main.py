#Creating Habit class to represent individual habits:
import json
from datetime import datetime, timedelta

class Habit:
    def __init__(self, task, periodicity):
        self.task = task
        self.periodicity = periodicity
        self.checklist = []

    def is_completed(self):
        return len(self.checklist) >= self.periodicity

    def check_off(self):
        self.checklist.append(datetime.now().isoformat())

    def break_habit(self):
        self.checklist.clear()

    def get_longest_streak(self):
        longest_streak = 0
        current_streak = 0

        for i in range(len(self.checklist) - 1):
            date1 = datetime.fromisoformat(self.checklist[i])
            date2 = datetime.fromisoformat(self.checklist[i + 1])
            if (date2 - date1).days == 1:
                current_streak += 1
                longest_streak = max(longest_streak, current_streak)
            else:
                current_streak = 0

        return longest_streak



#Creating the HabitTracker class to manage multiple habits and implement the analytics module
class HabitTracker:
    def __init__(self):
        self.habits = []

    def add_habit(self, habit):
        self.habits.append(habit)

    def get_all_habits(self):
        return self.habits

    def get_habits_with_periodicity(self, periodicity):
        return [habit for habit in self.habits if habit.periodicity == periodicity]

    def get_longest_run_streak(self):
        longest_streak = 0

        for habit in self.habits:
            longest_streak = max(longest_streak, habit.get_longest_streak())

        return longest_streak

    def get_longest_run_streak_for_habit(self, habit_task):
        habit = next((h for h in self.habits if h.task == habit_task), None)
        if habit:
            return habit.get_longest_streak()
        return 0





#Creating a function to load example habit data and another function to persist the habit data
def load_example_habits():
    example_habits = [
        {"task": "Brush teeth", "periodicity": 1},
        {"task": "Workout", "periodicity": 7}
    ]

    habits = [Habit(habit["task"], habit["periodicity"]) for habit in example_habits]
    return habits

def save_habits_to_file(habits, filename):
    data = [{"task": habit.task, "periodicity": habit.periodicity, "checklist": habit.checklist} for habit in habits]
    with open(filename, "w") as file:
        json.dump(data, file)



#creating a function to load habit data from a file
def load_habits_from_file(filename):
    try:
        with open(filename, "r") as file:
            data = json.load(file)
            habits = [Habit(habit["task"], habit["periodicity"]) for habit in data]
            for habit, saved_habit in zip(habits, data):
                habit.checklist = saved_habit["checklist"]
            return habits
    except FileNotFoundError:
        return []


#creating a simple CLI to interact with the habit tracker
def main():
    habits_filename = "habits_data.json"
    habits = load_habits_from_file(habits_filename)

    if not habits:
        habits = load_example_habits()
        save_habits_to_file(habits, habits_filename)

    tracker = HabitTracker()
    for habit in habits:
        tracker.add_habit(habit)

    print("Welcome to the Habit Tracking App!")

    while True:
        print("\nMenu:")
        print("1. View all habits")
        print("2. View habits with a specific periodicity")
        print("3. View longest run streak")
        print("4. View longest run streak for a specific habit")
        print("0. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            for habit in tracker.get_all_habits():
                print(f"{habit.task} (Periodicity: {habit.periodicity})")
        elif choice == "2":
            periodicity = int(input("Enter the periodicity (1 for daily, 7 for weekly): "))
            habits_with_periodicity = tracker.get_habits_with_periodicity(periodicity)
            for habit in habits_with_periodicity:
                print(habit.task)
        elif choice == "3":
            print("Longest run streak:", tracker.get_longest_run_streak())
        elif choice == "4":
            habit_task = input("Enter the habit task: ")
            print(f"Longest run streak for {habit_task}:", tracker.get_longest_run_streak_for_habit(habit_task))
        elif choice == "0":
            save_habits_to_file(tracker.get_all_habits(), habits_filename)
            print("Exiting the Habit Tracking App. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
