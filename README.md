# Auto Forward Bot

A simple Telegram bot that automatically forwards **video files** from a source channel to a destination channel. The bot is built using Python and the Telegram Bot API.

## Features
- Forwards **only video files** from a **source channel** to a **destination channel**.
- Handles **forwarded messages** properly.
- Supports **media groups (albums).**
- Uses logging for debugging and monitoring.

## Repository
GitHub Repo: [Auto-Media-Forward-asifalex03](https://github.com/RiyanMahmudbhai/Auto-Media-Forward-asifalex03)

## Installation

### 1. Clone the Repository
```sh
git clone https://github.com/RiyanMahmudbhai/Auto-Media-Forward-asifalex03.git
cd Auto-Media-Forward-asifalex03
```

### 2. Install Dependencies
```sh
pip3 install -r requirements.txt
```

### 3. Set Up Environment Variables
Create a `.env` file and add your **Telegram Bot Token**:
```sh
nano .env
```
Add the following:
```
BOT_TOKEN=your-telegram-bot-token
SOURCE_CHANNEL_ID=-100xxxxxxxxxx
DESTINATION_CHANNEL_ID=-100xxxxxxxxxx
```
Save and exit (`CTRL+X`, then `Y`, then `ENTER`).

### 4. Run the Bot
```sh
python3 main.py
```

## Deploy on a VPS
### 1. Connect to VPS
```sh
ssh username@your-vps-ip
```

### 2. Update and Install Dependencies
```sh
sudo apt update && sudo apt upgrade -y
sudo apt install python3 python3-pip git -y
```

### 3. Clone the Repository on VPS
```sh
git clone https://github.com/RiyanMahmudbhai/Auto-Media-Forward-asifalex03.git
cd Auto-Media-Forward-asifalex03
pip3 install -r requirements.txt
```

### 4. Configure Environment Variables
```sh
nano .env
```
Add your bot token and channel IDs:
```
BOT_TOKEN=your-telegram-bot-token
SOURCE_CHANNEL_ID=-100xxxxxxxxxx
DESTINATION_CHANNEL_ID=-100xxxxxxxxxx
```
Save and exit.

### 5. Run the Bot in the Background
#### Option 1: Using `screen`
```sh
screen -S telegram-bot
python3 main.py
```
To detach: `CTRL+A`, then `D`
To reattach: `screen -r telegram-bot`

#### Option 2: Using `systemd`
```sh
sudo nano /etc/systemd/system/telegram-bot22.service
```
Paste the following:
```
[Unit]
Description=Telegram Auto Forward Bot
After=network.target

[Service]
WorkingDirectory=/root/Auto-Media-Forward-asifalex03
ExecStart=/usr/bin/python3 /root/Auto-Media-Forward-asifalex03/main.py
Restart=always
User=root

[Install]
WantedBy=multi-user.target

```
Save and exit.

Enable and start the service:
```sh
sudo systemctl daemon-reload
sudo systemctl enable telegram-bot22
sudo systemctl start telegram-bot22
```
Check status:
```sh
sudo systemctl status telegram-bot22
```

## Usage
- Add the bot to both **source** and **destination** channels as an **admin**.
- The bot will **automatically forward video messages** from the **source channel** to the **destination channel**.
- You can monitor logs to see activity:
```sh
tail -f bot.log  # If using nohup logging
```

## License
MIT License

## Contributions
Feel free to submit pull requests or open issues.

## Contact
For any questions, reach out to Telegram - @asifalex2

