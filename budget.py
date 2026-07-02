import math
from decimal import Decimal
class Category:

    def __init__(self, name):
        self.name = name
        self.ledger = []

    def __str__(self):
        text = self.name.center(30, "*")
        total = f"{self.get_balance():.2f}"
        for entry in self.ledger:
            amount = entry['amount']
            desc = entry['description'][:23]
            text += f"\n{desc:<23}{amount:>7.2f}"
        return text + "\n" + "Total: " + total
    
    def check_funds(self, amount):
        return amount <= self.get_balance()
    
    def get_balance(self):
        total = 0
        for item in self.ledger:
            total += item["amount"]
        return total
    
    def deposit(self, amount, description=""):
        self.ledger.append({'amount': round(amount, 2), 'description': description})

    def withdraw(self, amount, description=""):
        if self.check_funds(amount):
            self.ledger.append({'amount': -round(amount, 2), 'description': description})
            return True
        else:
            return False

    def transfer(self, amount, category):
        if self.check_funds(amount):
            self.withdraw(amount, "Transfer to " + category.name)
            category.deposit(amount, "Transfer from " + self.name)
            return True
        else:
            return False

def create_spend_chart(categories):
    chartText = "Percentage spent by category"
    spending = []
    percents = []
    totalSpending = 0
    #calculate total spending and spending per category
    for category in categories:
        categorySpending = 0
        for entry in category.ledger:
            amount = round(entry['amount'], 2)
            if amount < 0:
                categorySpending += abs(amount)
        spending.append((category.name, categorySpending))
        totalSpending += categorySpending
    #calculate spending percentages
    #prevent divide by 0 error
    if totalSpending > 0:
        for i in spending:
            categoryPercent = math.floor(((i[1] / totalSpending) * 100) / 10) * 10
            percents.append((i[0], categoryPercent))
        #y-axis
        for n in range(100, -10, -10):
            chartText += "\n" + str(n).rjust(3) + "| "
            for j in percents:
                if n <= j[1]:
                    chartText += "o  "
                else:
                    chartText += "   "
        #x-axis
        dash = "-"
        dashes = "-" * (len(categories) * 3 + 1)
        chartText += "\n    " + dashes 
        #x-axis labels
        max_length = max(len(category[0]) for category in percents)
        for o in range(max_length):
            chartText += "\n     "
            for category in categories:
                if o < len(category.name):
                    chartText += category.name[o] + "  "
                else:
                    chartText += "   "
        return chartText


def main():
    food = Category('Food')
    clothing = Category('Clothing')
    auto = Category('Auto')
    books = Category('Books')
    food.deposit(1000)
    clothing.deposit(400)
    auto.deposit(1000)
    books.deposit(400)
    food.withdraw(100)
    auto.withdraw(100)
    books.withdraw(100)
    clothing.withdraw(100)

    categories=[food, clothing, auto, books]
    create_spend_chart(categories)


if __name__ == '__main__':
    main()