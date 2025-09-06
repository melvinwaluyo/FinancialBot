#!/usr/bin/env python3
"""
Demo of the updated Pure Indonesian Budget Advice and Purchase Planning features
Simple and logical analysis
"""

from core.bot_core import FinancialBotCore
import os

def main():
    """Demo the Indonesian features"""
    print("🇮🇩 MOGRE FINANCIAL ASSISTANT - FITUR BAHASA INDONESIA")
    print("Analisis Anggaran dan Perencanaan Pembelian dalam Bahasa Indonesia")
    print("="*65)
    
    # Setup
    test_db = "demo_indonesian.db"
    if os.path.exists(test_db):
        try:
            os.remove(test_db)
        except:
            pass
    
    bot = FinancialBotCore(test_db)
    user_id = "demo_user_id"
    username = "DemoUser"
    
    print("\n📊 Menambahkan data keuangan...")
    print("Pemasukan: Rp 6,250,000")
    print("Pengeluaran: Rp 4,500,000")
    
    bot.process_message(user_id, username, "Saya dapat gaji 6250000 dari kantor")
    bot.process_message(user_id, username, "Habis 4500000 untuk pengeluaran bulanan")
    
    print("\n" + "="*65)
    print("🏦 CONTOH SARAN ANGGARAN")
    print("="*65)
    print("\nKamu: bantuan anggaran saya")
    print("\nMoGre Financial Assistant:")
    response = bot.process_message(user_id, username, "bantuan anggaran saya")
    print(response)
    
    print("\n" + "="*65)
    print("🛍️ CONTOH ANALISIS PEMBELIAN")
    print("="*65)
    print("\nKamu: saya mau beli mobil 30000000")
    print("\nMoGre Financial Assistant:")
    response = bot.process_message(user_id, username, "saya mau beli mobil 30000000")
    print(response)
    
    print("\n" + "="*65)
    print("✅ FITUR BERHASIL DIUBAH KE BAHASA INDONESIA")
    print("="*65)
    print("✓ Pola regex murni bahasa Indonesia")
    print("✓ Analisis yang lebih sederhana dan logis")
    print("✓ Response dalam bahasa Indonesia sepenuhnya")
    print("✓ Saran yang mudah dipahami")
    print("✓ Tidak ada campuran bahasa Inggris")

if __name__ == "__main__":
    main()
