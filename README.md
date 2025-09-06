# Financial Bot Discord

Bot Discord untuk melacak pemasukan dan pengeluaran keuangan menggunakan Python dengan sistem berbasis aturan (regex) dan reflection kata ganti.

## Latar Belakang

Financial Bot dirancang untuk membantu pengguna mengelola keuangan pribadi atau kelompok melalui Discord. Bot ini menyelesaikan masalah pencatatan manual yang sering terlupakan dengan menyediakan interface yang mudah digunakan di platform yang sudah familiar.

## Fitur

- 📊 Tracking pemasukan dan pengeluaran
- 💰 Kategori transaksi otomatis
- 📈 Laporan keuangan
- 🔄 Reflection kata ganti untuk interaksi natural
- 🤖 Sistem berbasis aturan (regex) untuk parsing perintah

## Setup & Run

### Prerequisites

- Python 3.8+
- Discord Bot Token

### Instalasi

1. Clone repository

```bash
git clone <repository-url>
cd FinancialBot
```

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Setup environment

```bash
copy .env.example .env
# Edit .env dengan Discord Bot Token Anda
```

4. Run bot

```bash
python bot.py
```

### Konfigurasi

Buat file `.env` berdasarkan `.env.example` dan isi dengan:

- `DISCORD_TOKEN`: Token bot Discord Anda

## Demo

![Demo GIF](demo/demo.gif)

## Testing

```bash
python -m pytest tests/
```

## Struktur Project

```
FinancialBot/
├── bot.py              # Main bot file
├── core/               # Core bot logic
│   ├── __init__.py
│   ├── bot_core.py     # Bot core logic
│   ├── rules.py        # Regex rules dan reflection
│   └── database.py     # Database management
├── tests/              # Unit tests
├── logs/               # Log files
├── demo/               # Demo screenshots/GIFs
├── requirements.txt    # Dependencies
├── .env.example        # Environment template
└── README.md          # This file
```

## Perintah Bot

- `!income <jumlah> <kategori> <deskripsi>` - Catat pemasukan
- `!expense <jumlah> <kategori> <deskripsi>` - Catat pengeluaran
- `!balance` - Lihat saldo
- `!report` - Laporan keuangan
- `!help` - Bantuan

## Lisensi

MIT License
