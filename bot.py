import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Updater,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,  # Changed from Filters to filters
    CallbackContext,
    ApplicationBuilder,  # New in v20.x
    ContextTypes,  # New in v20.x
)

# Configuration - USING YOUR PROVIDED TOKEN (will be revoked after testing)
TELEGRAM_TOKEN = '8022918713:AAEDN4RZ0TrhTJPe5G_DvpvebszR1VuMaU4'
CHANNEL_USERNAME = '@yourchannel'  # Change this to your actual channel
GROUP_USERNAME = '@yourgroup'      # Change this to your actual group
TWITTER_USERNAME = '@yourtwitter'   # Change this to your actual Twitter

# Bot states
JOIN_CHANNEL, JOIN_GROUP, FOLLOW_TWITTER, SUBMIT_WALLET = range(4)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Send message on `/start`."""
    user = update.message.from_user
    await update.message.reply_text(
        f"👋 Welcome {user.first_name} to our Airdrop Bot!\n\n"
        "Complete the steps below to qualify for the airdrop:"
    )
    
    # Step 1: Join channel
    keyboard = [
        [InlineKeyboardButton("Join Channel", url=f"https://t.me/{CHANNEL_USERNAME[1:]}")],
        [InlineKeyboardButton("I've Joined ✅", callback_data='joined_channel')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "1. Join our official channel:",
        reply_markup=reply_markup
    )
    return JOIN_CHANNEL

async def joined_channel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """User claims to have joined the channel."""
    query = update.callback_query
    await query.answer()
    
    # Step 2: Join group
    keyboard = [
        [InlineKeyboardButton("Join Group", url=f"https://t.me/{GROUP_USERNAME[1:]}")],
        [InlineKeyboardButton("I've Joined ✅", callback_data='joined_group')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        "✅ Channel joined!\n\n"
        "2. Join our official group:",
        reply_markup=reply_markup
    )
    return JOIN_GROUP

async def joined_group(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """User claims to have joined the group."""
    query = update.callback_query
    await query.answer()
    
    # Step 3: Follow Twitter
    keyboard = [
        [InlineKeyboardButton("Follow Twitter", url=f"https://twitter.com/{TWITTER_USERNAME[1:]}")],
        [InlineKeyboardButton("I'm Following ✅", callback_data='followed_twitter')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        "✅ Group joined!\n\n"
        "3. Follow us on Twitter:",
        reply_markup=reply_markup
    )
    return FOLLOW_TWITTER

async def followed_twitter(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """User claims to have followed Twitter."""
    query = update.callback_query
    await query.answer()
    
    await query.edit_message_text(
        "✅ Twitter followed!\n\n"
        "4. Please send your Solana wallet address to receive the airdrop:"
    )
    return SUBMIT_WALLET

async def submit_wallet(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """User submits wallet address."""
    wallet_address = update.message.text
    
    # Very basic Solana address validation (just checks length)
    if len(wallet_address) < 32 or len(wallet_address) > 44:
        await update.message.reply_text("❌ Invalid Solana wallet address. Please try again.")
        return SUBMIT_WALLET
    
    await update.message.reply_text(
        "🎉 Congratulations!\n\n"
        "10 SOL is on its way to your wallet!\n\n"
        "Thank you for participating in our airdrop!"
    )
    return -1  # Ends the conversation

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    await update.message.reply_text(
        'Airdrop registration cancelled. Type /start to begin again.'
    )
    return -1

def main() -> None:
    """Run the bot."""
    # Create the Application
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    # Setup conversation handler
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            JOIN_CHANNEL: [CallbackQueryHandler(joined_channel, pattern='^joined_channel$')],
            JOIN_GROUP: [CallbackQueryHandler(joined_group, pattern='^joined_group$')],
            FOLLOW_TWITTER: [CallbackQueryHandler(followed_twitter, pattern='^followed_twitter$')],
            SUBMIT_WALLET: [MessageHandler(filters.TEXT & ~filters.COMMAND, submit_wallet)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    application.add_handler(conv_handler)

    # Start the Bot
    application.run_polling()

if __name__ == '__main__':
    main()
