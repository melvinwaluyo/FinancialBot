# Demo Financial Bot Discord

## Setup Discord Bot

### 1. Discord Developer Portal

```
1. Buka https://discord.com/developers/applications
2. Klik "New Application"
3. Nama: "Financial Bot"
4. Ke tab "Bot" → "Add Bot"
5. Copy Token untuk .env file
6. Enable "Message Content Intent"
```

### 2. Invite Bot ke Server

```
OAuth2 → URL Generator
Scopes: ☑️ bot
Bot Permissions: ☑️ Send Messages ☑️ Read Message History
Copy generated URL dan buka di browser
```

## Demo Interaksi Bot

### Screenshot 1: Help Command

```
User: !help
Bot: 🤖 Financial Bot - Panduan Penggunaan

**Perintah Utama:**
• !income <jumlah> <kategori> <deskripsi> - Catat pemasukan
• !expense <jumlah> <kategori> <deskripsi> - Catat pengeluaran
• !balance - Lihat saldo
• !report - Laporan keuangan
• !delete <id> - Hapus transaksi

**Cara Natural:**
• "Saya dapat gaji 5000000 dari kantor"
• "Habis 50000 untuk makanan lunch"
• "Berapa saldo saya?"
• "Lihat laporan keuangan"

**Kategori Otomatis:**
Makanan, Transport, Hiburan, Belanja, Tagihan, Kesehatan, Pendidikan, Gaji, Freelance, Investasi, dll.
```

### Screenshot 2: Income Command (Formal)

```
User: !income 5000000 gaji bonus akhir tahun
Bot: Baik! Saya telah mencatat pemasukan kamu sebesar Rp 5,000,000 untuk kategori 'gaji' dengan deskripsi 'bonus akhir tahun'.
💰 Saldo terbaru: Rp 5,000,000
```

### Screenshot 3: Income Natural Language

```
User: saya dapat freelance 1500000 dari projek website
Bot: Baik! Saya telah mencatat pemasukan kamu sebesar Rp 1,500,000 untuk kategori 'freelance' dengan deskripsi 'dari projek website'.
💰 Saldo terbaru: Rp 6,500,000
```

### Screenshot 4: Expense Command

```
User: !expense 250000 makanan groceries bulanan
Bot: Oke! Saya sudah catat pengeluaran kamu sebesar Rp 250,000 untuk kategori 'makanan' dengan deskripsi 'groceries bulanan'.
💰 Saldo terbaru: Rp 6,250,000
```

### Screenshot 5: Expense Natural Language

```
User: saya habis 75000 untuk transport bensin motor
Bot: Oke! Saya sudah catat pengeluaran kamu sebesar Rp 75,000 untuk kategori 'transport' dengan deskripsi 'bensin motor'.
💰 Saldo terbaru: Rp 6,175,000
```

### Screenshot 6: Auto-Categorization

```
User: beli makanan 45000
Bot: Oke! Saya sudah catat pengeluaran kamu sebesar Rp 45,000 untuk kategori 'makanan'.
💰 Saldo terbaru: Rp 6,130,000

User: bayar listrik 200000
Bot: Oke! Saya sudah catat pengeluaran kamu sebesar Rp 200,000 untuk kategori 'tagihan'.
💰 Saldo terbaru: Rp 5,930,000
```

### Screenshot 7: Balance Query Variations

```
User: !balance
Bot: 💰 **Ringkasan Keuangan Kamu:**
• Pemasukan: Rp 6,500,000
• Pengeluaran: Rp 570,000
• Saldo: Rp 5,930,000 (positif)

📋 **5 Transaksi Terakhir:**
1. 💸 Rp 200,000 - tagihan
2. 💸 Rp 45,000 - makanan
3. 💸 Rp 75,000 - transport (bensin motor)
4. 💸 Rp 250,000 - makanan (groceries bulanan)
5. 💚 Rp 1,500,000 - freelance (dari projek website)

User: berapa saldo saya?
Bot: [Same response as above]

User: saldo
Bot: [Same response as above]
```

### Screenshot 8: Report Generation

```
User: !report
Bot: 📊 **Laporan Keuangan per Kategori:**

💰 **Total Pemasukan**: Rp 6,500,000
💸 **Total Pengeluaran**: Rp 570,000
📈 **Saldo**: Rp 5,930,000

**📋 Breakdown per Kategori:**

**Gaji:**
  💚 Masuk: Rp 5,000,000
  📈 Net: Rp 5,000,000

**Freelance:**
  💚 Masuk: Rp 1,500,000
  📈 Net: Rp 1,500,000

**Makanan:**
  💸 Keluar: Rp 295,000
  📉 Net: Rp -295,000

**Transport:**
  💸 Keluar: Rp 75,000
  📉 Net: Rp -75,000

**Tagihan:**
  💸 Keluar: Rp 200,000
  📉 Net: Rp -200,000
```

### Screenshot 9: Stats Command (Rich Embed)

```
User: !stats
Bot: [Rich Discord Embed]
📊 Statistik Keuangan Anda

💰 Ringkasan
Pemasukan: Rp 6,500,000
Pengeluaran: Rp 570,000
Saldo: Rp 5,930,000

📈 Aktivitas
Total transaksi: 7

📋 Transaksi Terbaru
💸 Rp 200,000 - tagihan
💸 Rp 45,000 - makanan
💚 Rp 1,500,000 - freelance

Requested by UserName
Today at 2:30 PM
```

### Screenshot 10: Error Handling

```
User: !income 0 gaji
Bot: ❌ Jumlah pemasukan harus lebih dari 0.

User: hello world
Bot: Maaf, saya tidak mengerti perintah 'hello world'. Ketik `!help` untuk melihat panduan penggunaan.

User: !expense 2000000 makanan
Bot: Oke! Saya sudah catat pengeluaran kamu sebesar Rp 2,000,000 untuk kategori 'makanan'.
💰 Saldo terbaru: Rp 3,930,000
⚠️ **Perhatian**: Saldo Anda sudah negatif!
```

### Screenshot 11: Indonesian Slang Support

```
User: gue dapet 500000 projek
Bot: Baik! Saya telah mencatat pemasukan kamu sebesar Rp 500,000 untuk kategori 'freelance'.
💰 Saldo terbaru: Rp 4,430,000

User: gue abis 30000 bensin
Bot: Oke! Saya sudah catat pengeluaran kamu sebesar Rp 30,000 untuk kategori 'transport'.
💰 Saldo terbaru: Rp 4,400,000
```

### Screenshot 12: Multiple Users

```
[User A]
User A: !income 3000000 gaji
Bot: Baik! Saya telah mencatat pemasukan kamu sebesar Rp 3,000,000...
💰 Saldo terbaru: Rp 3,000,000

[User B]
User B: !balance
Bot: 📭 Anda belum memiliki transaksi apapun.

[User A]
User A: !balance
Bot: 💰 **Ringkasan Keuangan Kamu:**
• Pemasukan: Rp 3,000,000
• Pengeluaran: Rp 0
• Saldo: Rp 3,000,000 (positif)
```

## GIF Demo Scenario

### Animation Flow (10 detik)

1. **Setup** (1s): Bot online, status "watching your finances 💰"
2. **Help** (1s): User types `!help`, bot shows command list
3. **Income** (2s): User types income command, bot responds with confirmation
4. **Natural** (2s): User types natural language, bot understands and responds
5. **Balance** (2s): User checks balance, bot shows rich summary
6. **Report** (2s): User requests report, bot shows category breakdown

### Key Demo Points

- ✅ Multiple command formats (formal, natural, slang)
- ✅ Real-time balance updates
- ✅ Rich formatting with emojis
- ✅ Auto-categorization
- ✅ Error handling
- ✅ Multi-user support
- ✅ Indonesian + English support

## CLI Demo

### Terminal Output

```
🤖 Financial Bot CLI Mode
========================================
Ketik 'exit' atau 'quit' untuk keluar
Ketik '!help' untuk melihat bantuan
========================================

👤 Anda: !income 1000000 gaji
🤖 Bot: Baik! Saya telah mencatat pemasukan kamu sebesar Rp 1,000,000 untuk kategori 'gaji'.
💰 Saldo terbaru: Rp 1,000,000

👤 Anda: habis 50000 makan siang
🤖 Bot: Oke! Saya sudah catat pengeluaran kamu sebesar Rp 50,000 untuk kategori 'makanan'.
💰 Saldo terbaru: Rp 950,000

👤 Anda: saldo
🤖 Bot: 💰 **Ringkasan Keuangan Kamu:**
• Pemasukan: Rp 1,000,000
• Pengeluaran: Rp 50,000
• Saldo: Rp 950,000 (positif)

📋 **2 Transaksi Terakhir:**
1. 💸 Rp 50,000 - makanan
2. 💚 Rp 1,000,000 - gaji

👤 Anda: exit
👋 Sampai jumpa!
```
