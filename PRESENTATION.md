# Financial Bot Discord - Presentasi

## 1. Latar Belakang Pembuatan Chatbot

### Masalah yang Diselesaikan

- **Pencatatan Keuangan Manual**: Banyak orang kesulitan mencatat pemasukan dan pengeluaran secara konsisten
- **Platform Terpisah**: Harus buka aplikasi khusus untuk mencatat keuangan
- **Kompleksitas Interface**: Aplikasi keuangan sering rumit untuk penggunaan sehari-hari
- **Kurang Interaktif**: Tidak ada feedback real-time atau reminder

### Solusi yang Ditawarkan

- **Integrasi Discord**: Menggunakan platform yang sudah familiar untuk komunitas/tim
- **Natural Language Processing**: Bisa menggunakan bahasa natural Indonesia
- **Real-time Tracking**: Pencatatan dan laporan instant
- **Automated Categorization**: Kategori otomatis berdasarkan deskripsi
- **Mention-Only Mode**: Bot hanya respond ketika di-mention untuk mengurangi spam

### Target Pengguna

- Mahasiswa yang ingin tracking uang jajan
- Freelancer yang perlu catat income dari berbagai projek
- Tim/komunitas yang ingin transparansi keuangan
- Keluarga yang ingin budgeting bersama

## 2. Kompleksitas Aturan (Rules)

### A. Regex-Based Pattern Matching

#### Income Patterns (4 Variations)

```regex
# Command format: !income 100000 gaji bonus
r'!income\s+(\d+(?:\.\d+)?)\s+(\w+)(?:\s+(.+))?'

# Natural language: saya dapat gaji 5000000 dari kantor
r'(?:saya|aku)\s+(?:dapat|terima|dapet|menerima|meraih|peroleh)\s+(\w+)\s+(\d+(?:\.\d+)?)\s*(?:dari\s+(.+))?'

# Simple: dapat 500000 freelance
r'(?:dapat|terima|dapet|menerima|meraih|peroleh)\s+(\d+(?:\.\d+)?)\s+(\w+)(?:\s+(.+))?'

# Generic: income 1000000 kategori deskripsi
r'(?:income|pemasukan|masuk)\s+(\d+(?:\.\d+)?)\s+(\w+)(?:\s+(.+))?'
```

#### Expense Patterns (4 Variations)

```regex
# Command: !expense 50000 makanan lunch
r'!expense\s+(\d+(?:\.\d+)?)\s+(\w+)(?:\s+(.+))?'

# Natural: saya habis 50000 untuk makanan
r'(?:saya|aku)\s+(?:habis|keluar|bayar|beli|menghabiskan|mengeluarkan|belanja|pakai|gunakan)\s+(\d+(?:\.\d+)?)\s+(?:untuk\s+)?(\w+)(?:\s+(.+))?'

# Action-first: beli makanan 25000
r'(?:beli|bayar|belanja)\s+(\w+)\s+(\d+(?:\.\d+)?)(?:\s+(.+))?'

# Generic: keluar 75000 transport
r'(?:keluar|habis|bayar|beli|expense|pengeluaran|menghabiskan|mengeluarkan|belanja|pakai|gunakan)\s+(\d+(?:\.\d+)?)\s+(?:untuk\s+)?(\w+)(?:\s+(.+))?'
```

#### Conversation Patterns

```regex
# About bot
r'(?:siapa)\s+(?:kamu|bot)'
r'(?:apa)\s+(?:nama)\s+(?:kamu)'

# Capabilities
r'(?:apa)\s+(?:yang bisa|bisa kamu)'
r'(?:kemampuan)\s+(?:kamu)'

# Thanks and goodbye
r'(?:terima kasih|makasih)'
r'(?:sampai jumpa|dadah)'
```

### B. Reflection Engine (Kata Ganti)

#### Pronoun Mapping - Bahasa Indonesia

```python
pronoun_reflections = {
    'saya': 'kamu',
    'aku': 'kamu',
    'kamu': 'saya',
    'anda': 'saya'
}
```

#### Contoh Reflection

- Input: "saya punya 100000"
- Output: "kamu punya 100000"
- Response: "Baik! Saya telah mencatat pemasukan **kamu**..."

### C. Automatic Categorization

#### Income Keywords - Bahasa Indonesia

```python
income_keywords = {
    'gaji': ['gaji', 'kantor', 'kerja', 'pekerjaan'],
    'freelance': ['freelance', 'projek', 'kontrak', 'lepas', 'sampingan'],
    'investasi': ['saham', 'reksadana', 'dividen', 'profit', 'trading', 'investasi'],
    'hadiah': ['hadiah', 'bonus', 'reward', 'kado', 'pemberian']
}
```

#### Expense Keywords - Bahasa Indonesia

```python
expense_keywords = {
    'makanan': ['makan', 'nasi', 'ayam', 'restaurant', 'cafe', 'snack', 'lapar', 'kenyang', 'minuman'],
    'transport': ['transport', 'bensin', 'ojek', 'taksi', 'bus', 'kereta', 'grab', 'gojek', 'motor', 'mobil'],
    'hiburan': ['film', 'game', 'spotify', 'netflix', 'youtube', 'concert', 'musik', 'hiburan'],
    'tagihan': ['listrik', 'air', 'internet', 'wifi', 'telepon', 'cicilan', 'bayar', 'tagihan']
}
```

### D. Advanced Pattern Features

#### Natural Language Support

- **Bahasa Indonesia Formal**: "saya dapat", "saya habis"
- **Bahasa Indonesia Casual**: "aku dapat", "aku habis"

#### Flexible Amount Parsing

- **Plain**: "50000"
- **With separators**: "1,000,000"
- **Decimal**: "99.5" (for 99.5k)

#### Context-Aware Categorization

```python
def categorize_automatically(description, amount):
    # Large amount (>1M) likely income
    if amount > 1000000:
        return 'gaji'
    # Small daily amounts likely expense
    else:
        return categorize_by_keywords(description)
```

#### Mention-Only Processing

```python
# Check if bot is mentioned
is_mentioned = bot.user in message.mentions
starts_with_mention = content.startswith(f'<@{bot.user.id}>')

# Only process if mentioned
if not (is_mentioned or starts_with_mention):
    return
```

## 3. Arsitektur Sistem

### Core Components

1. **Rules Engine** ([`core/rules.py`](core/rules.py))

   - Regex pattern matching untuk bahasa Indonesia
   - Reflection engine untuk conversation natural
   - Automatic categorization dengan keyword matching
   - Response generation dengan context awareness

2. **Database Manager** ([`core/database.py`](core/database.py))

   - SQLite operations
   - Transaction CRUD
   - Balance calculations
   - Category reports

3. **Bot Core** ([`core/bot_core.py`](core/bot_core.py))

   - Integration layer
   - Error handling
   - Logging
   - User session management

4. **Discord Bot** ([`bot.py`](bot.py))
   - Discord.py integration dengan mention-only mode
   - Event handling
   - Command processing
   - Rich embeds

### Data Flow

```
User Mention → Mention Check → Regex Parsing → Command Recognition →
Database Operation → Response Generation → Reflection Application → Discord Output
```

## 4. Testing & Quality Assurance

### Test Coverage (38 Comprehensive Tests)

#### A. Unit Tests - Rules Engine (13 tests)

- Pronoun reflection bahasa Indonesia
- Income command parsing (4 variations)
- Expense command parsing (4 variations)
- Balance/report/help command recognition
- About/capability/thanks/goodbye patterns
- Automatic categorization
- Amount parsing edge cases
- Unknown command handling
- Response generation

#### B. Unit Tests - Database (12 tests)

- Database initialization
- Add income/expense transactions
- Multiple transactions & balance calculation
- Transaction retrieval & ordering
- Category reporting
- Transaction deletion
- Invalid transaction handling
- User data isolation
- Large number handling
- Available categories

#### C. Integration Tests (13 tests)

- Complete income flow (end-to-end)
- Complete expense flow (end-to-end)
- Balance query variations
- Report generation
- Help command
- Automatic categorization in context
- Negative balance warnings
- Invalid amount handling
- Unknown command handling
- Multi-user isolation
- Large number handling

### Test Statistics

```
======================================================================
platform win32 -- Python 3.11.9, pytest-8.4.2, pluggy-1.6.0
collected 38 items

tests/test_database.py::TestDatabaseManager (12 tests) - 100% PASSED
tests/test_integration.py::TestBotCoreIntegration (13 tests) - 100% PASSED
tests/test_rules.py::TestReflectionEngine (1 test) - 100% PASSED
tests/test_rules.py::TestFinancialRulesEngine (12 tests) - 100% PASSED

======================================================================
38 passed, 1 warning in 1.14s
======================================================================
```

- **Total Tests**: 38 test cases (100% PASSED)
- **Coverage Areas**: Rules Engine, Database, Integration
- **Test Types**: Unit, Integration, Functional
- **Error Handling**: Invalid inputs, edge cases
- **Performance**: All tests completed in 1.14 seconds

## 5. Fitur Unggulan

### A. Natural Language Processing Bahasa Indonesia

```
✅ "@FinancialBot !income 5000000 gaji" (Command format)
✅ "@FinancialBot saya dapat gaji 5000000 dari kantor" (Natural)
✅ "@FinancialBot dapat 1000000 freelance" (Simple)
✅ "@FinancialBot aku dapat 500000 projek" (Casual)
```

### B. Smart Categorization

```python
Input: "@FinancialBot habis 50000 makan siang di warteg"
→ Auto-detect: category="makanan"

Input: "@FinancialBot bayar 200000 listrik bulan ini"
→ Auto-detect: category="tagihan"
```

### C. Rich Reporting

```
📊 **Laporan Keuangan per Kategori:**

💰 **Total Pemasukan**: Rp 6,000,000
💸 **Total Pengeluaran**: Rp 500,000
📈 **Saldo**: Rp 5,500,000

**📋 Breakdown per Kategori:**

**Gaji:**
  💚 Masuk: Rp 5,000,000
  📈 Net: Rp 5,000,000

**Makanan:**
  💸 Keluar: Rp 350,000
  📉 Net: Rp -350,000
```

### D. Mention-Only Mode

- **Spam Protection**: Bot hanya respond ketika di-mention
- **Clean Channels**: Tidak ada interference dengan conversation lain
- **Clear Intent**: User harus explicit mention bot untuk interaction

## 6. Implementasi Technical

### A. Discord Integration dengan Mention Check

```python
# Mention detection
is_mentioned = bot.user in message.mentions
starts_with_mention = content.startswith(f'<@{bot.user.id}>')

# Clean content dari mention
if starts_with_mention:
    clean_content = content.replace(f'<@{bot.user.id}>', '').strip()

# Rich embed responses
embed = discord.Embed(title="📊 Statistik Keuangan")
embed.add_field(name="💰 Saldo", value=f"Rp {balance:,.0f}")
```

### B. Error Handling

- **Invalid amounts**: "Jumlah harus lebih dari 0"
- **Unknown commands**: Suggestion untuk `!help`
- **Database errors**: Graceful fallback
- **Permission errors**: Clear error messages

### C. Logging & Monitoring

```python
self.logger.info(f"Mentioned by {username}: {clean_content}")
self.logger.info(f"Income added: {username} - Rp {amount:,.0f}")
self.logger.error(f"Database error: {e}")
```

## 7. Deployment & Usage

### Setup Process

1. **Clone Repository**
2. **Install Dependencies**: `pip install -r requirements.txt`
3. **Configure Token**: Copy `.env.example` → `.env`
4. **Run Bot**: `python bot.py`
5. **Test CLI**: `python cli_runner.py`

### Mention-Based Commands

```
@FinancialBot !income <amount> <category> <description>  # Add income
@FinancialBot !expense <amount> <category> <description> # Add expense
@FinancialBot !balance                                   # Check balance
@FinancialBot !report                                    # Generate report
@FinancialBot !help                                      # Show help
@FinancialBot !stats                                     # Detailed statistics
```

### Natural Commands (dengan Mention)

```
@FinancialBot saya dapat gaji 5000000 dari kantor
@FinancialBot habis 50000 untuk makan siang
@FinancialBot berapa saldo saya?
@FinancialBot lihat laporan keuangan
@FinancialBot bantuan
```

### Conversation Commands

```
@FinancialBot siapa kamu?
@FinancialBot apa yang bisa kamu lakukan?
@FinancialBot terima kasih
@FinancialBot sampai jumpa
```

## 8. Kesimpulan

Financial Bot Discord menggabungkan:

### ✅ Kompleksitas Technical

- **20+ Regex patterns** untuk parsing multi-format bahasa Indonesia
- **Reflection engine** untuk natural conversation
- **Auto-categorization** dengan keyword matching approach
- **Mention-only processing** untuk clean Discord experience

### ✅ User Experience

- **Zero learning curve** - gunakan bahasa Indonesia sehari-hari
- **Real-time feedback** dengan emoji dan formatting
- **Rich reporting** dengan breakdown kategori
- **Error handling** yang informatif
- **Non-intrusive** - hanya respond ketika di-mention

### ✅ Quality Assurance

- **38 comprehensive tests** covering all scenarios (100% PASSED)
- **End-to-end testing** dari mention ke output
- **Edge case handling** untuk robust operation
- **Multi-user isolation** untuk privacy
- **Performance optimization** - tests complete in 1.14s

### ✅ Language Processing

- **Natural Language Understanding** untuk bahasa Indonesia
- **Context-aware categorization** berdasarkan deskripsi
- **Flexible input parsing** untuk berbagai format
- **Conversation support** untuk interaction yang natural

### 🚀 Scalability

- **Modular architecture** mudah dikembangkan
- **Database abstraction** bisa ganti ke PostgreSQL
- **Plugin system** untuk fitur tambahan
- **API ready** untuk integrasi external

**Financial Bot Discord** adalah **intelligent financial assistant** yang memahami bahasa natural Indonesia dan memberikan insights keuangan real-time melalui platform Discord dengan mention-only mode untuk pengalaman yang clean dan focused.

🚀 **Ready to manage your finances smartly? Just mention @FinancialBot and start tracking!**
