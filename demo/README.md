# Demo Financial Bot

Folder ini berisi demo dan screenshot penggunaan Financial Bot.

## Files yang akan ditambahkan:

### Screenshots

- `setup_bot.png` - Screenshot setup bot di Discord Developer Portal
- `bot_invite.png` - Screenshot proses invite bot ke server
- `help_command.png` - Screenshot output command help
- `income_command.png` - Screenshot perintah income
- `expense_command.png` - Screenshot perintah expense
- `balance_command.png` - Screenshot perintah balance
- `report_command.png` - Screenshot laporan keuangan
- `natural_language.png` - Screenshot penggunaan bahasa natural

### GIF Demo

- `demo.gif` - GIF animasi yang menunjukkan:
  1. Perintah income dengan berbagai format
  2. Perintah expense dengan berbagai format
  3. Query balance dan report
  4. Penggunaan bahasa natural Indonesia
  5. Automatic categorization
  6. Error handling

### Video (optional)

- `full_demo.mp4` - Video demo lengkap fitur bot

## Cara Membuat Demo

1. **Setup Bot Discord**

   - Buat bot di Discord Developer Portal
   - Screenshot proses setup
   - Screenshot proses invite ke server

2. **Record Interaksi**

   - Gunakan screen recorder (OBS Studio, etc.)
   - Demonstrasi semua fitur utama
   - Tunjukkan error handling

3. **Convert ke GIF**
   - Gunakan tools seperti FFmpeg atau online converter
   - Optimasi ukuran untuk GitHub README

## Tips Demo

- Gunakan data yang realistis (angka pemasukan/pengeluaran wajar)
- Tunjukkan variasi perintah (formal dan natural language)
- Demonstrate reflection kata ganti
- Tunjukkan automatic categorization
- Include error cases dan handling

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
