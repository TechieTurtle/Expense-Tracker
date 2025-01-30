import database

def main():
    while True:
        print("\nExpense Tracker")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Delete Expense")
        print("4. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            date = input("Enter date (YYYY-MM-DD): ")
            category = input("Enter category: ")
            amount = float(input("Enter amount: "))
            description = input("Enter description: ")
            database.add_expense(date, category, amount, description)
            print("Expense added successfully!")

        elif choice == "2":
            expenses = database.get_expenses()
            if not expenses:
                print("\nNo expenses recorded.")
            else:
                print("\nID | Date       | Category    | Amount | Description")
                print("-" * 50)
                for exp in expenses:
                    print(f"{exp[0]}  | {exp[1]} | {exp[2]} | ${exp[3]:.2f} | {exp[4]}")

        elif choice == "3":
            expense_id = int(input("Enter expense ID to delete: "))
            database.delete_expense(expense_id)
            print("Expense deleted successfully!")

        elif choice == "4":
            print("Exiting Expense Tracker...")
            break

        else:
            print("Invalid choice! Please enter a valid option.")

if __name__ == "__main__":
    main()
