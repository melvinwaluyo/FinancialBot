"""
Rules engine dengan regex dan reflection kata ganti untuk Financial Bot
Menangani parsing perintah dan respons yang natural dalam bahasa Indonesia
"""

import re
from typing import Dict, List, Tuple, Optional, Any
from datetime import datetime

class ReflectionEngine:
    """Engine untuk reflection kata ganti dan transformasi kalimat"""
    
    def __init__(self):
        # Mapping kata ganti subjek ke objek
        self.pronoun_reflections = {
            'saya': 'kamu',
            'aku': 'kamu', 
            'kamu': 'saya',
            'anda': 'saya'
        }
        
        # Mapping untuk kata kerja
        self.verb_reflections = {
            'punya': 'punya',
            'adalah': 'adalah',
            'ingin': 'ingin',
            'mau': 'mau',
            'bisa': 'bisa',
            'akan': 'akan',
            'sudah': 'sudah',
            'belum': 'belum'
        }
    
    def reflect_text(self, text: str) -> str:
        """Reflect text dengan mengganti kata ganti dan kata kerja"""
        words = text.lower().split()
        reflected_words = []
        
        for word in words:
            # Cari reflection untuk kata ganti
            if word in self.pronoun_reflections:
                reflected_words.append(self.pronoun_reflections[word])
            elif word in self.verb_reflections:
                reflected_words.append(self.verb_reflections[word])
            else:
                reflected_words.append(word)
        
        return ' '.join(reflected_words)

class FinancialRulesEngine:
    """Engine utama untuk parsing perintah finansial menggunakan regex"""
    
    def __init__(self):
        self.reflection_engine = ReflectionEngine()
        self.setup_patterns()
    
    def setup_patterns(self):
        """Setup regex patterns untuk berbagai perintah"""
        
        # Pattern untuk pemasukan - hanya bahasa Indonesia
        self.income_patterns = [
            # Pattern: !income 100000 gaji bonus bulan ini
            r'!income\s+(\d+(?:\.\d+)?)\s+(\w+)(?:\s+(.+))?',
            # Pattern natural: saya dapat gaji 5000000 dari kantor
            r'(?:saya|aku)\s+(?:dapat|terima|dapet|menerima|meraih|peroleh)\s+(\w+)\s+(\d+(?:\.\d+)?)\s*(?:dari\s+(.+))?',
            # Pattern: dapat 50000 dari ortu (FIXED: swap amount and category order)
            r'(?:dapat|terima|dapet|menerima|meraih|peroleh)\s+(\d+(?:\.\d+)?)\s+(?:dari\s+)?(\w+)(?:\s+(.+))?',
            # Pattern: income 1000000 kategori deskripsi
            r'(?:income|pemasukan|masuk)\s+(\d+(?:\.\d+)?)\s+(\w+)(?:\s+(.+))?'
        ]
        
        # Pattern untuk pengeluaran - hanya bahasa Indonesia
        self.expense_patterns = [
            # Pattern: !expense 50000 makanan makan siang
            r'!expense\s+(\d+(?:\.\d+)?)\s+(\w+)(?:\s+(.+))?',
            # Pattern natural: saya habis 50000 untuk makanan
            r'(?:saya|aku)\s+(?:habis|abis|keluar|bayar|beli|menghabiskan|mengeluarkan|belanja|pakai|gunakan)\s+(\d+(?:\.\d+)?)\s+(?:untuk\s+)?(\w+)(?:\s+(.+))?',
            # Pattern: keluar 75000 transport
            r'(?:keluar|habis|abis|bayar|beli|expense|pengeluaran|menghabiskan|mengeluarkan|belanja|pakai|gunakan)\s+(\d+(?:\.\d+)?)\s+(?:untuk\s+)?(\w+)(?:\s+(.+))?',
            # Pattern: beli makanan 25000
            r'(?:beli|bayar|belanja)\s+(\w+)\s+(\d+(?:\.\d+)?)(?:\s+(.+))?'
        ]
        
        # Pattern untuk saldo
        self.balance_patterns = [
            r'^!balance$',
            r'^(?:saldo|balance)(?:\s+(?:saya|aku))?$',
            r'^(?:cek|lihat|check)\s+(?:saldo|balance|uang)$',
            r'^(?:berapa)\s+(?:saldo|uang)(?:\s+(?:saya|aku))?$',
            r'^(?:saya|aku)\s+(?:punya|ada)\s+(?:berapa)$'
        ]
        
        # Pattern untuk laporan
        self.report_patterns = [
            r'^!report$',
            r'^(?:laporan|report)$',
            r'^(?:lihat|show|cek)\s+(?:laporan|report)$',
            r'^(?:ringkasan|summary)\s+(?:keuangan|finansial)$',
            r'^summary\s+keuangan$',
            r'^(?:laporan|report)\s+(?:keuangan|finansial)$'
        ]
        
        # Pattern untuk bantuan - More specific to avoid conflicts
        self.help_patterns = [
            r'^!help$',
            r'^(?:help|bantuan)$',
            r'^(?:help me)$',
            r'^(?:bantuan dong)$',
            r'(?:gimana|bagaimana)\s+(?:cara)$',
            r'(?:gimana|bagaimana)\s+(?:cara)\s+(?:pakai|gunakan)',
            r'^(?:apa)\s+(?:perintah|command)',
            r'^(?:help|bantuan)\s+(?:dong|please|pls)$'
        ]
        
        # Pattern untuk hapus transaksi
        self.delete_patterns = [
            r'!delete\s+(\d+)',
            r'(?:hapus|delete|remove)\s+(?:transaksi\s+)?(\d+)',
            r'(?:batalkan|cancel)\s+(?:transaksi\s+)?(\d+)'
        ]
        
        # Pattern untuk pertanyaan umum tentang bot
        self.about_patterns = [
            r'(?:siapa)\s+(?:kamu|bot)',
            r'(?:apa)\s+(?:nama)\s+(?:kamu)',
            r'(?:kamu)\s+(?:siapa)',
            r'(?:perkenalkan)\s+(?:diri)',
            r'^(?:hai|hello|hi|halo)$',
            r'^(?:apa kabar)$'
        ]
        
        # Pattern untuk pertanyaan kemampuan bot
        self.capability_patterns = [
            r'(?:apa)\s+(?:yang bisa|bisa kamu)',
            r'(?:kamu)\s+(?:bisa)\s+(?:apa)',
            r'(?:fungsi|fitur)\s+(?:apa)',
            r'(?:kemampuan)\s+(?:kamu)',
            r'(?:untuk apa)\s+(?:kamu)'
        ]
        
        # Pattern untuk ucapan terima kasih
        self.thanks_patterns = [
            r'(?:terima kasih|makasih)',
            r'(?:bagus|mantap|keren)',
            r'(?:hebat|bagus sekali)'
        ]
        
        # Pattern untuk salam perpisahan
        self.goodbye_patterns = [
            r'^(?:bye|goodbye|sampai jumpa|dadah|selamat tinggal)$',
            r'^(?:sampai nanti)$',
            r'bye\s*$',
            r'goodbye\s*$'
        ]
        
        # Pattern untuk budgeting advice - Indonesian & English
        self.budget_patterns = [
            # Indonesian patterns
            r'(?:bantuan|buatkan|buat)\s+(?:saya|aku)?\s*(?:buat|bikin)?\s+(?:anggaran|budget)',
            r'(?:saya|aku)\s+(?:mau|ingin|butuh|perlu)\s+(?:anggaran|budget|bantuan anggaran|budget advice)',
            r'(?:gimana|bagaimana)\s+(?:cara|bikin|buat)\s+(?:anggaran|budget)',
            r'(?:tolong|bantuan)\s+(?:anggaran|budget)',
            r'(?:analisis|analisa|cek)\s+(?:anggaran|budget)\s+(?:saya|aku)',
            r'(?:anggaran|budget)\s+(?:saran|rekomendasi)',
            r'(?:buat|bikin|buatkan)\s+(?:anggaran|budget)',
            r'(?:bantuan)\s+(?:anggaran|budget)',
            r'(?:saran|rekomendasi)\s+(?:anggaran|budget)',
            r'(?:konsultasi)\s+(?:anggaran|keuangan|budget)',
            # English patterns
            r'(?:help|create|make).*(?:budget)',
            r'(?:budget).*(?:help|advice|recommendation|create)',
            r'(?:i|I)\s+(?:need|want|require)\s+(?:a\s+)?(?:budget)',
            r'(?:how to|how)\s+(?:create|make)\s+(?:a\s+)?(?:budget)',
            r'(?:budget).*(?:planning|advice)',
            r'(?:financial).*(?:advice|planning)',
            r'(?:help me create a budget)'
        ]
        
        # Pattern untuk purchasing planning - Indonesian & English  
        self.purchase_patterns = [
            # Indonesian patterns
            r'(?:saya|aku)\s+(?:mau|ingin|pengen)\s+(?:beli)\s+(.+?)(?:\s+(?:harga|seharga)?\s*(\d+(?:,?\d+)*))?',
            r'(?:mau|ingin|pengen)\s+(?:beli)\s+(.+?)(?:\s+(?:Rp)?\s*(\d+(?:,?\d+)*))?',
            r'(?:rencana)\s+(?:beli|membeli)\s+(.+?)(?:\s+(?:Rp)?\s*(\d+(?:,?\d+)*))?',
            r'(?:analisis|analisa)\s+(?:beli)\s+(.+?)(?:\s+(?:Rp)?\s*(\d+(?:,?\d+)*))?',
            r'(?:konsultasi)\s+(?:beli|pembelian)\s+(.+?)(?:\s+(?:Rp)?\s*(\d+(?:,?\d+)*))?',
            # English patterns
            r'(?:i|I)\s+(?:want to|wanna)\s+(?:buy)\s+(?:a\s+)?(.+?)(?:\s+(?:for|at|price)?\s*(\d+(?:,?\d+)*))?',
            r'(?:buying|purchase)\s+(?:a\s+)?(.+?)(?:\s+(?:for|at|price)?\s*(\d+(?:,?\d+)*))?',
            r'(?:planning to buy)\s+(?:a\s+)?(.+?)(?:\s+(?:for|at|price)?\s*(\d+(?:,?\d+)*))?',
            r'(?:can i buy)\s+(?:a\s+)?(.+?)(?:\s+(?:for|at|price)?\s*(\d+(?:,?\d+)*))?'
        ]
        
        self.stats_patterns = [
            r'^\s*!stats\s*$',
            r'\bstatistik\b',
            r'\bstat\b'
        ]
    
    def parse_amount(self, amount_str: str) -> float:
        """Parse string jumlah menjadi float"""
        try:
            # Remove common separators
            cleaned = re.sub(r'[.,]', '', amount_str.replace(',', ''))
            return float(cleaned)
        except ValueError:
            return 0.0
    
    def categorize_automatically(self, description: str, amount: float) -> str:
        """Kategorisasi otomatis berdasarkan deskripsi dan jumlah"""
        description_lower = description.lower()
        
        # Smart categorization berdasarkan:
        # 1. Keywords dalam deskripsi
        # 2. Jumlah transaksi (>1M = kemungkinan gaji)
        # 3. Context patterns (waktu, lokasi, dll)
        income_keywords = {
            'gaji': ['gaji', 'kantor', 'kerja', 'pekerjaan'],
            'freelance': ['freelance', 'projek', 'kontrak', 'lepas', 'sampingan'],
            'investasi': ['saham', 'reksadana', 'dividen', 'profit', 'trading', 'investasi'],
            'hadiah': ['hadiah', 'bonus', 'reward', 'kado', 'pemberian']
        }
        
        expense_keywords = {
            'makanan': ['makan', 'nasi', 'ayam', 'restaurant', 'cafe', 'snack', 'lapar', 'kenyang', 'minuman'],
            'transport': ['transport', 'bensin', 'ojek', 'taksi', 'bus', 'kereta', 'grab', 'gojek', 'motor', 'mobil'],
            'hiburan': ['film', 'game', 'spotify', 'netflix', 'youtube', 'concert', 'musik', 'hiburan'],
            'belanja': ['beli', 'shopping', 'baju', 'sepatu', 'elektronik', 'gadget', 'belanja', 'mall', 'toko'],
            'tagihan': ['listrik', 'air', 'internet', 'wifi', 'telepon', 'cicilan', 'bayar', 'tagihan'],
            'kesehatan': ['dokter', 'obat', 'hospital', 'rumah sakit', 'vitamin', 'therapy', 'clinic'],
            'pendidikan': ['kursus', 'buku', 'sekolah', 'kuliah', 'training', 'seminar', 'workshop']
        }
        
        # Check income keywords
        for category, keywords in income_keywords.items():
            if any(keyword in description_lower for keyword in keywords):
                return category
        
        # Check expense keywords  
        for category, keywords in expense_keywords.items():
            if any(keyword in description_lower for keyword in keywords):
                return category
        
        # Default based on amount
        if amount > 1000000:  # > 1 juta, likely income
            return 'gaji'
        else:
            return 'lainnya'
    
    def match_pattern(self, text, patterns):
        """Match pattern and return the match object"""
        import re
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match
        return None
    
    def parse_income_command(self, text: str) -> Optional[Dict[str, Any]]:
        """Parse perintah pemasukan"""
        match = self.match_pattern(text, self.income_patterns)
        if not match:
            return None
        
        groups = match.groups()
        
        # Handle different pattern orders
        if text.lower().startswith(('saya', 'aku')):
            # Natural language: saya dapat freelance 1000000 dari projek
            category = groups[0].lower()
            amount = self.parse_amount(groups[1])
            description = groups[2] if len(groups) > 2 and groups[2] else ""
        elif text.lower().startswith(('dapat', 'terima', 'dapet', 'menerima', 'meraih', 'peroleh')) and not text.lower().startswith('!'):
            # Pattern: dapat 50000 dari ortu (amount first, then category)
            amount = self.parse_amount(groups[0])
            # Check if "dari" is in the text to extract category correctly
            if 'dari' in text.lower():
                # Extract category from the "dari X" part
                dari_match = re.search(r'dari\s+(\w+)', text.lower())
                if dari_match:
                    category = dari_match.group(1)
                    description = ""
                else:
                    category = groups[1].lower() if len(groups) >= 2 and groups[1] else "lainnya"
                    description = groups[2] if len(groups) > 2 and groups[2] else ""
            else:
                category = groups[1].lower() if len(groups) >= 2 and groups[1] else "lainnya"
                description = groups[2] if len(groups) > 2 and groups[2] else ""
        else:
            # Standard: amount category description
            amount = self.parse_amount(groups[0])
            category = groups[1].lower() if len(groups) >= 2 and groups[1] else "lainnya"
            description = groups[2] if len(groups) > 2 and groups[2] else ""
        
        # Auto-categorize if category is generic
        if category in ['uang', 'dana', 'income', 'pemasukan']:
            category = self.categorize_automatically(description, amount)
        else:
            # Check if the current category should be auto-categorized to a broader category
            auto_category = self.categorize_automatically(category + " " + description, amount)
            if auto_category != 'lainnya':  # If auto-categorization found a match
                category = auto_category
        
        return {
            'type': 'income',
            'amount': amount,
            'category': category,
            'description': description.strip()
        }
    
    def parse_expense_command(self, text: str) -> Optional[Dict[str, Any]]:
        """Parse perintah pengeluaran"""
        match = self.match_pattern(text, self.expense_patterns)
        if not match:
            return None
        
        groups = match.groups()
        
        # Handle different pattern structures
        if text.startswith(('beli', 'bayar', 'belanja')) and len(groups) >= 2:
            # Pattern: beli makanan 25000
            category = groups[0].lower()
            amount = self.parse_amount(groups[1])
            description = groups[2] if len(groups) > 2 and groups[2] else ""
        else:
            # Standard pattern: amount category description
            amount = self.parse_amount(groups[0])
            category = groups[1].lower() if len(groups) >= 2 and groups[1] else "lainnya"
            description = groups[2] if len(groups) > 2 and groups[2] else ""
        
        # Auto-categorize if category is generic OR if category matches keywords
        if category in ['uang', 'dana', 'expense', 'pengeluaran']:
            category = self.categorize_automatically(description, amount)
        else:
            # Check if the current category should be auto-categorized to a broader category
            auto_category = self.categorize_automatically(category + " " + description, amount)
            if auto_category != 'lainnya':  # If auto-categorization found a match
                category = auto_category
        
        return {
            'type': 'expense',
            'amount': amount,
            'category': category,
            'description': description.strip()
        }
    
    def parse_delete_command(self, text: str) -> Optional[Dict[str, Any]]:
        """Parse perintah hapus transaksi"""
        match = self.match_pattern(text, self.delete_patterns)
        if not match:
            return None
        
        transaction_id = int(match.group(1))
        return {
            'type': 'delete',
            'transaction_id': transaction_id
        }
    
    def parse_budget_command(self, text: str) -> Optional[Dict[str, Any]]:
        """Parse perintah budget advice"""
        match = self.match_pattern(text, self.budget_patterns)
        if not match:
            return None
        
        return {
            'type': 'budget_advice',
            'original_text': text
        }
    
    def parse_purchase_command(self, text: str) -> Optional[Dict[str, Any]]:
        """Parse perintah purchase planning"""
        match = self.match_pattern(text, self.purchase_patterns)
        if not match:
            return None
        
        groups = match.groups()
        
        # Extract item name and price
        item = ""
        price = 0.0
        
        if groups[0]:
            item = groups[0].strip()
        
        # Look for price in the original text using a more flexible approach
        # Try to find all numbers and use the largest one as the price
        price_matches = re.findall(r'(\d+(?:,?\d+)*)', text)
        if price_matches:
            try:
                # Convert all matches to numbers and pick the largest
                numbers = []
                for match in price_matches:
                    numbers.append(float(match.replace(',', '')))
                price = max(numbers)
            except ValueError:
                price = 0.0
        
        # If groups has a second element, try to use it as price (override auto-detection)
        if len(groups) > 1 and groups[1]:
            try:
                price_str = groups[1].replace(',', '')
                price = float(price_str)
            except ValueError:
                pass
        
        # Clean up item name - remove common words that might be captured
        if item:
            # Remove leading/trailing articles and clean up
            item = re.sub(r'^(a|an|the)\s+', '', item, flags=re.IGNORECASE)
            item = re.sub(r'\s+(harga|seharga|price|for|at|dengan)\s*$', '', item, flags=re.IGNORECASE)
            # Remove numbers from the item name if they appear to be the price
            if price > 0:
                item = re.sub(r'\s*\d+(?:,?\d+)*\s*', ' ', item)
            item = item.strip()
            
            # Fix common extraction issues
            if len(item) <= 2:  # If only 1-2 characters, likely extraction error
                # Try to extract from the original text more carefully
                words = text.lower().split()
                purchase_words = ['buy', 'beli', 'purchase']
                for i, word in enumerate(words):
                    if word in purchase_words and i + 1 < len(words):
                        next_word = words[i + 1]
                        if next_word not in ['a', 'an', 'the'] and not next_word.isdigit():
                            item = next_word
                        elif i + 2 < len(words) and not words[i + 2].isdigit():
                            item = words[i + 2]
                        break
        
        if not item or len(item) <= 1:
            item = "item"
        
        return {
            'type': 'purchase_planning',
            'item': item,
            'price': price,
            'original_text': text
        }
    
    def parse_command(self, text: str) -> Dict[str, Any]:
        """Parse perintah utama"""
        text = text.strip()
        
        # Check about bot questions FIRST
        if self.match_pattern(text, self.about_patterns):
            return {'type': 'about'}
        
        # Check capability questions
        if self.match_pattern(text, self.capability_patterns):
            return {'type': 'capability'}
        
        # Check goodbye BEFORE thanks to avoid conflict
        if self.match_pattern(text, self.goodbye_patterns):
            return {'type': 'goodbye'}
        
        # Check thanks
        if self.match_pattern(text, self.thanks_patterns):
            return {'type': 'thanks'}
        
        # Check stats command EARLY (before other patterns)
        if self.match_pattern(text, self.stats_patterns):
            return {'type': 'stats'}
        
        # Check report FIRST (before balance to prevent conflicts)
        if self.match_pattern(text, self.report_patterns):
            return {'type': 'report'}
        
        # Check help first but with more specific patterns
        if self.match_pattern(text, self.help_patterns) and not any(keyword in text.lower() for keyword in ['budget', 'anggaran', 'create', 'buat']):
            return {'type': 'help'}
        
        # Check budget advice BEFORE help to catch budget-related help requests
        budget_result = self.parse_budget_command(text)
        if budget_result:
            return budget_result
        
        # Check help after budget check
        if self.match_pattern(text, self.help_patterns):
            return {'type': 'help'}
        
        # Check delete
        delete_result = self.parse_delete_command(text)
        if delete_result:
            return delete_result
        
        # Check purchase planning before expense to catch purchase intents
        purchase_result = self.parse_purchase_command(text)
        if purchase_result:
            return purchase_result
        
        # Check income
        income_result = self.parse_income_command(text)
        if income_result:
            return income_result
        
        # Check expense
        expense_result = self.parse_expense_command(text)
        if expense_result:
            return expense_result
        
        # Check balance LAST (to avoid conflicts with other patterns)
        if self.match_pattern(text, self.balance_patterns):
            return {'type': 'balance'}
        
        # Unknown command
        return {'type': 'unknown', 'original_text': text}
    
    def generate_response(self, command_result: Dict[str, Any], user_data: Dict[str, Any] = None) -> str:
        """Generate response dengan reflection"""
        command_type = command_result.get('type')
        
        if command_type == 'about':
            return ("👋 Hai! Saya adalah **Financial Bot**, asisten keuangan pintar untuk Discord!\n\n"
                   "🤖 **Tentang Saya:**\n"
                   "• Nama: Financial Bot\n"
                   "• Fungsi: Membantu melacak pemasukan dan pengeluaran\n"
                   "• Bahasa: Indonesia\n"
                   "• Dibuat dengan: Python \n\n"
                   "💡 Saya bisa memahami bahasa natural Indonesia, jadi kamu bisa bicara santai denganku!\n"
                   "Ketik `!help` untuk melihat semua yang bisa saya lakukan.")
        
        elif command_type == 'capability':
            return ("🚀 **Kemampuan Saya:**\n\n"
                   "💰 **Manajemen Keuangan:**\n"
                   "• Catat pemasukan dan pengeluaran\n"
                   "• Hitung saldo otomatis\n"
                   "• Buat laporan keuangan\n"
                   "• Kategorisasi transaksi otomatis\n\n"
                   "📊 **Analisis Keuangan:**\n"
                   "• Saran anggaran bulanan yang sederhana\n"
                   "• Analisis rencana pembelian barang\n"
                   "• Rekomendasi pengelolaan uang\n"
                   "• Bantuan perencanaan keuangan\n\n"
                   "🧠 **Kecerdasan:**\n"
                   "• Mengerti bahasa natural Indonesia\n"
                   "• Deteksi kategori otomatis dari deskripsi\n"
                   "• Percakapan yang natural dan santai\n"
                   "• Rekomendasi keuangan yang praktis\n\n"
                   "📊 **Fitur Lain:**\n"
                   "• Dukungan multi-user\n"
                   "• Tracking saldo real-time\n"
                   "• Format cantik dengan emoji\n"
                   "• Penanganan error yang informatif\n\n"
                   "Ketik `!help` untuk panduan lengkap!")
        
        elif command_type == 'thanks':
            return ("😊 Sama-sama! Senang bisa membantu kamu mengelola keuangan.\n\n"
                   "💪 Terus semangat mengatur keuangannya ya! Kalau ada yang mau ditanyakan atau dicatat lagi, "
                   "langsung saja bilang ke saya.\n\n"
                   "💡 **Pro tip**: Rutin catat transaksi harian untuk kontrol keuangan yang lebih baik!")
        
        elif command_type == 'goodbye':
            return ("👋 Sampai jumpa! Semoga keuangannya selalu terkontrol dengan baik.\n\n"
                   "💰 Jangan lupa terus catat pemasukan dan pengeluarannya ya!\n"
                   "🔔 Saya akan selalu siap membantu kapan saja kamu butuh.")
        
        elif command_type == 'income':
            amount = command_result['amount']
            category = command_result['category']
            response = f"Baik! Saya telah mencatat pemasukan kamu sebesar Rp {amount:,.0f} untuk kategori '{category}'"
            if command_result.get('description'):
                response += f" dengan deskripsi '{command_result['description']}'"
            return response + "."
        
        elif command_type == 'expense':
            amount = command_result['amount']
            category = command_result['category']
            response = f"Oke! Saya sudah catat pengeluaran kamu sebesar Rp {amount:,.0f} untuk kategori '{category}'"
            if command_result.get('description'):
                response += f" dengan deskripsi '{command_result['description']}'"
            return response + "."
        
        elif command_type == 'balance':
            if user_data:
                balance_info = user_data.get('balance', {})
                income = balance_info.get('income', 0)
                expense = balance_info.get('expense', 0)
                balance = balance_info.get('balance', 0)
                
                status = "positif" if balance >= 0 else "negatif"
                return (f"💰 **Ringkasan Keuangan Kamu:**\n"
                       f"• Pemasukan: Rp {income:,.0f}\n"
                       f"• Pengeluaran: Rp {expense:,.0f}\n"
                       f"• Saldo: Rp {balance:,.0f} ({status})")
            else:
                return "📭 Anda belum memiliki transaksi apapun."
        
        elif command_type == 'report':
            return "📊 Laporan keuangan kamu sedang disiapkan..."
        
        elif command_type == 'help':
            return ("""🤖 **Financial Bot - Panduan Penggunaan**

**❗ PENTING:** Mention bot (@FinancialBot) untuk menggunakan semua fitur!

**Perintah Utama:**
• `@FinancialBot !income <jumlah> <kategori> <deskripsi>` - Catat pemasukan
• `@FinancialBot !expense <jumlah> <kategori> <deskripsi>` - Catat pengeluaran  
• `@FinancialBot !balance` - Lihat saldo
• `@FinancialBot !report` - Laporan keuangan
• `@FinancialBot !delete <id>` - Hapus transaksi

**Fitur Analisis Keuangan:**
• `@FinancialBot bantuan anggaran` - Saran anggaran bulanan
• `@FinancialBot saya mau beli mobil 50000000` - Analisis rencana pembelian

**Cara Natural:**
• "@FinancialBot Saya dapat gaji 5000000 dari kantor"
• "@FinancialBot Habis 50000 untuk makanan lunch"
• "@FinancialBot Berapa saldo saya?"
• "@FinancialBot Buatkan anggaran saya"
• "@FinancialBot Saya mau beli laptop 15000000"

**Pertanyaan Umum:**
• "@FinancialBot Siapa kamu?" - Kenalan dengan bot
• "@FinancialBot Apa yang bisa kamu lakukan?" - Lihat kemampuan

**Kategori Otomatis:**
Makanan, Transport, Hiburan, Belanja, Tagihan, Kesehatan, Pendidikan, Gaji, Freelance, Investasi, dll.""")
        
        elif command_type == 'delete':
            return f"Transaksi dengan ID {command_result['transaction_id']} telah dihapus."
        
        elif command_type == 'budget_advice':
            return self._generate_budget_advice_response(user_data)
        
        elif command_type == 'purchase_planning':
            return self._generate_purchase_planning_response(command_result, user_data)
        
        elif command_type == 'unknown':
            original = command_result.get('original_text', '')
            reflected = self.reflection_engine.reflect_text(original)
            return (f"Maaf, saya tidak mengerti perintah '{original}'. "
                   f"Ketik `!help` untuk melihat panduan penggunaan.\n\n"
                   f"💡 **Atau coba tanyakan:**\n"
                   f"• \"Siapa kamu?\" - Untuk berkenalan\n"
                   f"• \"Apa yang bisa kamu lakukan?\" - Untuk melihat kemampuan saya")
        
        return "Perintah tidak dikenali. Ketik `!help` untuk bantuan."
    
    def _generate_budget_advice_response(self, user_data: Dict[str, Any] = None) -> str:
        """Generate budget advice response based on user's financial data - Pure Indonesian"""
        if not user_data or not user_data.get('balance'):
            return ("📊 **Saran Anggaran**\n\n"
                   "Untuk memberikan saran anggaran yang tepat, saya perlu data keuangan kamu dulu.\n\n"
                   "💡 **Mulai dengan:**\n"
                   "• Catat pemasukan bulanan kamu\n"
                   "• Catat pengeluaran rutin kamu\n"
                   "• Lalu minta saran anggaran lagi\n\n"
                   "**Contoh**: \"Saya dapat gaji 6250000 dari kantor\"")
        
        balance_info = user_data.get('balance', {})
        income = balance_info.get('income', 0)
        expense = balance_info.get('expense', 0)
        balance = balance_info.get('balance', 0)
        
        if income == 0:
            return ("📊 **Saran Anggaran**\n\n"
                   "Saya belum melihat pemasukan kamu. Untuk membuat anggaran yang baik, "
                   "tolong catat pemasukan bulanan kamu dulu.\n\n"
                   "**Contoh**: \"Saya dapat gaji 6250000 dari kantor\"")
        
        # Calculate simple percentages
        expense_percentage = (expense / income * 100) if income > 0 else 0
        available = balance
        
        dana_darurat = income * 0.15  # 15% untuk dana darurat
        tabungan = available * 0.30 if available > 0 else 0  # 30% dari sisa untuk tabungan
        sisanya = max(0, available - dana_darurat - tabungan)
        
        # Generate simple response in Indonesian
        response = f"💰 **Ringkasan Keuangan Bulanan**:\n"
        response += f"• **Pemasukan**: Rp {income:,.0f}\n"
        response += f"• **Pengeluaran**: Rp {expense:,.0f}\n"
        response += f"• **Sisa**: Rp {available:,.0f}\n\n"
        
        response += f"📊 **Saran Penggunaan Sisa Uang**:\n"
        response += f"• **Dana Darurat**: Rp {dana_darurat:,.0f} (15% dari gaji)\n"
        response += f"• **Tabungan**: Rp {tabungan:,.0f} (30% dari sisa)\n"
        response += f"• **Sisanya untuk Kamu**: Rp {sisanya:,.0f}\n\n"
        
        # Simple advice based on expense ratio
        if expense_percentage > 80:
            response += "⚠️ **Perhatian**: Pengeluaran kamu sudah {:.0f}% dari gaji. Coba kurangi pengeluaran yang tidak perlu.\n\n".format(expense_percentage)
        elif expense_percentage > 60:
            response += "✅ **Lumayan Baik**: Pengeluaran kamu {:.0f}% dari gaji. Sisanya bisa ditabung atau investasi.\n\n".format(expense_percentage)
        else:
            response += "👍 **Bagus Sekali**: Pengeluaran kamu cuma {:.0f}% dari gaji. Kamu bisa nabung banyak!\n\n".format(expense_percentage)
        
        # Simple actionable tips
        response += "💡 **Yang Harus Dilakukan**:\n"
        if available > 0:
            response += "• Sisihkan dana darurat dulu (target 6 bulan pengeluaran)\n"
            response += "• Tabung sisanya secara rutin\n" 
            response += "• Kalau udah cukup, coba investasi\n"
        else:
            response += "• Catat semua pengeluaran selama sebulan\n"
            response += "• Cari pengeluaran yang bisa dikurangi\n"
            response += "• Coba cari tambahan pendapatan\n"
        
        return response
    
    def _generate_purchase_planning_response(self, command_result: Dict[str, Any], user_data: Dict[str, Any] = None) -> str:
        """Generate purchase planning response - Pure Indonesian & Simple"""
        item = command_result.get('item', 'barang')
        price = command_result.get('price', 0)
        
        if not user_data or not user_data.get('balance'):
            return (f"🛍️ **Analisis Pembelian: {item.title()}**\n\n"
                   f"**Harga**: Rp {price:,.0f}\n\n"
                   "Untuk memberikan analisis yang tepat, saya perlu data keuangan kamu.\n\n"
                   "💡 **Catat dulu:**\n"
                   "• Pemasukan bulanan kamu\n"
                   "• Pengeluaran rutin kamu\n\n"
                   "Lalu tanyakan lagi tentang rencana beli ini!")
        
        balance_info = user_data.get('balance', {})
        income = balance_info.get('income', 0)
        expense = balance_info.get('expense', 0)
        current_balance = balance_info.get('balance', 0)
        
        response = f"🛍️ **Analisis Beli {item.title()}**:\n\n"
        response += f"**Harga Barang**: Rp {price:,.0f}\n"
        response += f"**Gaji Bulanan**: Rp {income:,.0f}\n"
        response += f"**Saldo Sekarang**: Rp {current_balance:,.0f}\n\n"
        
        # Simple affordability check
        can_afford_now = current_balance >= price
        months_salary = (price / income) if income > 0 else 0
        
        # Simple analysis
        if can_afford_now:
            response += "✅ **Kabar Baik**: Kamu bisa beli sekarang!\n\n"
        else:
            kurang = price - current_balance
            response += f"⚠️ **Kurang Dana**: Masih kurang Rp {kurang:,.0f}\n\n"
        
        # Simple options
        response += "💡 **Pilihan untuk Kamu**:\n\n"
        
        if can_afford_now:
            response += "**Pilihan 1**: Beli Sekarang\n"
            response += f"• Sisa uang setelah beli: Rp {current_balance - price:,.0f}\n"
            response += "• Pastikan masih ada dana darurat\n\n"
            
            if price > income:  # Expensive item
                cheaper_option = price * 0.7
                response += f"**Pilihan 2**: Cari yang Lebih Murah (sekitar Rp {cheaper_option:,.0f})\n"
                response += "• Bisa sisihkan lebih banyak untuk tabungan\n"
                response += "• Resiko rugi lebih kecil\n\n"
        else:
            # Need to save
            kurang = price - current_balance
            monthly_saving = max(0, income - expense)
            if monthly_saving > 0:
                months_needed = kurang / monthly_saving
                response += f"**Pilihan 1**: Nabung Dulu ({months_needed:.0f} bulan)\n"
                response += f"• Nabung Rp {monthly_saving:,.0f} per bulan\n"
                response += "• Bisa beli cash tanpa hutang\n\n"
            
            if price > income * 2:  # Very expensive
                cheaper_option = price * 0.6
                response += f"**Pilihan 2**: Cari Alternatif Lebih Murah (Rp {cheaper_option:,.0f})\n"
                response += "• Lebih mudah dijangkau\n"
                response += "• Bisa beli lebih cepat\n\n"
        
        # Simple recommendation
        response += "🎯 **Saran Saya**: "
        if can_afford_now and price < income:
            response += "Boleh beli, tapi pastikan masih ada dana darurat minimal 3 bulan pengeluaran."
        elif can_afford_now and price >= income:
            response += "Bisa beli, tapi pertimbangkan apakah ini kebutuhan atau keinginan. Kalau keinginan, mending nabung dulu."
        else:
            if monthly_saving > 0:
                months_needed = (price - current_balance) / monthly_saving
                response += f"Nabung dulu sekitar {months_needed:.0f} bulan. Lebih aman dan tidak ada beban hutang."
            else:
                response += "Cari cara untuk mengurangi pengeluaran atau tambah pendapatan dulu sebelum beli ini."
        
        return response