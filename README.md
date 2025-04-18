# Contest Notification Discord Bot

A Discord bot that fetches programming contest information from Clist.by and sends notifications before contests start.

## Features

-   Fetches upcoming contests from Clist.by API
-   Sends notifications at 2 hours, 1 hour, and 10 minutes before contests start
-   Displays upcoming contests with the `!upcoming` command
-   Allows administrators to set the notification channel

## Setup Instructions

### Prerequisites

-   Python 3.8 or higher
-   A Discord bot token
-   Clist.by API credentials

### Installation

1. Clone this repository or download the bot code

2. Install required dependencies:

    ```
    pip install discord.py requests python-dotenv
    ```

3. Create a `.env` file in the same directory as the bot script with the following content:
    ```
    DISCORD_TOKEN=your_discord_bot_token
    CLIST_USERNAME=your_clist_username
    CLIST_API_KEY=your_clist_api_key
    NOTIFICATION_CHANNEL_ID=your_default_channel_id
    ```

### Getting API Credentials

1. **Discord Bot Token**:

    - Go to the [Discord Developer Portal](https://discord.com/developers/applications)
    - Create a new application
    - Navigate to the "Bot" tab and click "Add Bot"
    - Under the bot's token section, click "Copy" to get your token
    - Make sure to enable the "Message Content Intent" under Privileged Gateway Intents

2. **Clist.by API Credentials**:
    - Register for an account on [Clist.by](https://clist.by)
    - Go to your profile and find the API section
    - Generate an API key if you don't have one

### Inviting the Bot to Your Server

1. In the Discord Developer Portal, go to the "OAuth2" tab
2. In the URL Generator, select the "bot" scope and the following permissions:
    - Read Messages/View Channels
    - Send Messages
    - Embed Links
3. Copy the generated URL and open it in your browser
4. Select the server where you want to add the bot and confirm

## Usage

### Bot Commands

-   `!upcoming [count]`: Shows a list of upcoming contests. You can specify the number of contests to display (default: 5).
-   `!setnotificationchannel`: Sets the current channel as the notification channel (requires administrator permissions).

### Notifications

The bot will automatically send notifications at the following times before each contest:

-   2 hours before
-   1 hour before
-   10 minutes before

Each notification includes:

-   Contest name
-   Platform
-   Duration
-   Start time
-   Link to the contest

## Customization

You can modify the notification times by changing the `NOTIFICATION_TIMES` list in the code.

## Troubleshooting

-   If the bot is not sending notifications, ensure it has permissions to send messages in the notification channel.
-   If you're not receiving contest data, check your Clist.by API credentials and ensure your account has access to the API.
-   The bot checks for new contests every 30 minutes and sends notifications on a 1-minute cycle.

## Contributing

Feel free to submit issues or pull requests if you have suggestions for improvements!
