# Demo Financial Bot

Folder ini berisi demo dan contoh penggunaan Financial Bot dalam **bahasa Indonesia murni**.

## 🎯 Fitur Demo Utama

### 🇮🇩 Fitur Analisis Keuangan Indonesia

- 🏦 **Saran Anggaran**: "bantuan anggaran saya" → Rekomendasi anggaran sederhana
- 🛍️ **Analisis Pembelian**: "saya mau beli mobil 50000000" → Analisis rencana beli
- 💡 **Konsultasi Finansial**: Bantuan keuangan dalam bahasa natural Indonesia

### 📊 Fitur Dasar Pencatatan

- 💰 **Pencatatan Pemasukan**: "saya dapat gaji 5000000 dari kantor"
- 💸 **Pencatatan Pengeluaran**: "habis 50000 makan siang"
- 📈 **Laporan Keuangan**: "berapa saldo saya?"

## 📁 Files yang Tersedia

### Dokumentasi Demo

- `DEMO_SCENARIOS.md` - Skenario demo lengkap dengan contoh interaksi
- `README.md` - Panduan demo dan setup (file ini)

## 🚀 Cara Menjalankan Demo

### 1. Setup Environment

```bash
# Install dependencies
pip install -r requirements.txt

# Configure bot token
cp .env.example .env
# Edit .env dengan Discord Bot Token kamu
```

### 2. Demo via CLI (Mudah untuk Testing)

```bash
# Jalankan demo interaktif
python cli_runner.py

# Test fitur Indonesia
python -c "
from core.bot_core import FinancialBotCore
bot = FinancialBotCore()
print(bot.process_message('1', 'demo', 'bantuan anggaran saya'))
"
```

### 3. Demo via Discord Bot

```bash
# Jalankan bot Discord
python bot.py

# Test di Discord dengan mention:
# @FinancialBot bantuan anggaran saya
# @FinancialBot saya dapat gaji 5000000
# @FinancialBot saya mau beli laptop 15000000
```

## 💡 Tips Demo Interaktif

1. **Mulai dengan Fitur Baru**: Tunjukkan analisis keuangan Indonesia terlebih dahulu
2. **Gunakan Angka Realistis**: 5 juta gaji, 50 ribu makan, 15 juta laptop
3. **Demo Bahasa Natural**: Tunjukkan fleksibilitas bahasa Indonesia
4. **Tunjukkan Simplicity**: Sorot kesederhanaan analisis (15% darurat, 30% tabungan)

## 🎬 Alur Demo Recommended

```
1. Intro: "@FinancialBot siapa kamu?"
2. Setup: "@FinancialBot saya dapat gaji 5000000 dari kantor"
3. Expense: "@FinancialBot habis 50000 makan siang"
4. Check: "@FinancialBot berapa saldo saya?"
5. Budget: "@FinancialBot bantuan anggaran saya"
6. Purchase: "@FinancialBot saya mau beli laptop 15000000"
7. Report: "@FinancialBot buatkan laporan keuangan"
```

### Key Features yang Harus Disorot:

- 🇮🇩 **Pure Indonesian**: Tidak ada bahasa Inggris sama sekali
- 🧠 **Simple Logic**: Analisis yang mudah dipahami
- 💬 **Natural Language**: Fleksibilitas input bahasa natural
- 📊 **Smart Analysis**: Saran anggaran dan analisis pembelian otomatis

## Contoh Skenario Demo

```
User: !income 5000000 gaji bonus akhir tahun
Bot: Baik! Saya telah mencatat pemasukan kamu sebesar Rp 5,000,000...

User: saya habis 50000 untuk makan siang
Bot: Oke! Saya sudah catat pengeluaran kamu sebesar Rp 50,000...

User: berapa saldo saya?
Bot: 💰 Ringkasan Keuangan Kamu:
     • Pemasukan: Rp 5,000,000
     • Pengeluaran: Rp 50,000
     • Saldo: Rp 4,950,000 (positif)

User: laporan
Bot: 📊 Laporan Keuangan per Kategori: ...
```
