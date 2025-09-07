import json
import os
import argparse


parser = argparse.ArgumentParser(description="Распределние финансов")
parser.add_argument(
    "--filepath",
    type=str,
    default="budget_data.json",
    help="Путь к JSON файлу с данными бюджета (по умолчанию budget_data.json)"
)
args = parser.parse_args()
date_file = args.filepath


inital_budget = float(input("""Добро пожаловать, здесь вы сможете отслеживать ваши финансы.
Пожалуйста введите имеющееся у вас кол-во денег: """))

budget = inital_budget
expenses = []
first_budget = inital_budget
total_added_money = 0


def load_budget_data(filepath):
    try:
        with open("filepath", "r", encoding="utf-8") as f:
            data = json.load(f)
            return data["first_budget"], data["initial_budget"], [
                {"expense_name": e["description"], "expense": e["amount"]}
                for e in data["expenses"]
            ]
    except FileNotFoundError:
        print("Файл с данными не обнаруженю. Начнём с пустого бюджета.")
        return None, None, []
    except json.JSONDecodeError:
        print("Ошибка чтения данных. Начнём с пустого бюджета.")
        return None, None, []


def add_expenses():
    global budget
    expense_name = input("Введите описание траты (на что вы потратили деньги?): ")
    expense_amount = float(input("Введите кол-во потраченных денег: "))

    if expense_amount > budget:
        print("Не можем добавить трату, кол-ва ваших денег не хватает, сначала укажите ваш точный бюджет")
        return None

    expense = {
        'expense_name': expense_name,
        'expense': expense_amount
    }
    expenses.append(expense)
    budget -= expense_amount
    print(f"Добавлена трата: {expense_name}, потрачено денег: {expense_amount}")
    return budget


def get_total_expenses(expenses_list):
    return sum(e['expense'] for e in expenses_list)


def show_budget_details(first_budget, budget, expenses):
    print(f"Изначально было денег: {first_budget}")
    print("Траты:")
    if expenses:
        for e in expenses:
            print(f"- {e['expense_name']}: {e['expense']};")
            total_spent = get_total_expenses(expenses)
        print(f"Всего потрачено: {total_spent}")
        print(f"Всего добавлено к бюджету: {total_added_money}")
    else:
        print("- нет трат")
    print(f"Текущий баланс: {budget}")


def update_budget(budget):
    try:
        added_money = float(input("Введите сумму, которую хотите добавить к бюджету: "))
        if added_money < 0:
            print("Нельзя добавлять отрицательную сумму.")
            return 0, budget
        budget += added_money
        print(f"Вы добавили {added_money}. Новый бюджет: {budget}")
        return added_money, budget
    except ValueError:
        print("Ошибка ввода. Введите число.")
        return 0, budget


def save_budget_details():
    data = {
        "first_budget": first_budget,
        "initial_budget": budget,
        "expenses": [
            {"description": e["expense_name"], "amount": e["expense"]}
            for e in expenses
        ],
        "total_added": total_added_money
    }
    with open(date_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)
    print(f"Данные бюджета сохранены в {date_file}")


while True:
    actions = int(input("""Чтобы вы хотели сделать?
    1. Добавить траты
    2. Показать кол-во оставшихся денег
    3. Обновить бюджет
    4. Выйти
    Ваш выбор (1-4): """))

    if actions == 1:
        add_expenses()
    elif actions == 2:
        show_budget_details(first_budget, budget, expenses)
    elif actions == 3:
        added_money, budget = update_budget(budget)
        total_added_money += added_money
    elif actions == 4:
        save_budget_details()
        print("Выход из программы.")
        break
    else:
        print("Неверный выбор!")