"""
Rules engine dengan regex dan reflection kata ganti untuk Financial Bot
Menangani parsing perintah dan respons yang natural
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
            'gue': 'lu',
            'gw': 'lu',
            'kamu': 'saya',
            'lu': 'gue',
            'anda': 'saya',
            'my': 'your',
            'mine': 'yours',
            'i': 'you',
            'me': 'you',
            'you': 'me',
            'your': 'my',
            'yours': 'mine'
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
        
        # Pattern untuk pemasukan - Diperbaiki urutan dan struktur
        self.income_patterns = [
            # Pattern: !income 100000 gaji bonus bulan ini
            r'!income\s+(\d+(?:\.\d+)?)\s+(\w+)(?:\s+(.+))?',
            # Pattern natural: saya dapat gaji 5000000 dari kantor
            r'(?:saya|aku|gw|gue)\s+(?:dapat|terima|dapet|menerima|meraih|peroleh)\s+(\w+)\s+(\d+(?:\.\d+)?)\s*(?:dari\s+(.+))?',
            # Pattern: dapat 500000 freelance
            r'(?:dapat|terima|dapet|menerima|meraih|peroleh)\s+(\d+(?:\.\d+)?)\s+(\w+)(?:\s+(.+))?',
            # Pattern: income 1000000 kategori deskripsi
            r'(?:income|pemasukan|masuk)\s+(\d+(?:\.\d+)?)\s+(\w+)(?:\s+(.+))?'
        ]
        
        # Pattern untuk pengeluaran - Diperbaiki dengan sinonim
        self.expense_patterns = [
            # Pattern: !expense 50000 makanan makan siang
            r'!expense\s+(\d+(?:\.\d+)?)\s+(\w+)(?:\s+(.+))?',
            # Pattern natural: saya habis 50000 untuk makanan
            r'(?:saya|aku|gw|gue)\s+(?:habis|keluar|bayar|beli|menghabiskan|mengeluarkan|spent|belanja|pakai|gunakan)\s+(\d+(?:\.\d+)?)\s+(?:untuk\s+)?(\w+)(?:\s+(.+))?',
            # Pattern: keluar 75000 transport
            r'(?:keluar|habis|bayar|beli|expense|pengeluaran|menghabiskan|mengeluarkan|belanja|pakai|gunakan)\s+(\d+(?:\.\d+)?)\s+(?:untuk\s+)?(\w+)(?:\s+(.+))?',
            # Pattern: beli makanan 25000
            r'(?:beli|bayar|belanja)\s+(\w+)\s+(\d+(?:\.\d+)?)(?:\s+(.+))?'
        ]
        
        # Pattern untuk saldo - Made more specific to avoid conflicts
        self.balance_patterns = [
            r'^!balance$',
            r'^(?:saldo|balance)(?:\s+(?:saya|aku|gw|gue))?$',
            r'^(?:cek|lihat|check)\s+(?:saldo|balance|uang)$',
            r'^(?:berapa|how much)\s+(?:saldo|uang|money)(?:\s+(?:saya|aku|gw|gue))?$',
            r'^(?:saya|aku|gw|gue)\s+(?:punya|ada)\s+(?:berapa|how much)$'
        ]
        
        # Pattern untuk laporan - Made more specific and comprehensive
        self.report_patterns = [
            r'^!report$',
            r'^(?:laporan|report)$',
            r'^(?:lihat|show|cek)\s+(?:laporan|report)$',
            r'^(?:ringkasan|summary)\s+(?:keuangan|finansial|financial)$',
            r'^summary\s+keuangan$',  # Specific pattern for test case
            r'^(?:laporan|report)\s+(?:keuangan|finansial|financial)$'
        ]
        
        # Pattern untuk bantuan
        self.help_patterns = [
            r'!help',
            r'(?:help|bantuan)',
            r'(?:gimana|bagaimana|how)\s+(?:cara|way)',
            r'(?:apa|what)\s+(?:perintah|command)'
        ]
        
        # Pattern untuk hapus transaksi
        self.delete_patterns = [
            r'!delete\s+(\d+)',
            r'(?:hapus|delete|remove)\s+(?:transaksi\s+)?(\d+)',
            r'(?:batalkan|cancel)\s+(?:transaksi\s+)?(\d+)'
        ]
        
        # Pattern untuk pertanyaan umum tentang bot - FIXED
        self.about_patterns = [
            r'(?:siapa|who)\s+(?:kamu|you|bot)',
            r'(?:apa|what)\s+(?:nama|name)\s+(?:kamu|you)',
            r'(?:kamu|you)\s+(?:siapa|who)',
            r'(?:perkenalkan|introduce)\s+(?:diri|yourself)',
            r'^(?:hai|hello|hi|halo)$',
            r'^(?:apa kabar|how are you)$',
            r'who\s+are\s+you',  # Fixed: specific pattern for "who are you"
            r'what\s+are\s+you'   # Added: "what are you"
        ]
        
        # Pattern untuk pertanyaan kemampuan bot
        self.capability_patterns = [
            r'(?:apa|what)\s+(?:yang bisa|can you do)',
            r'(?:kamu|you)\s+(?:bisa|can)\s+(?:apa|what)',
            r'(?:fungsi|function|fitur|feature)\s+(?:apa|what)',
            r'(?:kemampuan|capability|abilities)\s+(?:kamu|you)',
            r'(?:untuk apa|what for)\s+(?:kamu|you)'
        ]
        
        # Pattern untuk ucapan terima kasih
        self.thanks_patterns = [
            r'(?:terima kasih|thank you|thanks|makasih)',
            r'(?:bagus|good|mantap|keren|nice)',
            r'(?:hebat|great|awesome|amazing)'
        ]
        
        # Pattern untuk salam perpisahan - FIXED
        self.goodbye_patterns = [
            r'^(?:bye|goodbye|sampai jumpa|dadah|selamat tinggal)$',  # Fixed: exact match
            r'^(?:see you|until next time|sampai nanti)$',  # Fixed: exact match
            r'bye\s*$',  # Match "bye" at end of line
            r'goodbye\s*$'  # Match "goodbye" at end of line
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
        
        # Income categories
        income_keywords = {
            'gaji': ['gaji', 'salary', 'kantor', 'kerja', 'office', 'pekerjaan', 'job'],
            'freelance': ['freelance', 'projek', 'project', 'kontrak', 'lepas', 'sampingan'],
            'investasi': ['saham', 'reksadana', 'dividen', 'profit', 'trading', 'invest'],
            'hadiah': ['hadiah', 'gift', 'bonus', 'reward', 'prize', 'kado', 'pemberian']
        }
        
        # Expense categories
        expense_keywords = {
            'makanan': ['makan', 'food', 'nasi', 'ayam', 'restaurant', 'cafe', 'snack', 'lapar', 'kenyang', 'minuman', 'drink'],
            'transport': ['transport', 'bensin', 'ojek', 'taksi', 'bus', 'kereta', 'grab', 'gojek', 'uber', 'motor', 'mobil'],
            'hiburan': ['film', 'movie', 'game', 'spotify', 'netflix', 'youtube', 'concert', 'musik', 'entertainment'],
            'belanja': ['beli', 'shopping', 'baju', 'sepatu', 'elektronik', 'gadget', 'belanja', 'mall', 'toko'],
            'tagihan': ['listrik', 'air', 'internet', 'wifi', 'telepon', 'cicilan', 'bayar', 'bill', 'utilities'],
            'kesehatan': ['dokter', 'obat', 'hospital', 'medical', 'vitamin', 'therapy', 'rumah sakit', 'clinic'],
            'pendidikan': ['kursus', 'buku', 'sekolah', 'kuliah', 'training', 'course', 'seminar', 'workshop']
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
    
    def match_pattern(self, text: str, patterns: List[str]) -> Optional[re.Match]:
        """Match text dengan list of patterns"""
        for pattern in patterns:
            match = re.search(pattern, text.lower(), re.IGNORECASE)
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
        if text.lower().startswith(('saya', 'aku', 'gw', 'gue')):
            # Natural language: saya dapat freelance 1000000 dari projek
            category = groups[0].lower()
            amount = self.parse_amount(groups[1])
            description = groups[2] if len(groups) > 2 and groups[2] else ""
        else:
            # Standard: amount category description
            amount = self.parse_amount(groups[0])
            category = groups[1].lower() if len(groups) >= 2 and groups[1] else "lainnya"
            description = groups[2] if len(groups) > 2 and groups[2] else ""
        
        # Auto-categorize if category is generic
        if category in ['uang', 'dana', 'income', 'pemasukan']:
            category = self.categorize_automatically(description, amount)
        
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
        
        # Auto-categorize if category is generic
        if category in ['uang', 'dana', 'expense', 'pengeluaran']:
            category = self.categorize_automatically(description, amount)
        
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
        
        # Check report FIRST (before balance to prevent conflicts)
        if self.match_pattern(text, self.report_patterns):
            return {'type': 'report'}
        
        # Check help
        if self.match_pattern(text, self.help_patterns):
            return {'type': 'help'}
        
        # Check delete
        delete_result = self.parse_delete_command(text)
        if delete_result:
            return delete_result
        
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
                   "• Bahasa: Indonesia & English\n"
                   "• Dibuat dengan: Python & Love ❤️\n\n"
                   "💡 Saya bisa memahami bahasa natural, jadi kamu bisa bicara santai denganku!\n"
                   "Ketik `!help` untuk melihat semua yang bisa saya lakukan.")
        
        elif command_type == 'capability':
            return ("🚀 **Kemampuan Saya:**\n\n"
                   "💰 **Manajemen Keuangan:**\n"
                   "• Catat pemasukan dan pengeluaran\n"
                   "• Hitung saldo otomatis\n"
                   "• Buat laporan keuangan\n"
                   "• Kategorisasi transaksi otomatis\n\n"
                   "🧠 **Kecerdasan:**\n"
                   "• Mengerti bahasa natural Indonesia & English\n"
                   "• Pahami bahasa gaul (gue/lu, dll)\n"
                   "• Auto-detect kategori dari deskripsi\n"
                   "• Reflection kata ganti untuk percakapan natural\n\n"
                   "📊 **Fitur Lain:**\n"
                   "• Multi-user support\n"
                   "• Real-time balance tracking\n"
                   "• Rich formatting dengan emoji\n"
                   "• Error handling yang informatif\n\n"
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

**Cara Natural:**
• "@FinancialBot Saya dapat gaji 5000000 dari kantor"
• "@FinancialBot Habis 50000 untuk makanan lunch"
• "@FinancialBot Berapa saldo saya?"
• "@FinancialBot Lihat laporan keuangan"

**Pertanyaan Umum:**
• "@FinancialBot Siapa kamu?" - Kenalan dengan bot
• "@FinancialBot Apa yang bisa kamu lakukan?" - Lihat kemampuan

**Kategori Otomatis:**
Makanan, Transport, Hiburan, Belanja, Tagihan, Kesehatan, Pendidikan, Gaji, Freelance, Investasi, dll.""")
        
        elif command_type == 'delete':
            return f"Transaksi dengan ID {command_result['transaction_id']} telah dihapus."
        
        elif command_type == 'unknown':
            original = command_result.get('original_text', '')
            reflected = self.reflection_engine.reflect_text(original)
            return (f"Maaf, saya tidak mengerti perintah '{original}'. "
                   f"Ketik `!help` untuk melihat panduan penggunaan.\n\n"
                   f"💡 **Atau coba tanyakan:**\n"
                   f"• \"Siapa kamu?\" - Untuk berkenalan\n"
                   f"• \"Apa yang bisa kamu lakukan?\" - Untuk melihat kemampuan saya")
        
        return "Perintah tidak dikenali. Ketik `!help` untuk bantuan."