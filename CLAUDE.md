# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

FinancialBot is a Discord bot for tracking income and expenses using Natural Language Processing in Indonesian (Bahasa Indonesia). The bot uses regex patterns and pronoun reflection to understand casual Indonesian conversation and provide financial tracking and analysis.

**Key Characteristics:**
- Pure Indonesian language interface (no English in user-facing responses)
- Natural language processing using regex patterns
- Reflection engine for pronoun substitution (saya↔kamu)
- Mention-only bot (only responds when @mentioned in Discord)
- SQLite database for multi-user transaction tracking
- CLI mode available for testing without Discord

## Development Commands

### Setup and Installation

```bash
# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Setup environment
copy .env.example .env
# Edit .env with your Discord Bot Token
```

### Running the Bot

```bash
# Discord mode (requires DISCORD_TOKEN in .env)
python bot.py

# CLI testing mode (no Discord token needed)
python cli_runner.py
```

### Testing

```bash
# Run all tests (79 test cases)
# Windows
run_tests.bat

# Linux/Mac
./run_tests.sh

# Or directly with pytest
python -m pytest tests/ -v --tb=short

# Run specific test file
python -m pytest tests/test_rules.py -v
python -m pytest tests/test_database.py -v
python -m pytest tests/test_integration.py -v

# Run with coverage
python -m pytest tests/ --cov=core --cov-report=html
```

**Test Coverage:** 79 test cases covering rules engine, database operations, integration flows, Indonesian language features, edge cases, and performance.

**Note:** Test runner scripts (`run_tests.bat`/`run_tests.sh`) automatically activate the virtual environment and run pytest with appropriate flags.

## Architecture

### Core Components

**3-Layer Architecture:**
1. **`bot.py`** - Discord integration layer (handles Discord events, mentions, message routing)
2. **`core/bot_core.py`** - Business logic coordinator (processes messages, orchestrates rules + database)
3. **`core/rules.py`** + **`core/database.py`** - Domain layer (NLP patterns + data persistence)

**File Structure:**
```
FinancialBot/
├── core/
│   ├── bot_core.py      # Main integration: connects rules engine + database + logging
│   ├── rules.py         # Regex patterns, reflection engine, response generation
│   └── database.py      # SQLite operations, transaction CRUD, balance calculations
├── tests/               # 79 comprehensive test cases
├── demo/                # Demo scenarios and screenshots
├── PPT/                 # Project presentation materials
├── logs/                # Auto-created log directory (.gitkeep for version control)
├── bot.py               # Discord bot entry point
├── cli_runner.py        # CLI testing interface
└── run_tests.bat/sh     # Test runner scripts
```

### Key Design Patterns

**Regex-Based NLP Engine:**
- Multiple regex patterns per command type to catch various Indonesian phrasings
- Pattern matching order is critical (stats → report → help → budget → purchase → income → expense → balance)
- Each command type has 3-5 pattern variations for natural language flexibility

**Reflection Engine:**
- Transforms pronouns in conversation: `saya`/`aku` → `kamu`, `kamu` → `saya`
- Located in `ReflectionEngine` class in `rules.py`
- Applied to user input for natural conversational responses

**Automatic Categorization:**
- `categorize_automatically()` in `rules.py` uses smart keyword matching with context awareness
- **3-tier categorization logic:**
  1. Keyword matching in description (e.g., "makan" → makanan)
  2. Amount-based inference (>1M → likely gaji)
  3. Context patterns from combined category + description
- Categories: gaji, freelance, investasi, hadiah (income); makanan, transport, hiburan, belanja, tagihan, kesehatan, pendidikan (expense)
- **Enhanced in recent commits:** Now auto-categorizes even when user provides a category (e.g., user says "kantor" → system categorizes as "gaji")
- Falls back to 'lainnya' if no keywords match

**Multi-User Isolation:**
- Each transaction stored with `user_id` (Discord user ID)
- All database queries filter by `user_id` to ensure data privacy
- No shared data between users

### Command Processing Flow

1. User mentions bot in Discord: `@FinancialBot saya dapat gaji 5000000`
2. `bot.py` detects mention, strips mention prefix, passes clean text to `bot_core.py`
3. `bot_core.process_message()` calls `rules_engine.parse_command()`
4. Rules engine returns command dict: `{'type': 'income', 'amount': 5000000, 'category': 'gaji', ...}`
5. Bot core routes to appropriate handler (`_handle_income()`, `_handle_expense()`, etc.)
6. Handler updates database and generates response using `rules_engine.generate_response()`
7. Response sent back to Discord channel

### Important Implementation Details

**Pattern Matching Order** (in `parse_command()`):
- Check about/capability/goodbye/thanks patterns FIRST (conversational)
- Check stats EARLY (before balance to avoid conflicts)
- Check report before balance (both can match similar queries)
- Check budget advice BEFORE general help (budget help should route to budget advisor)
- Check purchase planning before expense (purchase intent vs. actual expense)
- Check balance LAST (generic pattern that catches many phrases)

**Amount Parsing:**
- `parse_amount()` strips common separators (commas, periods) before converting to float
- Handles Indonesian number formats: `1.000.000` or `1000000`

**Reflection in Responses:**
- Income: "Saya telah mencatat pemasukan **kamu**..." (reflected from user's "saya")
- Always use second-person perspective when responding about user's money

**Database Isolation:**
- Each test creates temporary database
- Production uses `financial_bot.db`
- CLI mode uses `financial_bot_cli.db`

**Logging:**
- Logs stored in `logs/` directory (auto-created on startup via `os.makedirs('logs', exist_ok=True)`)
- `logs/.gitkeep` ensures directory structure is tracked in git (empty placeholder file)
- File handler: `logs/bot.log`
- Also logs to console (StreamHandler)
- Log incoming messages, transactions, and errors
- Level: INFO (configurable in bot_core.py)

## Indonesian Language Requirements

**Critical:** All user-facing responses MUST be in pure Indonesian (Bahasa Indonesia). No English words except:
- Technical terms with no Indonesian equivalent (rare)
- Brand names or proper nouns
- Markdown formatting commands

**Budget Advice Response:**
- Use simple, practical Indonesian language
- Avoid complex financial jargon
- Provide actionable recommendations in bullet points
- Use percentage-based suggestions (15% dana darurat, 30% tabungan)

**Purchase Planning Response:**
- Analyze affordability based on current balance vs. price
- Suggest alternatives (nabung dulu, cari yang lebih murah)
- Calculate months needed to save
- Provide 2-3 concrete options with pros/cons

**Response Tone:**
- Friendly and conversational (use "kamu" not "Anda")
- Supportive and non-judgmental about financial decisions
- Encouraging about good financial habits
- Clear warnings for negative balances or risky purchases

## Common Development Scenarios

### Adding New Command Patterns

1. Add regex patterns to appropriate list in `rules.py` (e.g., `self.income_patterns`)
2. Create parsing method if needed (e.g., `parse_income_command()`)
3. Add command type to `parse_command()` decision tree
4. Create handler in `bot_core.py` (e.g., `_handle_income()`)
5. Add response template in `generate_response()`
6. Write tests in `tests/test_rules.py` and `tests/test_integration.py`

### Modifying Auto-Categorization

Edit keyword dictionaries in `categorize_automatically()` in `rules.py`:
- `income_keywords`: dict of category → keyword list (e.g., 'gaji': ['gaji', 'kantor', 'kerja', 'pekerjaan'])
- `expense_keywords`: dict of category → keyword list (e.g., 'makanan': ['makan', 'nasi', 'ayam', 'restaurant', ...])
- Keywords should be common Indonesian words associated with each category

**Important:** The auto-categorization now runs on BOTH:
1. Generic categories ('uang', 'dana', 'income', 'expense', 'pemasukan', 'pengeluaran')
2. User-provided categories (checks if they match broader category keywords)

This means even if a user says "kantor", the system will recognize it belongs to "gaji" category.

### Adding New Database Fields

1. Update schema in `database.py` `init_database()`
2. Modify `add_transaction()` to accept new fields
3. Update query methods to return new fields
4. Add database migration logic if needed (currently no migration system)
5. Update tests to cover new fields

### Testing Strategy

- **Unit tests:** `test_rules.py` (patterns), `test_database.py` (DB operations)
- **Integration tests:** `test_integration.py` (end-to-end flows)
- **Edge cases:** `test_edge_cases.py` (invalid input, unicode, extremes)
- **Performance:** `test_performance.py` (response times, concurrent users)
- **Language:** `test_indonesian_features.py` (Indonesian-specific patterns)
- Always test with Indonesian input variations (formal, casual, slang)

## Discord Bot Configuration

**Required Intents:**
- `message_content` (MUST be enabled in Discord Developer Portal)
- `guilds`

**Bot Behavior:**
- Only responds when mentioned (`@FinancialBot` or `<@BOT_ID>`)
- Strips mention prefix before processing
- Sets status to "watching for mentions 👀"

**Permissions Needed:**
- Send Messages
- Read Message History
- Embed Links (for `!stats`, `!recent` commands)

## Data Model

**Transactions Table:**
- `id` (INTEGER PRIMARY KEY)
- `user_id` (TEXT) - Discord user ID as string
- `username` (TEXT) - Discord display name
- `transaction_type` (TEXT) - 'income' or 'expense'
- `amount` (REAL) - transaction amount
- `category` (TEXT) - auto-categorized or user-specified
- `description` (TEXT) - optional details
- `created_at` (TIMESTAMP) - auto-populated

**Categories Table:**
- Predefined categories (Gaji, Freelance, Makanan, Transport, etc.)
- Type field: 'income', 'expense', or 'both'

## Financial Analysis Features

**Budget Advice** (`_handle_budget_advice()`):
- Calculates 15% for emergency fund (dana darurat)
- Suggests 30% of remaining balance for savings (tabungan)
- Provides spending warnings if expense > 80% of income
- Gives actionable Indonesian advice based on expense ratio

**Purchase Planning** (`_handle_purchase_planning()`):
- Extracts item name and price from natural language
- Compares price to current balance and monthly income
- Calculates months needed to save
- Suggests cheaper alternatives for expensive items
- Provides 2-3 options with simple pros/cons in Indonesian
