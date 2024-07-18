import io
import logging
import os
import PIL.Image
import google.generativeai as genai
from aiogram import Bot, Dispatcher, Router
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import Message
import asyncio  # Add this import
import markdown


# Create the bot object.
# TOKEN = os.getenv('BOT_TOKEN')
bot = Bot(token="7464571551:AAHVI_1lyg3G86hEZIk42QMms6gTfhWEohg")
dp = Dispatcher()
router = Router()
dp.include_router(router)

# Use os.getenv for the Google API key
# GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

# Configure the API key for Gemini
# genai.configure(api_key="risheendra-706e78316177.json")
genai.configure(api_key="AIzaSyBV8h_Rk9_efeWGUODO4CIyNIxLobsu0LU")

model = genai.GenerativeModel('gemini-pro-vision')

chat_sessions = {}

# @router.message(Command("gemi"))
@router.message()
async def gemi_handler(message: Message):
    try:
        prompt = message.text
        safety_settings = {
        "HARM_CATEGORY_HARASSMENT": "BLOCK_NONE",
        "HARM_CATEGORY_HATE_SPEECH": "BLOCK_NONE",
        "HARM_CATEGORY_SEXUALLY_EXPLICIT": "BLOCK_NONE",
        "HARM_CATEGORY_DANGEROUS_CONTENT": "BLOCK_NONE",
    }
        chat_id = message.chat.id
        # Example: Generate text from a prompt
        # model = genai.GenerativeModel('gemini-1.5-flash', safety_settings=safety_settings)
        # chat = model.start_chat(history=[])
        # response = chat.send_message(prompt)
        generation_config = genai.GenerationConfig(
        response_mime_type="text/plain",
        max_output_tokens=1000,
        temperature=1.5,
        top_p= 0.95,
        top_k= 64,
    )
        system_instruction = "You are a teacher named albert."
        if chat_id not in chat_sessions:
            model = genai.GenerativeModel('gemini-1.5-flash', safety_settings=safety_settings,generation_config=generation_config,system_instruction=system_instruction)
            chat_sessions[chat_id] = model.start_chat(history=[])
            chat = chat_sessions[chat_id]
        else:
            chat = chat_sessions[chat_id]
        # print(chat)
        response = chat.send_message(prompt)

        response_text = response.text
 
        print(response_text)
        if len(response_text) > 4000:
            # Split the response into parts
            parts = [response_text[i:i+4000] for i in range(0, len(response_text), 4000)]
            for part in parts:
                await message.answer(part, parse_mode=ParseMode.MARKDOWN
                                     )
        else:
            # Send the response as a single message
            await message.answer(response_text, parse_mode=ParseMode.MARKDOWN
                                 )

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        await message.answer(f"An error occurred: {str(e)}")
 

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())