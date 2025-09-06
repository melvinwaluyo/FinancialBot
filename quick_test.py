from core.rules import FinancialRulesEngine

rules = FinancialRulesEngine()

# Test key functionality
print('Budget parsing tests:')
tests = ['Help me create a budget', 'bantuan budget saya', 'buatkan budget']
for test in tests:
    result = rules.parse_command(test)
    print(f'{test} -> {result.get("type")}')

print()
print('Purchase parsing tests:')
tests = ['I want to buy a car 30000000', 'saya mau beli laptop 15000000']
for test in tests:
    result = rules.parse_command(test)
    print(f'{test} -> {result.get("type")}, {result.get("item")}, {result.get("price")}')
