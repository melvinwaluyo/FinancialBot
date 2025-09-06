# Financial Bot Discord

Bot Discord untuk melacak pemasukan dan pengeluaran keuangan menggunakan Python dengan sistem berbasis aturan (regex), reflection kata ganti, dan natural language processing bahasa Indonesia.

## 🎯 Latar Belakang

Financial Bot dirancang untuk membantu pengguna mengelola keuangan pribadi atau kelompok melalui Discord. Bot ini menyelesaikan masalah pencatatan manual yang sering terlupakan dengan menyediakan interface yang mudah digunakan di platform yang sudah familiar.

### Masalah yang Diselesaikan

- **Pencatatan Keuangan Manual**: Kesulitan mencatat pemasukan dan pengeluaran secara konsisten
- **Platform Terpisah**: Harus buka aplikasi khusus untuk mencatat keuangan
- **Kompleksitas Interface**: Aplikasi keuangan sering rumit untuk penggunaan sehari-hari
- **Kurang Interaktif**: Tidak ada feedback real-time atau reminder

## ✨ Fitur

### Core Features

- 📊 **Transaction Tracking**: Pencatatan pemasukan dan pengeluaran real-time
- 💰 **Auto Categorization**: Kategori transaksi otomatis berdasarkan deskripsi
- 📈 **Financial Reports**: Laporan keuangan per kategori dengan breakdown
- 🔄 **Reflection Engine**: Kata ganti untuk interaksi natural (saya↔kamu)
- 🤖 **Regex-Based Rules**: Sistem parsing perintah dengan 30+ pattern variations

### Language Support

- 🇮🇩 **Bahasa Indonesia**: "saya dapat gaji 5000000 dari kantor"

### Smart Features

- 🎯 **Mention-Only Mode**: Bot hanya respond ketika di-mention (@FinancialBot)
- 🧠 **Context Awareness**: Memahami intent dari bahasa natural
- 📋 **Rich Formatting**: Response dengan emoji dan formatting yang menarik
- 👥 **Multi-User Support**: Data terpisah per user dengan privacy

## 🚀 Setup & Installation

### Prerequisites

- Python 3.8+
- Discord Bot Token
- Virtual Environment (recommended)

### Quick Start

1. **Clone Repository**

```bash
git clone <repository-url>
cd FinancialBot
```

2. **Setup Virtual Environment**

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

3. **Install Dependencies**

```bash
pip install -r requirements.txt
```

4. **Configure Environment**

```bash
# Copy template dan edit dengan token bot Anda
copy .env.example .env
# Edit .env file dengan Discord Bot Token
```

5. **Run Bot**

```bash
# Discord Mode (Production)
python bot.py

# CLI Mode (Testing)
python cli_runner.py
```

## 💬 Cara Penggunaan

### ⚠️ PENTING: Mention Bot

Bot hanya akan merespons ketika di-mention. Contoh:

```
@FinancialBot !income 5000000 gaji
@FinancialBot saya habis 50000 untuk makan
@FinancialBot berapa saldo saya?
```

### Command Format

#### 📈 Income Commands

```bash
# Format command
@FinancialBot !income <jumlah> <kategori> <deskripsi>

# Natural language
@FinancialBot saya dapat gaji 5000000 dari kantor
@FinancialBot dapat 1000000 freelance projek website
```

#### 📉 Expense Commands

```bash
# Format command
@FinancialBot !expense <jumlah> <kategori> <deskripsi>

# Natural language
@FinancialBot saya habis 50000 untuk makan siang
@FinancialBot beli makanan 25000
@FinancialBot bayar listrik 200000
```

#### 💰 Balance & Reports

```bash
@FinancialBot !balance
@FinancialBot saldo saya
@FinancialBot berapa uang saya?

@FinancialBot !report
@FinancialBot laporan keuangan
```

#### 🤖 Conversation

```bash
@FinancialBot siapa kamu?
@FinancialBot apa yang bisa kamu lakukan?
@FinancialBot terima kasih
@FinancialBot sampai jumpa
```

#### 🛠️ Utility Commands

```bash
@FinancialBot !help          # Panduan lengkap
```

## 🧪 Testing

### Run Tests

```bash
# Windows
run_tests.bat

# Linux/Mac
chmod +x run_tests.sh
./run_tests.sh

# Manual pytest
python -m pytest tests/ -v
```

### Test Coverage

- **30+ test cases** covering all functionality
- **Unit Tests**: Rules engine, database operations
- **Integration Tests**: End-to-end transaction flows
- **Edge Cases**: Invalid inputs, error handling

## 🏗️ Project Structure

```
FinancialBot/
├── 📁 core/                    # Core bot logic
│   ├── bot_core.py            # Main bot integration
│   ├── rules.py               # Regex patterns & reflection
│   ├── database.py            # SQLite database manager
│   └── __init__.py
├── 📁 tests/                  # Comprehensive test suite
│   ├── test_rules.py          # Rules engine tests
│   ├── test_database.py       # Database tests
│   ├── test_integration.py    # Integration tests
│   └── run_tests.py
├── 📁 demo/                   # Demo screenshots & scenarios
├── 📁 logs/                   # Application logs
├── bot.py                     # Discord bot main entry
├── cli_runner.py              # CLI testing interface
├── requirements.txt           # Python dependencies
├── .env.example              # Environment template
├── SETUP.md                  # Detailed setup guide
├── PRESENTATION.md           # Technical presentation
└── README.md                 # This file
```

## 📊 Demo Examples

### Income Tracking

```
User: @FinancialBot saya dapat gaji 5000000 dari kantor
Bot:  Baik! Saya telah mencatat pemasukan kamu sebesar Rp 5,000,000
      untuk kategori 'gaji' dengan deskripsi 'dari kantor'.
      💰 Saldo terbaru: Rp 5,000,000
```

### Expense Tracking

```
User: @FinancialBot habis 50000 makan siang
Bot:  Oke! Saya sudah catat pengeluaran kamu sebesar Rp 50,000
      untuk kategori 'makanan'.
      💰 Saldo terbaru: Rp 4,950,000
```

### Balance Report

```
User: @FinancialBot berapa saldo saya?
Bot:  💰 **Ringkasan Keuangan Kamu:**
      • Pemasukan: Rp 5,000,000
      • Pengeluaran: Rp 50,000
      • Saldo: Rp 4,950,000 (positif)

      📋 **5 Transaksi Terakhir:**
      1. 💸 Rp 50,000 - makanan
      2. 💚 Rp 5,000,000 - gaji (dari kantor)
```

### Conversation

```
User: @FinancialBot siapa kamu?
Bot:  👋 Hai! Saya adalah **Financial Bot**, asisten keuangan pintar untuk Discord!

      🤖 **Tentang Saya:**
      • Nama: Financial Bot
      • Fungsi: Membantu melacak pemasukan dan pengeluaran
      • Bahasa: Indonesia
      • Dibuat dengan: Python
```

## 🔍 Advanced Features

### Smart Categorization

```python
# Auto-detect dari deskripsi
"makan siang di warteg" → kategori: makanan
"bayar listrik bulan ini" → kategori: tagihan
"bensin motor" → kategori: transport
"gaji dari kantor" → kategori: gaji
```

### Reflection Engine

```python
Input:  "saya punya 100000"
Output: "Baik! Saya telah mencatat pemasukan kamu..."
        # "saya" → "kamu" reflection
```

### Multi-Format Support

```bash
✅ !income 1000000 gaji                    # Command format
✅ saya dapat gaji 1000000 dari kantor     # Natural Indonesian
✅ dapat 1000000 projek                    # Simple format
```

**Financial Bot Discord** - Intelligent financial assistant yang memahami bahasa natural Indonesia dan memberikan insights keuangan real-time melalui platform Discord yang familiar.

🚀 **Ready to manage your finances smartly? Just mention @FinancialBot and start tracking!**
