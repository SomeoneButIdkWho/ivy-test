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
- Installed Python 3.11 and all dependencies
- Updated Flask server to use port 5000 (required for Replit)
- Created .gitignore for Python project
- Configured workflow for Discord bot with web preview

## Architecture Notes
- Uses discord.py's cog system for modular command organization
- Flask server runs in a separate thread to provide a web endpoint
- Bot automatically loads all cogs from the cogs/ directory on startup
