# Translation Bot

Translation Bot is a Python-based Telegram bot that allows users to translate text between different languages. It utilizes the DeepL API for translation and stores translation history in an SQLite database.
![image](https://github.com/Warmetallic/translation-bot/assets/35700332/62f2ebf4-dcd2-45d3-b2f5-9c12fccf5550)

## LINK: 
[@GK_TRANSLATE_BOT]

## Features

- Translate text between various languages.
- Maintain a history of translated texts.
- Delete translation history.
- User-friendly inline keyboard for language selection.

## Getting Started

Follow these instructions to get a copy of the project up and running on your local machine.

### Prerequisites

- Python 3.6 or higher
- Dependencies listed in `requirements.txt`. Alternatively it is possible to use Poetry to setup the project.

### Installation

1. Clone the repository to your local machine:

   ```bash
   git clone https://github.com/warmetallic/translation-bot.git
   cd translation-bot

2. Create a virtual environment (optional but recommended):
   
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use: venv\Scripts\activate

3. Install the required dependencies:
   
   ```bash
   pip install -r requirements.txt
   =====================or=======================
   poetry install
   
4. Create a .env file in the project root directory and add your DeepL API key:

   ```bash
    BOT_KEY=your_telegram_bot_token
    API_KEY=your_deepl_api_key

## Usage

1. Run the bot

   ```bash
   python translation-bot.py

2. Open Telegram and start a chat with your bot.

3. Use the following commands to interact with the bot:

* `/translate`: Start a translation session.
- `/history`: View your translation history.
+ `/delete_history`: Delete your translation history.


## Screenshots


![image](https://github.com/Warmetallic/translation-bot/assets/35700332/5463c704-7d0b-4289-a1ac-d87d122d631c)


![image](https://github.com/Warmetallic/translation-bot/assets/35700332/c28fb169-ad18-468a-a366-a50a9b37ae16) 
