Here’s a summarized guide for deploying your bot on any VPS:

---

### **Step-by-Step Guide: Deploy Auto Media Forward Bot**

---

#### **1. Set Up the VPS**
1. **Update the system**:
   ```bash
   sudo apt update && sudo apt upgrade -y
   ```
2. **Install Python and pip**:
   ```bash
   sudo apt install python3 python3-pip python3-venv -y
   ```

---

#### **2. Clone the Repository**
1. **Install Git (if not already installed)**:
   ```bash
   sudo apt install git -y
   ```
2. **Clone the repository**:
   ```bash
   git clone https://github.com/your-repo/Auto-Media-Forward-Bot.git
   ```
3. **Navigate to the project directory**:
   ```bash
   cd Auto-Media-Forward-Bot
   ```

---

#### **3. Set Up a Virtual Environment**
1. **Create and activate a virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

---

#### **4. Configure the Bot**
1. **Create a `.env` file**:
   ```bash
   nano .env
   ```
2. **Add the following environment variables**:
   ```env
   API_HASH=your_api_hash
   API_ID=your_api_id
   BOT_TOKEN=your_bot_token
   CHANNEL_ID=source_channel:destination_channel
   AS_COPY=True  # Optional: Use True/False based on your requirements
   ```
3. **Save and exit**: Press `Ctrl + O`, then `Enter`, and `Ctrl + X`.

---

#### **5. Test the Bot**
1. **Run the bot manually to ensure it works**:
   ```bash
   python3 bot.py
   ```
2. **Verify that the bot forwards media messages as expected.

---

#### **6. Set Up Persistent Running with `systemd`**
1. **Create a `systemd` service file**:
   ```bash
   sudo nano /etc/systemd/system/media-forward-bot.service
   ```
2. **Add the following content**:
   ```ini
   [Unit]
   Description=Telegram Media Forward Bot
   After=network.target

   [Service]
   User=root
   WorkingDirectory=/path/to/Auto-Media-Forward-Bot
   ExecStart=/path/to/Auto-Media-Forward-Bot/venv/bin/python3 bot.py
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```
   Replace `/path/to/Auto-Media-Forward-Bot` with the actual path to the cloned repository.

3. **Reload and start the service**:
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable media-forward-bot
   sudo systemctl start media-forward-bot
   ```
4. **Check the service status**:
   ```bash
   sudo systemctl status media-forward-bot
   ```

---

#### **7. Monitor Logs**
To check the logs in real-time:
```bash
journalctl -u media-forward-bot.service -f
```

---

### **Final Notes**
- The bot will now run persistently and restart automatically on crashes or system reboots.
- For future deployments, just follow these steps and replace the environment variables with the appropriate values.

---

Would you like me to save this note as a text file for easy access?
