import asyncio
import requests
import argparse
import os
import sys
import time
from typing import Dict, Any, List

def look_for(message: str, char: str, offset: int, max_offset: int) -> int:
    """
        Looks for a given char in the message looking back from
        offset with a maximum search back of max_offset. If
        found returns the index where it was found, if not returns -1.
        Args:
            message: message in which we look for the char
            char: a given character we are looking for
            offset: starting offset to look back from
            max_offset: how far back to look from offset
        Returns:
            An index in message where the char was found or -1 if not found.
    """
    for i in range(max_offset):
        if message[offset - i] == char:
            return offset - i
    return -1

def send_telegram(bot_token: str, chat_token: str, message: str) -> None:
    """
        Sends a given message via telegram from bot specified by bot_token,
        to a chat specified by chat_token.
        Args:
            bot_token: unique identifier for the telegram bot
            chat_token: unique identifier for a chat
            message: message to be sent
        Returns:
            Nothing
    """
    print(f"Sending to {chat_token}: {message}")
    chunk_size = 4090
    max_search_back = 2048
    min_size = 512
    start = 0
    while start < len(message):
        end = min(start + chunk_size, len(message)) - 1
        if start + chunk_size < len(message):
            search = look_for(message, '\n', end, min(max_search_back, end - start - min_size))
            if search < 0:
                search = look_for(message, ' ', end, min(max_search_back, end - start - min_size))
            if search > 0:
                end = search
        chunk = message[start:end + 1]
        start = end + 1

        try:
            url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
            data = {"chat_id": chat_token, "text": chunk}
            requests.post(url, data=data)
        except Exception as e:
            print(f"Error sending message: {e}")

async def _send_media_helper(bot_token: str, chat_token: str, file_path: str, caption: str, timeout: int, method_name: str, file_arg_name: str) -> None:
    """
    Private helper to send various media types to avoid code duplication.
    """
    media_type = method_name.split('_')[-1] # e.g. 'photo' from 'send_photo' or 'document' from 'send_document'
    # Actually, method_name passed will be 'send_photo', 'send_video' etc.
    # Cleaner to just use method_name for logging? No, let's use file path.
    print(f"Sending {media_type} to {chat_token}: {file_path} {caption}")
    try:
        from telegram.ext import Application
        application = Application.builder().token(bot_token).build()

        method = getattr(application.bot, method_name)
        
        with open(file_path, 'rb') as f:
            # Construct arguments dynamically
            kwargs = {
                'chat_id': chat_token,
                'caption': caption,
                'read_timeout': timeout,
                'write_timeout': timeout,
                file_arg_name: f
            }
            await method(**kwargs)
        print(f"{media_type.capitalize()} {file_path} sent successfully!")
    except FileNotFoundError:
        print(f"Error: {media_type.capitalize()} file not found at \"{file_path}\"")
    except Exception as e:
        print(f"Error sending {media_type}: {e}")

async def send_telegram_image(bot_token: str, chat_token: str, image_path: str, caption: str = "", timeout: int = None) -> None:
    """
        Sends a given image via telegram from bot specified by bot_token,
        to a chat specified by chat_token.
        Args:
            bot_token: unique identifier for the telegram bot
            chat_token: unique identifier for a chat
            image_path: path to the image file to send
            caption: caption to associate with the image
            timeout: timeout in seconds how long to attempt to send
        Returns:
            Nothing
    """
    await _send_media_helper(bot_token, chat_token, image_path, caption, timeout, 'send_photo', 'photo')

async def send_telegram_video(bot_token: str, chat_token: str, video_path: str, caption: str = "", timeout: int = None) -> None:
    """
        Sends a given video via telegram from bot specified by bot_token,
        to a chat specified by chat_token.
        Args:
            bot_token: unique identifier for the telegram bot
            chat_token: unique identifier for a chat
            video_path: path to the video file to send
            caption: caption to associate with the image
            timeout: timeout in seconds how long to attempt to send
        Returns:
            Nothing
    """
    await _send_media_helper(bot_token, chat_token, video_path, caption, timeout, 'send_video', 'video')

async def send_telegram_audio(bot_token: str, chat_token: str, audio_path: str, caption: str = "", timeout: int = None) -> None:
    """
        Sends a given audio via telegram from bot specified by bot_token,
        to a chat specified by chat_token.
        Args:
            bot_token: unique identifier for the telegram bot
            chat_token: unique identifier for a chat
            audio_path: path to the audio file to send
            caption: caption to associate with the image
            timeout: timeout in seconds how long to attempt to send
        Returns:
            Nothing
    """
    await _send_media_helper(bot_token, chat_token, audio_path, caption, timeout, 'send_audio', 'audio')

async def send_telegram_animation(bot_token: str, chat_token: str, animation_path: str, caption: str = "", timeout: int = None) -> None:
    """
        Sends a given animation via telegram from bot specified by bot_token,
        to a chat specified by chat_token.
        Args:
            bot_token: unique identifier for the telegram bot
            chat_token: unique identifier for a chat
            animation_path: path to the animation file to send
            caption: caption to associate with the file
            timeout: timeout in seconds how long to attempt to send
        Returns:
            Nothing
    """
    await _send_media_helper(bot_token, chat_token, animation_path, caption, timeout, 'send_animation', 'animation')

async def send_telegram_document(bot_token: str, chat_token: str, document_path: str, caption: str = "", timeout: int = None) -> None:
    """
        Sends a given document via telegram from bot specified by bot_token,
        to a chat specified by chat_token.
        Args:
            bot_token: unique identifier for the telegram bot
            chat_token: unique identifier for a chat
            document_path: path to the document file to send
            caption: caption to associate with the file
            timeout: timeout in seconds how long to attempt to send
        Returns:
            Nothing
    """
    await _send_media_helper(bot_token, chat_token, document_path, caption, timeout, 'send_document', 'document')

def send_telegram_file(bot_token: str, chat_token: str, filename: str, caption: str = "", timeout: int = None) -> None:
    """
        Sends a given file via telegram from bot specified by bot_token,
        to a chat specified by chat_token.
        Args:
            bot_token: unique identifier for the telegram bot
            chat_token: unique identifier for a chat
            filename: path to the file to send
            caption: caption to associate with the image
            timeout: timeout in seconds how long to attempt to send
        Returns:
            Nothing
    """
    file_name = os.path.basename(filename)
    if caption == "":
        caption = file_name
    if filename.lower().endswith(".mp3"):
        asyncio.run(send_telegram_audio(bot_token, chat_token, filename, caption, timeout))
    elif filename.lower().endswith(".mp4") or filename.lower().endswith(".webp"):
        asyncio.run(send_telegram_video(bot_token, chat_token, filename, caption, timeout))
    elif filename.lower().endswith(".jpg") or filename.lower().endswith(".jpeg") or filename.lower().endswith(".png"):
        asyncio.run(send_telegram_image(bot_token, chat_token, filename, caption, timeout))
    elif filename.lower().endswith(".gif"):
        asyncio.run(send_telegram_animation(bot_token, chat_token, filename, caption, timeout))
    else:
        asyncio.run(send_telegram_document(bot_token, chat_token, filename, caption, timeout))

def get_telegram_file(bot_token: str, chat_token: str, file_id: str, FILES_DIR: str) -> str:
    """
        Retrieves a given file from telegram and stores it in FIlES_DIR.
        Args:
            bot_token: unique identifier for the telegram bot
            chat_token: unique identifier for a chat
            file_id: telegram file identifier
            FILES_DIR: location where to store the file
        Returns:
            filename of the file that was stored in the FILES_DIR
    """
    telegram_link = f"https://api.telegram.org/bot{bot_token}/getFile?file_id={file_id}"
    telegram_response = requests.get(telegram_link)
    response = telegram_response.json()

    if not response["ok"]:
        print("error with response", response)
        if chat_token and len(chat_token) > 0:
            send_telegram(bot_token, chat_token, "Error getting image")
        else:
            print("Error getting image")
        return ""

    telegram_link = f"https://api.telegram.org/file/bot{bot_token}/{response['result']['file_path']}"
    telegram_response = requests.get(telegram_link)
    print("telegram response", response)

    if telegram_response.status_code != 200:
        print("Telegram is unhappy", telegram_response)
        if chat_token and len(chat_token) > 0:
            send_telegram(bot_token, chat_token, "Error fetching image")
        return ""

    filename, file_extension = os.path.splitext(response['result']['file_path'])
    unique_id = response['result']['file_unique_id']
    filename = f"{int(time.time()*1000)}{file_extension}"
    out_path = os.path.join(FILES_DIR, filename)
    with open(out_path, "wb") as f:
        f.write(telegram_response.content)
    print(f"Fetched {unique_id} from telegram. Stored as {out_path}")
    return filename


def telegram_set_commands(bot_token: str, commands: Dict[str, Any]) -> None:
    """
        Sets the commands available on a given bot to telegram.
        Args:
            bot_token: bot for which we set commands
            commands: mapping from the command to a description.
        Returns:
            Nothing
    """
    import telegram
    commands_dict = []
    for command_name in commands.keys():
        commands_dict.append(telegram.BotCommand(command_name, commands[command_name]))

    try:
        asyncio.run(telegram.Bot(token = bot_token).set_my_commands(commands_dict))
        print(f"Commands have been successfully set with {commands.keys()}")
    except telegram.error.TelegramError as e:
        print(f'Error setting commands: {e}')

def get_telegram_updates(bot_token: str, last_update: int) -> Dict[str, Any]:
    """
        Retrieves the latest updates from telegram.
        Args:
            bot_token: unique identifier for the telegram bot
            last_update: the index of the update that was last processed.
        Returns:
            A json structure with the updates from telegram
    """
    url = f"https://api.telegram.org/bot{bot_token}/getUpdates"
    if last_update > 0:
        url = url + "?offset=" + str(last_update + 1)
    response = requests.get(url)
    updates = response.json()
    return updates

def main(argv=None):
    parser = argparse.ArgumentParser(description="Send a telegram message in a chat")
    parser.add_argument("--message", type=str, default="", help="message to send")
    parser.add_argument("--bot_token", type=str, default="", help="bot token for telegram")
    parser.add_argument("--chat_token", type=str, default="", help="chat token for telegram")
    parser.add_argument("--image", action='extend', nargs='+', help="image file to send")
    parser.add_argument("--video", action='extend', nargs='+', help="video file to send")
    parser.add_argument("--audio", action='extend', nargs='+', help="audio file to send")
    parser.add_argument("--document", action='extend', nargs='+', help="document file to send")
    parser.add_argument("--animation", action='extend', nargs='+', help="animation file to send")
    parser.add_argument("--file", action='extend', nargs='+', help="arbitrary file to send")
    parser.add_argument("--updates", type=int, default=0, help="query updates from bot")
    parser.add_argument("--fetch", type=str, default="", help="fetches a telegram file")
    args = parser.parse_args(argv)

    if args.bot_token == "":
        print("must specify bot token")
        sys.exit(-1)

    updates = get_telegram_updates(args.bot_token, args.updates)
    if "result" in updates and len(updates["result"]) > 0:
        print("Updates: ", updates)

    if args.fetch and len(args.fetch) > 0:
        get_telegram_file(args.bot_token, "", args.fetch, "./")

    sent = False
    
    # List of (argument_values, function_to_call, timeout)
    media_actions = [
        (args.image, send_telegram_image, 60),
        (args.video, send_telegram_video, 180),
        (args.audio, send_telegram_audio, 60),
        (args.document, send_telegram_document, 120),
        (args.animation, send_telegram_animation, 120)
    ]

    for media_list, func, timeout in media_actions:
        if media_list:
            for item in media_list:
                message = args.message
                if not message:
                    message = item
                asyncio.run(func(args.bot_token, args.chat_token, item, message, timeout=timeout))
                sent = True

    if args.file:
        for file in args.file:
            message = args.message
            if not message:
                message = file
            send_telegram_file(args.bot_token, args.chat_token, file, message, timeout=360)
            sent = True

    if not sent and len(args.message) > 0:
        send_telegram(args.bot_token, args.chat_token, args.message)

if __name__ == "__main__":
    main(sys.argv[1:])

