# Call of Dragons Bot

This project is a bot designed to automate tasks in the game "Call of Dragons" using an Android emulator. The bot interacts with the emulator to perform various in-game actions, enhancing the gaming experience through automation.

## Project Structure

```
call-of-dragons-bot
├── src
│   ├── bot.py               # Main entry point for the bot
│   ├── emulator
│   │   └── controller.py    # Handles interactions with the Android emulator
│   └── tasks
│       └── task_manager.py   # Manages the tasks the bot will perform
├── requirements.txt         # Lists the project dependencies
└── README.md                # Project documentation
```

## Setup Instructions

1. **Clone the repository:**
   ```
   git clone https://github.com/yourusername/call-of-dragons-bot.git
   cd call-of-dragons-bot
   ```

2. **Install dependencies:**
   Ensure you have Python installed, then run:
   ```
   pip install -r requirements.txt
   ```

3. **Configure the Android Emulator:**
   Make sure you have an Android emulator set up and configured on your machine. You may need to adjust settings in the `controller.py` file to match your emulator's configuration.

## Usage Guidelines

1. **Run the bot:**
   To start the bot, execute the following command:
   ```
   python src/bot.py
   ```

2. **Task Management:**
   You can add tasks to the bot by modifying the `task_manager.py` file. The bot will execute these tasks in the order they are added.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any suggestions or improvements.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.