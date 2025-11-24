# Telegram Communication Library

[![Run Telegram Unit Tests](https://github.com/puchkarev/telegram/actions/workflows/ci.yml/badge.svg)](https://github.com/puchkarev/telegram/actions/workflows/ci.yml)

This Python library provides a set of functions to interact with the Telegram Bot API. It allows you to send messages, files (images, videos, audio, documents, and animations), and retrieve updates from your Telegram bot.

The primary reason for this library is to simplify the overall interface and give capability to call this library from command line.

## Command Line Usage

You can use this library directly from the command line to interact with your Telegram bot.

### General Arguments

-   `--bot_token`: **Required**. Your Telegram bot's unique token.
-   `--chat_token`: The unique identifier for the target chat (required for sending messages/files).
-   `--message`: The text message or caption to send.

### Examples

**1. Send a Text Message:**

```bash
python tele.py --bot_token "YOUR_BOT_TOKEN" --chat_token "YOUR_CHAT_ID" --message "Hello from CLI!"
```

**2. Send an Image with Caption:**

```bash
python tele.py --bot_token "YOUR_BOT_TOKEN" --chat_token "YOUR_CHAT_ID" --image path/to/image.jpg --message "Check this out!"
```

**3. Send a Video:**

```bash
python tele.py --bot_token "YOUR_BOT_TOKEN" --chat_token "YOUR_CHAT_ID" --video path/to/video.mp4
```

**4. Send Multiple Files:**

```bash
python tele.py --bot_token "YOUR_BOT_TOKEN" --chat_token "YOUR_CHAT_ID" --image img1.jpg img2.png
```

**5. Get Updates:**

```bash
python tele.py --bot_token "YOUR_BOT_TOKEN" --updates 0
```

**6. Download a File:**

```bash
python tele.py --bot_token "YOUR_BOT_TOKEN" --fetch "FILE_ID_FROM_TELEGRAM"
```

### Available Flags

-   `--image`: Send one or more image files.
-   `--video`: Send one or more video files.
-   `--audio`: Send one or more audio files.
-   `--document`: Send one or more document files.
-   `--animation`: Send one or more animation files (GIFs).
-   `--file`: Send any arbitrary file (auto-detects type if possible).
-   `--updates`: Query updates from the bot. Pass `0` or the last update ID.
-   `--fetch`: Download a file from Telegram using its `file_id`.

## Functions

### `send_telegram(bot_token: str, chat_token: str, message: str) -> None`

Sends a text message to a specified Telegram chat.

-   **bot_token**: Your Telegram bot's unique token.
-   **chat_token**: The unique identifier for the target chat.
-   **message**: The text message to send.

### `send_telegram_file(bot_token: str, chat_token: str, filename: str, caption: str = "", timeout: int = None) -> None`

Sends a file to a specified Telegram chat. The file type is determined by its extension.

-   **bot_token**: Your Telegram bot's unique token.
-   **chat_token**: The unique identifier for the target chat.
-   **filename**: The local path to the file you want to send.
-   **caption**: (Optional) A caption for the file.
-   **timeout**: (Optional) The timeout in seconds for the request.

Supported file types:
-   Images: `.jpg`, `.jpeg`, `.png`
-   Videos: `.mp4`, `.webp`
-   Audio: `.mp3`
-   Animations: `.gif`
-   Documents: Any other file type.

### `get_telegram_file(bot_token: str, chat_token: str, file_id: str, FILES_DIR: str) -> str`

Downloads a file from Telegram using its `file_id`.

-   **bot_token**: Your Telegram bot's unique token.
-   **chat_token**: The unique identifier for the target chat.
-   **file_id**: The `file_id` of the file on Telegram's servers.
-   **FILES_DIR**: The local directory where the file will be saved.

Returns the filename of the downloaded file.

### `get_telegram_updates(bot_token: str, last_update: int) -> Dict[str, Any]`

Retrieves the latest updates for your bot.

-   **bot_token**: Your Telegram bot's unique token.
-   **last_update**: The ID of the last update you've processed.

Returns a dictionary containing the bot's updates.

### `telegram_set_commands(bot_token: str, commands: Dict[str, Any]) -> None`

Sets the list of commands for your bot.

-   **bot_token**: Your Telegram bot's unique token.
-   **commands**: A dictionary where keys are command names and values are their descriptions.
