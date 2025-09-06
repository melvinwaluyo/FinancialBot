from core.rules import FinancialRulesEngine

rules = FinancialRulesEngine()

print('=== Testing Pure Indonesian Budget Patterns ===')
indonesian_budget_tests = [
    'bantuan anggaran saya',
    'buatkan anggaran',
    'saya mau anggaran',
    'konsultasi anggaran',
    'analisis anggaran saya'
]

for test in indonesian_budget_tests:
    result = rules.parse_command(test)
    print(f'{test} -> {result.get("type")}')

print('\n=== Testing Pure Indonesian Purchase Patterns ===')
indonesian_purchase_tests = [
    'saya mau beli mobil 50000000',
    'mau beli laptop 15000000',
    'rencana beli motor 25000000',
    'analisis beli rumah 500000000',
    'konsultasi beli handphone 10000000'
]

for test in indonesian_purchase_tests:
    result = rules.parse_command(test)
    print(f'{test} -> {result.get("type")}, {result.get("item")}, {result.get("price")}')
