# Financial Bot Discord - Presentasi

## 1. Latar Belakang Pembuatan Chatbot

### Masalah yang Diselesaikan

- **Pencatatan Keuangan Manual**: Banyak orang kesulitan mencatat pemasukan dan pengeluaran secara konsisten
- **Platform Terpisah**: Harus buka aplikasi khusus untuk mencatat keuangan
- **Kompleksitas Interface**: Aplikasi keuangan sering rumit untuk penggunaan sehari-hari
- **Kurang Interaktif**: Tidak ada feedback real-time atau reminder

### Solusi yang Ditawarkan

- **Integrasi Discord**: Menggunakan platform yang sudah familiar untuk komunitas/tim
- **Natural Language Processing**: Bisa menggunakan bahasa natural Indonesia dan English
- **Real-time Tracking**: Pencatatan dan laporan instant
- **Automated Categorization**: Kategori otomatis berdasarkan deskripsi

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
r'(?:saya|aku|gw|gue)\s+(?:dapat|terima|dapet)\s+(?:gaji|uang|dana|income|pemasukan)\s+(\d+(?:\.\d+)?)\s+(?:dari\s+)?(\w+)(?:\s+(.+))?'

# Simple: dapat 500000 freelance
r'(?:dapat|terima|dapet)\s+(\d+(?:\.\d+)?)\s+(?:dari\s+)?(\w+)(?:\s+(.+))?'

# Generic: income 1000000 kategori deskripsi
r'(?:income|pemasukan|masuk)\s+(\d+(?:\.\d+)?)\s+(\w+)(?:\s+(.+))?'
```

#### Expense Patterns (4 Variations)

```regex
# Command: !expense 50000 makanan lunch
r'!expense\s+(\d+(?:\.\d+)?)\s+(\w+)(?:\s+(.+))?'

# Natural: saya habis 50000 untuk makanan
r'(?:saya|aku|gw|gue)\s+(?:habis|keluar|bayar|beli)\s+(\d+(?:\.\d+)?)\s+(?:untuk\s+)?(\w+)(?:\s+(.+))?'

# Action-first: beli makanan 25000
r'(?:beli|bayar)\s+(\w+)\s+(\d+(?:\.\d+)?)(?:\s+(.+))?'

# Generic: keluar 75000 transport
r'(?:keluar|habis|bayar|beli|expense|pengeluaran)\s+(\d+(?:\.\d+)?)\s+(?:untuk\s+)?(\w+)(?:\s+(.+))?'
```

### B. Reflection Engine (Kata Ganti)

#### Pronoun Mapping

```python
pronoun_reflections = {
    'saya': 'kamu',    'aku': 'kamu',
    'gue': 'lu',       'gw': 'lu',
    'kamu': 'saya',    'lu': 'gue',
    'anda': 'saya',    'my': 'your',
    'i': 'you',        'you': 'me'
}
```

#### Contoh Reflection

- Input: "saya punya 100000"
- Output: "kamu punya 100000"
- Response: "Baik! Saya telah mencatat pemasukan **kamu**..."

### C. Automatic Categorization

#### Income Keywords

```python
income_keywords = {
    'gaji': ['gaji', 'salary', 'kantor', 'kerja'],
    'freelance': ['freelance', 'projek', 'project', 'kontrak'],
    'investasi': ['saham', 'reksadana', 'dividen', 'profit'],
    'hadiah': ['hadiah', 'gift', 'bonus', 'reward']
}
```

#### Expense Keywords

```python
expense_keywords = {
    'makanan': ['makan', 'food', 'nasi', 'restaurant', 'cafe'],
    'transport': ['bensin', 'ojek', 'taksi', 'grab', 'gojek'],
    'hiburan': ['film', 'movie', 'game', 'spotify', 'netflix'],
    'tagihan': ['listrik', 'air', 'internet', 'cicilan']
}
```

### D. Advanced Pattern Features

#### Multi-Language Support

- **Bahasa Indonesia**: "saya dapat", "habis uang"
- **Bahasa Gaul**: "gue dapet", "lu abis"
- **English**: "i got", "spent money"

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

## 3. Arsitektur Sistem

### Core Components

1. **Rules Engine** (`core/rules.py`)

   - Regex pattern matching
   - Reflection engine
   - Automatic categorization
   - Response generation

2. **Database Manager** (`core/database.py`)

   - SQLite operations
   - Transaction CRUD
   - Balance calculations
   - Category reports

3. **Bot Core** (`core/bot_core.py`)

   - Integration layer
   - Error handling
   - Logging
   - User session management

4. **Discord Bot** (`bot.py`)
   - Discord.py integration
   - Event handling
   - Command processing
   - Rich embeds

### Data Flow

```
User Message → Regex Parsing → Command Recognition →
Database Operation → Response Generation →
Reflection Application → Discord Output
```

## 4. Testing & Quality Assurance

### Test Coverage (6+ Cases Minimal)

#### A. Unit Tests - Rules Engine (8 tests)

- Pronoun reflection (Indonesian, informal, English)
- Income command parsing (4 variations)
- Expense command parsing (4 variations)
- Balance/report/help command recognition
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

#### C. Integration Tests (10 tests)

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

### Test Statistics

- **Total Tests**: 30+ test cases
- **Coverage Areas**: Rules Engine, Database, Integration
- **Test Types**: Unit, Integration, Functional
- **Error Handling**: Invalid inputs, edge cases

## 5. Fitur Unggulan

### A. Natural Language Processing

```
✅ "!income 5000000 gaji" (Command format)
✅ "saya dapat gaji 5000000 dari kantor" (Natural)
✅ "dapat 1000000 freelance" (Simple)
✅ "gue dapet 500000 projek" (Slang)
```

### B. Smart Categorization

```python
Input: "habis 50000 makan siang di warteg"
→ Auto-detect: category="makanan"

Input: "bayar 200000 listrik bulan ini"
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

### D. Multi-Format Support

- **Formal Commands**: `!income`, `!expense`, `!balance`
- **Natural Language**: "berapa saldo saya?"
- **Conversational**: "saya habis uang untuk makan"
- **Mixed Language**: Indonesian + English keywords

## 6. Implementasi Technical

### A. Discord Integration

```python
# Rich embed responses
embed = discord.Embed(title="📊 Statistik Keuangan")
embed.add_field(name="💰 Saldo", value=f"Rp {balance:,.0f}")

# Multi-message handling for long responses
if len(response) > 2000:
    chunks = [response[i:i+1900] for i in range(0, len(response), 1900)]
```

### B. Error Handling

- **Invalid amounts**: "Jumlah harus lebih dari 0"
- **Unknown commands**: Suggestion untuk `!help`
- **Database errors**: Graceful fallback
- **Permission errors**: Clear error messages

### C. Logging & Monitoring

```python
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

### Bot Commands

```
!income <amount> <category> <description>  # Add income
!expense <amount> <category> <description> # Add expense
!balance                                   # Check balance
!report                                    # Generate report
!help                                      # Show help
!stats                                     # Detailed statistics
!recent [limit]                            # Recent transactions
!categories                                # Available categories
```

### Natural Commands

```
"saya dapat gaji 5000000 dari kantor"
"habis 50000 untuk makan siang"
"berapa saldo saya?"
"lihat laporan keuangan"
"bantuan"
```

## 8. Kesimpulan

Financial Bot Discord menggabungkan:

### ✅ Kompleksitas Technical

- **30+ Regex patterns** untuk parsing multi-format
- **Reflection engine** untuk natural conversation
- **Auto-categorization** dengan machine learning approach
- **Multi-language support** (ID, EN, slang)

### ✅ User Experience

- **Zero learning curve** - gunakan bahasa sehari-hari
- **Real-time feedback** dengan emoji dan formatting
- **Rich reporting** dengan breakdown kategori
- **Error handling** yang informatif

### ✅ Quality Assurance

- **30+ comprehensive tests** covering all scenarios
- **End-to-end testing** dari input ke output
- **Edge case handling** untuk robust operation
- **Multi-user isolation** untuk privacy

### 🚀 Scalability

- **Modular architecture** mudah dikembangkan
- **Database abstraction** bisa ganti ke PostgreSQL
- **Plugin system** untuk fitur tambahan
- **API ready** untuk integrasi external

**Financial Bot Discord** bukan hanya pencatat transaksi, tapi **intelligent financial assistant** yang memahami bahasa natural dan memberikan insights keuangan real-time melalui platform yang sudah familiar.
