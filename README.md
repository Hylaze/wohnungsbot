# Telegram Bot Setup

## 1. Get a Telegram Bot Token

1. Open Telegram and search for **BotFather**
2. Start a chat with BotFather
3. Send the following commands:
   ```
   /start
   /newbot
   ```
4. Follow the instructions and copy your `BOT_TOKEN`

---

## 2. Get Your User Chat ID

### Step 1: Start Your Bot

1. Open Telegram  
2. Search for your bot (the username you created with BotFather)  
3. Click **Start** or send any message (e.g. `hi`)

### Step 2: Retrieve Chat ID

Open the following URL in your browser:

```
https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates
```

### Step 3: Find Your Chat ID

Look for a section like this in the response:

```json
"chat": {
  "id": 123456789
}
```

Your `CHAT_ID` is the number shown in `"id"`.

---
