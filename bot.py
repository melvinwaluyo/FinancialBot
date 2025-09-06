"""
Financial Bot Discord - Main Entry Point
Bot untuk melacak pemasukan dan pengeluaran dengan regex dan reflection
"""

import os
import asyncio
import logging
from dotenv import load_dotenv
import discord
from discord.ext import commands

from core.bot_core import FinancialBotCore

# Load environment variables
load_dotenv()

# Setup logging directory
os.makedirs('logs', exist_ok=True)

# Bot configuration
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
BOT_PREFIX = '!'

# Create bot instance dengan intents
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True

bot = commands.Bot(command_prefix=BOT_PREFIX, intents=intents, help_command=None)

# Initialize core bot
financial_core = FinancialBotCore()

@bot.event
async def on_ready():
    """Event ketika bot sudah siap"""
    print(f'🤖 Financial Bot is ready!')
    print(f'📝 Logged in as: {bot.user.name}')
    print(f'🆔 Bot ID: {bot.user.id}')
    print(f'🔗 Invite link: https://discord.com/oauth2/authorize?client_id={bot.user.id}&permissions=2048&scope=bot')
    print(f'💡 Bot will only respond when mentioned: @{bot.user.name}')
    print('='*50)
    
    # Set bot status
    activity = discord.Activity(type=discord.ActivityType.watching, name="for mentions 👀")
    await bot.change_presence(activity=activity)

@bot.event
async def on_message(message):
    """Event ketika ada pesan baru"""
    # Ignore pesan dari bot sendiri
    if message.author.bot:
        return
    
    # Check if bot is mentioned in the message
    is_mentioned = bot.user in message.mentions
    
    # Check if message starts with bot mention
    content = message.content.strip()
    starts_with_mention = content.startswith(f'<@{bot.user.id}>') or content.startswith(f'<@!{bot.user.id}>')
    
    # Only process if bot is mentioned
    if not (is_mentioned or starts_with_mention):
        # Still process commands for backward compatibility
        await bot.process_commands(message)
        return
    
    # Get user info
    user_id = str(message.author.id)
    username = message.author.display_name
    
    # Remove bot mention from content
    clean_content = content
    if starts_with_mention:
        # Remove the mention at the beginning
        clean_content = content.replace(f'<@{bot.user.id}>', '').replace(f'<@!{bot.user.id}>', '').strip()
    
    # Log pesan masuk
    print(f"📩 Mentioned by {username}: {clean_content}")
    
    # Process pesan
    try:
        # Process dengan financial core
        response = financial_core.process_message(user_id, username, clean_content)
        
        # Kirim response jika ada
        if response:
            # Split long messages
            if len(response) > 2000:
                # Split into chunks
                chunks = [response[i:i+1900] for i in range(0, len(response), 1900)]
                for chunk in chunks:
                    await message.channel.send(chunk)
            else:
                await message.channel.send(response)
    
    except Exception as e:
        error_msg = f"❌ Terjadi kesalahan: {str(e)}"
        await message.channel.send(error_msg)
        print(f"Error processing message: {e}")
    
    # Process commands juga (untuk compatibility)
    await bot.process_commands(message)

@bot.command(name='ping')
async def ping(ctx):
    """Test command untuk cek bot responsif"""
    latency = round(bot.latency * 1000)
    await ctx.send(f'🏓 Pong! Latency: {latency}ms')

@bot.command(name='stats')
async def stats(ctx):
    """Lihat statistik lengkap user"""
    user_id = str(ctx.author.id)
    stats = financial_core.get_user_stats(user_id)
    
    embed = discord.Embed(
        title="📊 Statistik Keuangan Anda",
        color=discord.Color.blue(),
        timestamp=ctx.message.created_at
    )
    
    # Balance info
    balance_info = stats['balance']
    embed.add_field(
        name="💰 Ringkasan",
        value=f"Pemasukan: Rp {balance_info['income']:,.0f}\n"
              f"Pengeluaran: Rp {balance_info['expense']:,.0f}\n"
              f"Saldo: Rp {balance_info['balance']:,.0f}",
        inline=False
    )
    
    # Transaction count
    embed.add_field(
        name="📈 Aktivitas",
        value=f"Total transaksi: {stats['transaction_count']}",
        inline=True
    )
    
    # Recent transactions preview
    if stats['recent_transactions']:
        recent_text = ""
        for trans in stats['recent_transactions'][:3]:
            emoji = "💚" if trans['type'] == 'income' else "💸"
            recent_text += f"{emoji} Rp {trans['amount']:,.0f} - {trans['category']}\n"
        
        embed.add_field(
            name="📋 Transaksi Terbaru",
            value=recent_text,
            inline=False
        )
    
    embed.set_footer(text=f"Requested by {ctx.author.display_name}")
    await ctx.send(embed=embed)

@bot.command(name='categories')
async def categories(ctx):
    """Lihat daftar kategori yang tersedia"""
    income_categories = financial_core.db.get_available_categories('income')
    expense_categories = financial_core.db.get_available_categories('expense')
    
    embed = discord.Embed(
        title="📂 Kategori yang Tersedia",
        color=discord.Color.green()
    )
    
    embed.add_field(
        name="💚 Pemasukan",
        value=", ".join(income_categories) if income_categories else "Tidak ada",
        inline=False
    )
    
    embed.add_field(
        name="💸 Pengeluaran", 
        value=", ".join(expense_categories) if expense_categories else "Tidak ada",
        inline=False
    )
    
    embed.add_field(
        name="💡 Tips",
        value="Bot akan otomatis menentukan kategori berdasarkan deskripsi Anda!",
        inline=False
    )
    
    await ctx.send(embed=embed)

@bot.command(name='recent')
async def recent_transactions(ctx, limit: int = 10):
    """Lihat transaksi terbaru (default 10)"""
    if limit > 50:
        limit = 50
    
    user_id = str(ctx.author.id)
    transactions = financial_core.db.get_user_transactions(user_id, limit)
    
    if not transactions:
        await ctx.send("📭 Anda belum memiliki transaksi apapun.")
        return
    
    embed = discord.Embed(
        title=f"📋 {len(transactions)} Transaksi Terbaru",
        color=discord.Color.blue()
    )
    
    for idx, trans in enumerate(transactions, 1):
        emoji = "💚" if trans['type'] == 'income' else "💸"
        type_text = "Pemasukan" if trans['type'] == 'income' else "Pengeluaran"
        
        value_text = f"{type_text}: Rp {trans['amount']:,.0f}\n"
        value_text += f"Kategori: {trans['category']}\n"
        if trans['description']:
            value_text += f"Deskripsi: {trans['description']}\n"
        value_text += f"ID: {trans['id']}"
        
        embed.add_field(
            name=f"{emoji} #{idx}",
            value=value_text,
            inline=True
        )
    
    await ctx.send(embed=embed)

@bot.event
async def on_command_error(ctx, error):
    """Handle command errors"""
    if isinstance(error, commands.CommandNotFound):
        # Ignore command not found errors karena kita handle semua pesan
        return
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("❌ Parameter yang diperlukan tidak lengkap. Ketik `!help` untuk bantuan.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("❌ Parameter tidak valid. Pastikan format sudah benar.")
    else:
        await ctx.send(f"❌ Terjadi kesalahan: {str(error)}")
        print(f"Command error: {error}")

def main():
    """Main function untuk menjalankan bot"""
    if not DISCORD_TOKEN:
        print("❌ DISCORD_TOKEN tidak ditemukan!")
        print("📝 Buat file .env berdasarkan .env.example dan isi dengan token bot Anda.")
        return
    
    try:
        print("🚀 Starting Financial Bot...")
        print("🔑 Token loaded successfully")
        print("⏳ Connecting to Discord...")
        print("💡 Bot will only respond when mentioned!")
        
        bot.run(DISCORD_TOKEN)
    
    except discord.LoginFailure:
        print("❌ Login gagal! Periksa token Discord bot Anda.")
    except Exception as e:
        print(f"❌ Error menjalankan bot: {e}")

if __name__ == "__main__":
    main()