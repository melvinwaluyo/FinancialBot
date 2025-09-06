# Discord Bot Setup Guide

## 1. Membuat Discord Application

### Step 1: Discord Developer Portal

1. Buka https://discord.com/developers/applications
2. Klik **"New Application"**
3. Masukkan nama: **"Financial Bot"**
4. Klik **"Create"**

### Step 2: Setup Bot

1. Di sidebar kiri, klik **"Bot"**
2. Klik **"Add Bot"** → **"Yes, do it!"**
3. Konfigurasi Bot:
   - **Username**: Financial Bot
   - **Profile Picture**: Upload logo bot (optional)

### Step 3: Bot Permissions

1. Scroll ke **"Privileged Gateway Intents"**
2. Enable **"Message Content Intent"** ✅
3. Klik **"Save Changes"**

### Step 4: Copy Token

1. Di section **"Token"**
2. Klik **"Copy"** untuk copy bot token
3. **JANGAN BAGIKAN TOKEN INI KEPADA SIAPAPUN!**

## 2. Setup Environment

### Step 1: Clone Project

```bash
git clone <repository-url>
cd FinancialBot
```

### Step 2: Install Dependencies

```bash
# Windows
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Step 3: Configure Environment

```bash
# Copy template
copy .env.example .env

# Edit .env file
notepad .env
```

Isi file `.env`:

```env
DISCORD_TOKEN=your_bot_token_here
DATABASE_PATH=financial_bot.db
LOG_LEVEL=INFO
LOG_FILE=logs/bot.log
```

## 3. Invite Bot ke Server

### Step 1: Generate Invite URL

1. Di Discord Developer Portal, pilih aplikasi Anda
2. Klik **"OAuth2"** → **"URL Generator"**
3. **Scopes**: ✅ `bot`
4. **Bot Permissions**:
   - ✅ Send Messages
   - ✅ Read Message History
   - ✅ Use Slash Commands
   - ✅ Embed Links
   - ✅ Read Messages
5. Copy **Generated URL**

### Step 2: Invite Bot

1. Buka URL yang di-generate di browser
2. Pilih server Discord Anda
3. Klik **"Authorize"**
4. Complete CAPTCHA jika diminta

## 4. Menjalankan Bot

### Development Mode (CLI Testing)

```bash
python cli_runner.py
```

### Production Mode (Discord)

```bash
python bot.py
```

### Running Tests

```bash
# Windows
run_tests.bat

# Linux/Mac
chmod +x run_tests.sh
./run_tests.sh
```

## 5. Verifikasi Setup

### Test 1: Bot Online

- Bot harus muncul **online** di server Discord
- Status: **"watching your finances 💰"**

### Test 2: Basic Commands

```
!help          # Harus menampilkan panduan
!ping          # Harus response "Pong!"
!categories    # Harus menampilkan daftar kategori
```

### Test 3: Core Functionality

```
!income 100000 gaji testing
!expense 50000 makanan lunch
!balance
!report
```

## 6. Troubleshooting

### Bot Tidak Online

- ✅ Check token di `.env` file
- ✅ Pastikan "Message Content Intent" enabled
- ✅ Check internet connection
- ✅ Lihat error di terminal/console

### Bot Tidak Respond

- ✅ Check bot permissions di server
- ✅ Pastikan bot bisa send messages di channel
- ✅ Check logs di `logs/bot.log`

### Import Errors

- ✅ Virtual environment aktif
- ✅ Dependencies terinstall: `pip list`
- ✅ Python version 3.8+

### Database Errors

- ✅ Check file permissions
- ✅ Pastikan folder `logs/` exists
- ✅ SQLite installed

## 7. Production Deployment

### Hosting Options

1. **VPS** (DigitalOcean, Linode, AWS EC2)
2. **Heroku** (Free tier available)
3. **Railway** (Easy deployment)
4. **PythonAnywhere** (Python-specific hosting)

### Environment Variables

```env
DISCORD_TOKEN=your_production_token
DATABASE_PATH=/app/financial_bot.db
LOG_LEVEL=WARNING
LOG_FILE=/app/logs/bot.log
```

### Process Management

```bash
# Using screen
screen -S financial-bot
python bot.py
# Ctrl+A+D to detach

# Using systemd (Linux)
sudo systemctl enable financial-bot
sudo systemctl start financial-bot
```

## 8. Advanced Configuration

### Custom Categories

Edit `core/database.py` untuk menambah kategori default:

```python
default_categories = [
    ('CustomCategory', 'both'),
    # Add more categories
]
```

### Custom Patterns

Edit `core/rules.py` untuk menambah pattern regex:

```python
self.income_patterns.append(r'your_custom_pattern')
```

### Logging Configuration

Edit logging level di `core/bot_core.py`:

```python
logging.basicConfig(level=logging.DEBUG)  # More verbose
```
