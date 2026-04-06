Setup:

get a telegram bot token

1. Open Telegram and search for Telegram
2. Start a chat with BotFather
3. Send:
  /start
  /newbot
4. Follow the steps and copy your BOT_TOKEN

get user chat token 

1.Start your bot
  1.1 Open Telegram
  1.2 Search for your bot (the username you created with BotFather)
  1.3 Click Start or send any message (e.g. “hi”)
2. Open in browser:
  https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates
3. Look for:
  "chat":{"id":123456789}
