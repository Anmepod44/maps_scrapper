import asyncio
import os
import random
from PIL import Image
from telegram import Update, InputFile
from telegram.ext import Application, CommandHandler, ContextTypes
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
TOKEN = os.getenv("TELEGRAM_API_TOKEN")

# Story content
story_parts = [
    "Once upon a time, there was an extraordinary woman, She had the kindest heart and the most beautiful smile.",
    "Her laughter was like music, bringing happiness to everyone around her.",
    "She was not just beautiful; she was smart, strong, and always knew how to make people feel loved.",
    "She had a way of turning even ordinary moments into magical memories.",
    "Every day spent with her is a gift, and I am incredibly lucky."
]

# Function to get a random valid image from the 'img' folder
def get_random_image() -> str:
    img_folder = "img"
    images = os.listdir(img_folder)

    for _ in range(len(images)):
        random_image = os.path.join(img_folder, random.choice(images))
        try:
            # Validate the image using Pillow
            with Image.open(random_image) as img:
                img.verify()  # Check if it's a valid image
                return random_image
        except Exception as e:
            print(f"Skipping invalid image: {random_image} ({e})")
    return None

# Define the /start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Hi there! Let me tell you a story about someone truly amazing. Just type /story to begin!"
    )

# Define the /story command handler
async def story(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.message.chat_id

    # Tell the story part by part
    for part in story_parts:
        await context.bot.send_message(chat_id=chat_id, text=part)

        # Send a random valid image to complement the story
        random_image = get_random_image()
        if random_image:
            try:
                await context.bot.send_photo(chat_id=chat_id, photo=InputFile(random_image))
            except Exception as e:
                print(f"Failed to send image: {random_image} ({e})")
        else:
            await context.bot.send_message(chat_id=chat_id, text="(Imagine a beautiful image here!)")

        # Pause between story parts for effect
        await asyncio.sleep(3)

    # End the story with a special message
    await context.bot.send_message(
        chat_id=chat_id,
        text="And that's the story of Babe, the most amazing person ever. Thank you for listening! ❤️"
    )

# Main function to start the bot
async def main():
    # Create the application
    application = Application.builder().token(TOKEN).build()

    # Add command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("story", story))

    # Initialize and start the bot
    await application.initialize()
    print("Bot is running... Press Ctrl+C to stop.")

    try:
        # Run the bot in polling mode (blocking call)
        await application.start()
        await application.updater.start_polling()
        await asyncio.Future()  # Keep running until manually stopped
    except KeyboardInterrupt:
        print("Shutting down bot...")
    finally:
        # Gracefully stop the updater and application
        await application.updater.stop()
        await application.shutdown()

# Entry point
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot stopped manually.")
