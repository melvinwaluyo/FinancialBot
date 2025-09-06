"""
Database management untuk Financial Bot
Menggunakan SQLite untuk menyimpan data transaksi
"""

import sqlite3
import os
from datetime import datetime
from typing import List, Dict, Optional, Tuple

class DatabaseManager:
    def __init__(self, db_path: str = "financial_bot.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Inisialisasi database dan tabel"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Tabel transaksi
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS transactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT NOT NULL,
                    username TEXT NOT NULL,
                    transaction_type TEXT NOT NULL CHECK (transaction_type IN ('income', 'expense')),
                    amount REAL NOT NULL,
                    category TEXT NOT NULL,
                    description TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Tabel kategori default
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS categories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE NOT NULL,
                    type TEXT NOT NULL CHECK (type IN ('income', 'expense', 'both'))
                )
            ''')
            
            # Insert kategori default jika belum ada
            default_categories = [
                ('Gaji', 'income'),
                ('Freelance', 'income'),
                ('Investasi', 'income'),
                ('Hadiah', 'income'),
                ('Makanan', 'expense'),
                ('Transport', 'expense'),
                ('Hiburan', 'expense'),
                ('Belanja', 'expense'),
                ('Tagihan', 'expense'),
                ('Kesehatan', 'expense'),
                ('Pendidikan', 'expense'),
                ('Lainnya', 'both')
            ]
            
            cursor.executemany('''
                INSERT OR IGNORE INTO categories (name, type) VALUES (?, ?)
            ''', default_categories)
            
            conn.commit()
    
    def add_transaction(self, user_id: str, username: str, transaction_type: str, 
                       amount: float, category: str, description: str = "") -> bool:
        """Tambah transaksi baru"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO transactions (user_id, username, transaction_type, amount, category, description)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (user_id, username, transaction_type, amount, category, description))
                conn.commit()
                return True
        except Exception as e:
            print(f"Error adding transaction: {e}")
            return False
    
    def get_user_balance(self, user_id: str) -> Dict[str, float]:
        """Dapatkan saldo user"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Total pemasukan
            cursor.execute('''
                SELECT COALESCE(SUM(amount), 0) FROM transactions 
                WHERE user_id = ? AND transaction_type = 'income'
            ''', (user_id,))
            total_income = cursor.fetchone()[0]
            
            # Total pengeluaran
            cursor.execute('''
                SELECT COALESCE(SUM(amount), 0) FROM transactions 
                WHERE user_id = ? AND transaction_type = 'expense'
            ''', (user_id,))
            total_expense = cursor.fetchone()[0]
            
            balance = total_income - total_expense
            
            return {
                'income': total_income,
                'expense': total_expense,
                'balance': balance
            }
    
    def get_user_transactions(self, user_id: str, limit: int = 10) -> List[Dict]:
        """Dapatkan transaksi terakhir user"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id, transaction_type, amount, category, description, created_at
                FROM transactions 
                WHERE user_id = ? 
                ORDER BY created_at DESC 
                LIMIT ?
            ''', (user_id, limit))
            
            transactions = []
            for row in cursor.fetchall():
                transactions.append({
                    'id': row[0],
                    'type': row[1],
                    'amount': row[2],
                    'category': row[3],
                    'description': row[4],
                    'date': row[5]
                })
            
            return transactions
    
    def get_category_report(self, user_id: str) -> Dict[str, Dict[str, float]]:
        """Dapatkan laporan per kategori"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT category, transaction_type, SUM(amount) as total
                FROM transactions 
                WHERE user_id = ? 
                GROUP BY category, transaction_type
                ORDER BY total DESC
            ''', (user_id,))
            
            report = {}
            for row in cursor.fetchall():
                category = row[0]
                trans_type = row[1]
                total = row[2]
                
                if category not in report:
                    report[category] = {'income': 0, 'expense': 0}
                
                report[category][trans_type] = total
            
            return report
    
    def get_available_categories(self, transaction_type: str = None) -> List[str]:
        """Dapatkan daftar kategori yang tersedia"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            if transaction_type:
                cursor.execute('''
                    SELECT name FROM categories 
                    WHERE type = ? OR type = 'both'
                    ORDER BY name
                ''', (transaction_type,))
            else:
                cursor.execute('''
                    SELECT name FROM categories 
                    ORDER BY name
                ''')
            
            return [row[0] for row in cursor.fetchall()]
    
    def delete_transaction(self, user_id: str, transaction_id: int) -> bool:
        """Hapus transaksi"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    DELETE FROM transactions 
                    WHERE id = ? AND user_id = ?
                ''', (transaction_id, user_id))
                
                if cursor.rowcount > 0:
                    conn.commit()
                    return True
                return False
        except Exception as e:
            print(f"Error deleting transaction: {e}")
            return False
