# Fixed exchange rate: 1 USD = 95.24 INR (hardcoded)
USD_TO_INR = 95.24

# Hardcoded list of expenses in INR
expenses_inr = [1500, 250.50, 9999, 45000, 799]

print("Expense Report (INR -> USD)")
print("-" * 40)

for expense in expenses_inr:
    usd = expense / USD_TO_INR
    print(f"INR {expense:>10.2f}  ->  USD {usd:>10.2f}")