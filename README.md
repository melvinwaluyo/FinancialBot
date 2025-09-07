# Pemrosesan Bahasa Alami - Kelas A | Dosen: Syukron Abu Ishaq Alfarozi, S.T., Ph.D.

## Melvin Waluyo (22/492978/TK/53955)

## Muhammad Grandiv Lava Putra (22/493242/TK/54023)

---

# Financial Bot Discord

Bot Discord untuk melacak pemasukan dan pengeluaran menggunakan natural language processing bahasa Indonesia dengan sistem regex dan reflection kata ganti.

## 🎯 Latar Belakang

Financial Bot membantu pengguna mengelola keuangan melalui Discord dengan interface yang familiar dan mudah digunakan.

### Masalah yang Diselesaikan

- Pencatatan keuangan manual yang sering terlupakan
- Kompleksitas aplikasi keuangan tradisional
- Kurangnya feedback real-time

### Solusi

- Natural Language Processing bahasa Indonesia
- Integrasi dengan platform Discord yang familiar
- Kategorisasi otomatis dan laporan real-time

## ✨ Fitur Utama

- 📊 **Pencatatan Transaksi**: Pemasukan dan pengeluaran real-time
- 💰 **Kategorisasi Otomatis**: Berdasarkan deskripsi transaksi
- 🔄 **Reflection Engine**: Kata ganti untuk conversation natural (saya↔kamu)
- 🏦 **Saran Anggaran**: Rekomendasi keuangan sederhana
- 🛍️ **Analisis Pembelian**: Evaluasi rencana pembelian
- 🇮🇩 **Bahasa Indonesia**: Mendukung bahasa formal dan kasual
- 🎯 **Mention-Only**: Bot hanya respond ketika di-mention

## 🚀 Setup & Instalasi

### Persyaratan

- Python 3.8+
- Discord Bot Token

### Membuat Discord Bot

1. **Discord Developer Portal**
   - Buka https://discord.com/developers/applications
   - Klik **"New Application"** → nama: **"Financial Bot"**
2. **Setup Bot**

   - Sidebar **"Bot"** → **"Add Bot"**
   - Enable **"Message Content Intent"** ✅
   - Copy **Token** (jangan bagikan!)

3. **Invite Bot ke Server**
   - **"OAuth2"** → **"URL Generator"**
   - **Scopes**: ✅ `bot`
   - **Permissions**: Send Messages, Read Message History, Embed Links
   - Copy URL dan authorize ke server Discord

### Instalasi

```bash
# Clone repository
git clone <repository-url>
cd FinancialBot

# Setup virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Setup environment
copy .env.example .env
# Edit .env dengan Discord Bot Token

# Run bot
python bot.py
```

## 💬 Cara Penggunaan

**⚠️ PENTING**: Bot hanya respond ketika di-mention (@FinancialBot)

### Basic Commands

```bash
# Pencatatan pemasukan
@FinancialBot !income 5000000 gaji
@FinancialBot saya dapat gaji 5000000 dari kantor

# Pencatatan pengeluaran
@FinancialBot !expense 50000 makanan
@FinancialBot habis 50000 makan siang

# Cek saldo dan laporan
@FinancialBot !balance
@FinancialBot berapa saldo saya?
@FinancialBot !report

# Fitur analisis
@FinancialBot bantuan anggaran saya
@FinancialBot saya mau beli laptop 15000000

# Utility
@FinancialBot !help
@FinancialBot siapa kamu?
```

## 🧪 Testing

```bash
# Run tests
run_tests.bat  # Windows
./run_tests.sh # Linux/Mac

# CLI testing mode
python cli_runner.py
```

**Test Results**: 79 test cases (100% PASSED) dalam 13.54 detik

## 🔍 Fitur Advanced

### Smart Categorization

```python
"makan siang di warteg" → kategori: makanan
"bayar listrik bulan ini" → kategori: tagihan
"gaji dari kantor" → kategori: gaji
```

### Reflection Engine

```python
Input:  "saya punya 100000"
Output: "Baik! Saya telah mencatat pemasukan kamu..."
```

### Multi-Format Support

```bash
✅ !income 1000000 gaji           # Command format
✅ saya dapat gaji 1000000        # Natural Indonesian
✅ aku dapet 500000 freelance     # Casual Indonesian
```

## 🏗️ Struktur Project

```
FinancialBot/
├── core/                 # Core bot logic
│   ├── bot_core.py      # Main integration
│   ├── rules.py         # Regex patterns & reflection
│   └── database.py      # SQLite database
├── tests/               # Test suite (79 tests)
├── demo/                # Demo scenarios
├── bot.py               # Discord bot entry point
├── cli_runner.py        # CLI testing
└── requirements.txt     # Dependencies
```

## 📊 Dokumentasi

- [PRESENTATION.md](PRESENTATION.md) - Technical details
- [demo/](demo/) - Demo scenarios & examples

## 🧪 Quality Assurance

- **79 comprehensive tests** (100% PASSED)
- **End-to-end testing** dari mention ke output
- **Multi-user isolation** untuk privacy
- **Error handling** yang robust
- **Performance tested** untuk scalability

---

**Financial Bot Discord** - Intelligent financial assistant yang memahami bahasa natural Indonesia untuk tracking keuangan real-time di Discord.

🚀 **Siap mencatat keuangan dengan smart? Mention @FinancialBot dan mulai tracking!**
