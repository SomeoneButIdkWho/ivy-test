# Discord Bot Project

## Overview
This is a Discord bot application built with discord.py. The bot includes a Flask web server for keep-alive functionality and uses a modular cog system for organizing commands.

## Project Structure
- `bot.py` - Main bot entry point that loads cogs and starts the bot
- `keep_alive.py` - Flask web server (runs on port 5000) to keep the bot alive
- `cogs/` - Directory containing bot command modules:
  - `echo.py` - Echo command that repeats user input
  - `greetings.py` - Auto-responds to greetings like "hi", "hello", "hey"
  - `reply.py` - Reply command that replies to messages

## Dependencies
- discord.py - Discord bot framework
- flask - Web server for keep-alive
- python-dotenv - Environment variable management

## Configuration
- **BOT_TOKEN** - Required Discord bot token (stored as a secret)
- Command prefix: `!` (e.g., `!echo Hello`, `!reply Test`)

## Recent Changes (October 18, 2025)
- Initial setup in Replit environment
- Installed Python 3.11 and all dependencies (discord.py, flask, python-dotenv)
- Updated Flask server to use port 5000 (required for Replit)
- Created .gitignore for Python project
- Configured workflow for Discord bot with web preview
- Updated bot.py to use modern async/await pattern for loading extensions
- Updated all cog setup() functions to be async (discord.py 2.x requirement)
- Configured VM deployment for continuous bot operation

## Architecture Notes
- Uses discord.py 2.6.4 with modern async/await patterns
- Flask server runs in a separate thread to provide a web endpoint (keep-alive)
- Bot automatically loads all cogs from the cogs/ directory on startup using async loading
- Cogs use the async setup() pattern required by discord.py 2.x

## Setup Instructions
1. Make sure BOT_TOKEN secret is set with a valid Discord bot token
2. The bot will automatically start and connect to Discord
3. Invite the bot to your server with proper permissions (message content intent enabled)
4. Use commands like `!echo`, `!reply`, or send greetings to test the bot

## Troubleshooting
- If you see "Improper token has been passed" error, verify your BOT_TOKEN is correct
- Make sure your Discord bot has "Message Content Intent" enabled in the Discord Developer Portal
- The Flask server on port 5000 is for keep-alive purposes and shows "Bot is alive!" when accessed
