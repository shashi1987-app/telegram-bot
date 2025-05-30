from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = "8094380646:AAHR3hJ58BeYM_O8M7hpidScKQwtBG3vqDs"

# Har user ke liye class/subject store karne ke liye
user_data = {}

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    # Reset user state
    user_data[user_id] = {}

    keyboard = [[KeyboardButton("9"), KeyboardButton("10")],
                [KeyboardButton("11"), KeyboardButton("12")]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)

    await update.message.reply_text("Welcome! Apna class select karo:", reply_markup=reply_markup)

# Message handling
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    message = update.message.text.strip().lower()

    # Agar class select nahi hui hai
    if user_id not in user_data or 'class' not in user_data[user_id]:
        if message in ['9', '10', '11', '12']:
            user_data[user_id] = {'class': message}
            keyboard = [[KeyboardButton("Maths"), KeyboardButton("Physics")],
                        [KeyboardButton("Chemistry"), KeyboardButton("English")]]
            reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
            await update.message.reply_text(f"Class {message} select kiya. Ab subject select karo:", reply_markup=reply_markup)
        else:
            await update.message.reply_text("Please valid class (9-12) choose karo.")
    
    # Agar class select ho chuki hai, ab subject chahiye
    elif 'subject' not in user_data[user_id]:
        if message in ['maths', 'physics', 'chemistry', 'english']:
            user_data[user_id]['subject'] = message

            selected_class = user_data[user_id]['class']
            selected_subject = user_data[user_id]['subject']

            # ✅ Yaha URL update kiya gaya hai
            link = f"https://growthreads.in/question-papers/?class={selected_class}&subject={selected_subject}"

            await update.message.reply_text(
                f"Class {selected_class} ka {selected_subject.capitalize()} subject select kiya.\n"
                f"Click here to view/download 5 saal ke papers:\n{link}"
            )

            # Reset kar diya so user dobara start kar sake
            del user_data[user_id]
        else:
            await update.message.reply_text("Please valid subject (Maths, Physics, Chemistry, English) choose karo.")
    else:
        await update.message.reply_text("Type /start to begin again.")

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
