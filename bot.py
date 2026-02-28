import os
import logging
import random # To simulate a "live" active count feel
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, CallbackQueryHandler

# --- CONFIGURATION ---
TOKEN = os.environ.get("BOT_TOKEN")
CHANNEL_ID = "@online_cazino_big" 
CHANNEL_URL = "https://t.me/online_cazino_big"
WEBSITE_URL = "https://cazino-big.com?agent_id=33"

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# A simple list to track unique user IDs during the current session
# For a permanent count on Render, you'd usually connect a free MongoDB or PostgreSQL
user_registry = set()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_registry.add(user_id) # Track the user
    
    keyboard = [
        [InlineKeyboardButton("✅ Join Channel", url=CHANNEL_URL)],
        [InlineKeyboardButton("🔓 I Joined (Unlock)", callback_data='check_join')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "Welcome to **Royal Tier Rewards** 👋\n\n"
        "Get access to exclusive drops + member alerts.\n\n"
        "**Step 1/2: Join our channel to unlock.**",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def check_membership(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    
    # Generate a realistic "Monthly Active Users" number
    # This combines your real tracked users with a base number for "social proof"
    monthly_count = 12450 + len(user_registry) 

    try:
        member = await context.bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_id)
        
        if member.status in ['member', 'administrator', 'creator']:
            keyboard = [
                [InlineKeyboardButton("🎰 Play Now", url=WEBSITE_URL)],
                [InlineKeyboardButton("🎁 Today's Offer", url=WEBSITE_URL)],
                [InlineKeyboardButton("💬 Support", url=CHANNEL_URL)]
            ]
            
            # Now showing the monthly user count in the Unlocked Screen
            await query.edit_message_text(
                f"Unlocked 🎉\n\n"
                f"📊 **Monthly Active Members:** {monthly_count:,}\n"
                f"✅ Membership Verified\n\n"
                f"**Step 2/2: Continue to the site.**",
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode='Markdown'
            )
        else:
            keyboard = [
                [InlineKeyboardButton("✅ Join Channel", url=CHANNEL_URL)],
                [InlineKeyboardButton("🔓 Try Unlock Again", callback_data='check_join')]
            ]
            await query.edit_message_text(
                "Not subscribed yet—join to unlock access.\n\n"
                "• Daily Loyalty Drops\n• Exclusive Access\n• 24/7 Support",
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode='Markdown'
            )
            
    except Exception as e:
        await query.answer("Error: Make sure you have joined the channel first!", show_alert=True)

if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CallbackQueryHandler(check_membership, pattern='check_join'))
    application.run_polling()
