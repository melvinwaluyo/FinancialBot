# Pemrosesan Bahasa Alami - Kelas A | Dosen: Syukron Abu Ishaq Alfarozi, S.T., Ph.D.

## Melvin Waluyo (22/492978/TK/53955)

## Muhammad Grandiv Lava Putra (22/493242/TK/54023)

# Financial Bot Discord

Bot Discord untuk melacak pemasukan dan pengeluaran keuangan menggunakan Python dengan sistem berbasis aturan (regex), reflection kata ganti, dan natural language processing bahasa Indonesia.

## 🎯 Latar Belakang

Financial Bot dirancang untuk membantu pengguna mengelola keuangan pribadi atau kelompok melalui Discord. Bot ini menyelesaikan masalah pencatatan manual yang sering terlupakan dengan menyediakan interface yang mudah digunakan di platform yang sudah familiar.

### Masalah yang Diselesaikan

- **Pencatatan Keuangan Manual**: Kesulitan mencatat pemasukan dan pengeluaran secara konsisten
- **Platform Terpisah**: Harus buka aplikasi khusus untuk mencatat keuangan
- **Kompleksitas Interface**: Aplikasi keuangan sering rumit untuk penggunaan sehari-hari
- **Kurang Interaktif**: Tidak ada feedback real-time, reminder, atau analisis

## ✨ Fitur

### Fitur Utama

- 📊 **Pencatatan Transaksi**: Pencatatan pemasukan dan pengeluaran real-time
- 💰 **Kategorisasi Otomatis**: Kategori transaksi otomatis berdasarkan deskripsi
- 📈 **Laporan Keuangan**: Laporan keuangan per kategori dengan breakdown
- 🔄 **Mesin Refleksi**: Kata ganti untuk interaksi natural (saya↔kamu)
- 🤖 **Sistem Regex**: Sistem parsing perintah dengan 30+ variasi pattern
- 🏦 **Saran Anggaran**: Rekomendasi anggaran bulanan yang sederhana dan mudah dipahami
- 🛍️ **Analisis Pembelian**: Analisis rencana pembelian dengan pertimbangan kemampuan finansial
- 📊 **Evaluasi Keuangan**: Penilaian kesehatan keuangan otomatis dengan saran praktis
- 💡 **Konsultasi Finansial**: Bantuan perencanaan keuangan dalam bahasa Indonesia

### Language Support

- 🇮🇩 **Bahasa Indonesia**

### Smart Features

- 🎯 **Mention-Only Mode**: Bot hanya respond ketika di-mention (@FinancialBot)
- 🧠 **Context Awareness**: Memahami intent dari bahasa natural
- 📋 **Rich Formatting**: Response dengan emoji dan formatting yang menarik
- 👥 **Multi-User Support**: Data terpisah per user dengan privacy

## 🚀 Setup & Instalasi

### Persyaratan Sistem

- Python 3.8+
- Discord Bot Token
- Virtual Environment (direkomendasikan)

### Panduan Instalasi

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

4. **Konfigurasi Environment**

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
@FinancialBot saya ingin membeli mobil 300000000
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

#### 🆕 Budget Advice & Purchase Planning

```bash
# Budget Advice
@FinancialBot help me create a budget
@FinancialBot bantuan budget saya
@FinancialBot buatkan budget
@FinancialBot analisis budget saya

# Purchase Planning
@FinancialBot I want to buy a $30000 car
@FinancialBot saya mau beli laptop 15000000
@FinancialBot I want to buy a house 500000000
@FinancialBot analisis beli motor 25000000
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

## 🧪 Pengujian

### Menjalankan Test

```bash
# Windows
run_tests.bat

# Linux/Mac
chmod +x run_tests.sh
./run_tests.sh

# Manual pytest
python -m pytest tests/ -v
```

### Cakupan Test

- **30+ test cases** yang mencakup semua fungsi
- **Unit Tests**: Rules engine, operasi database
- **Integration Tests**: Alur transaksi end-to-end
- **Edge Cases**: Input tidak valid, error handling

## 🎯 Contoh Fitur

### Contoh Saran Anggaran

```
Anda: bantuan anggaran saya

MoGre Financial Assistant:
💰 **Ringkasan Keuangan Bulanan**:
• **Pemasukan**: Rp 6,250,000
• **Pengeluaran**: Rp 4,500,000
• **Sisa Uang**: Rp 1,750,000

📊 **Saran Penggunaan Sisa Uang**:
• **Dana Darurat**: Rp 937,500 (15% dari pemasukan)
• **Tabungan**: Rp 1,875,000 (30% dari pemasukan)

💡 **Rekomendasi**:
Prioritaskan dana darurat dan tabungan secara seimbang untuk keamanan finansial jangka panjang.
```

### Contoh Analisis Pembelian

```
Anda: saya mau beli mobil 30000000

MoGre Financial Assistant:
🛍️ **Analisis Beli Mobil**:

**Harga**: Rp 30,000,000
**Pemasukan Bulanan**: Rp 6,250,000
**Sisa Uang**: Rp 1,750,000

💡 **Pilihan yang Tersedia**:

**Pilihan 1**: Alternatif Lebih Murah (Rp 18,000,000)
• Mengurangi beban finansial
• Lebih sesuai dengan kemampuan saat ini

**Pilihan 2**: Menabung Dulu
• Tabung selama 16 bulan untuk bayar tunai
• Menghindari beban cicilan bulanan

**Pilihan 3**: Jika Harus Beli Sekarang
```

• Large down payment (Rp 1,400,000)
• Shop for best interest rates
• Consider certified pre-owned options
• Ensure warranty coverage

🎯 **Recommendation**: Wait and save for this purchase. Building financial stability first will give you better options and peace of mind.

```

## 🏗️ Struktur Proyek

```

FinancialBot/
├── 📁 core/ # Core bot logic
│ ├── bot_core.py # Main bot integration
│ ├── rules.py # Regex patterns & reflection
│ ├── database.py # SQLite database manager
│ └── **init**.py
├── 📁 tests/ # Comprehensive test suite
│ ├── test_rules.py # Rules engine tests
│ ├── test_database.py # Database tests
│ ├── test_integration.py # Integration tests
│ └── run_tests.py
├── 📁 demo/ # Demo screenshots & scenarios
├── 📁 logs/ # Application logs
├── bot.py # Discord bot main entry
├── cli_runner.py # CLI testing interface
├── requirements.txt # Python dependencies
├── .env.example # Environment template
├── SETUP.md # Detailed setup guide
├── PRESENTATION.md # Technical presentation
└── README.md # This file

```

## 📊 Contoh Demo

### Pencatatan Pemasukan

```

User: @FinancialBot saya dapat gaji 5000000 dari kantor
Bot: Baik! Saya telah mencatat pemasukan kamu sebesar Rp 5,000,000
untuk kategori 'gaji' dengan deskripsi 'dari kantor'.
💰 Saldo terbaru: Rp 5,000,000

```

### Pencatatan Pengeluaran

```

User: @FinancialBot habis 50000 makan siang
Bot: Oke! Saya sudah catat pengeluaran kamu sebesar Rp 50,000
untuk kategori 'makanan'.
💰 Saldo terbaru: Rp 4,950,000

```

### Laporan Saldo

```

User: @FinancialBot berapa saldo saya?
Bot: 💰 **Ringkasan Keuangan Kamu:**
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
Bot: 👋 Hai! Saya adalah **Financial Bot**, asisten keuangan pintar untuk Discord!

      🤖 **Tentang Saya:**
      • Nama: Financial Bot
      • Fungsi: Membantu melacak pemasukan dan pengeluaran
      • Bahasa: Indonesia
      • Dibuat dengan: Python

````

## 🔍 Advanced Features

### Smart Categorization

```python
# Auto-detect dari deskripsi
"makan siang di warteg" → kategori: makanan
"bayar listrik bulan ini" → kategori: tagihan
"bensin motor" → kategori: transport
"gaji dari kantor" → kategori: gaji
````

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
