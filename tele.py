import asyncio
import requests
import argparse
import os
import sys
import time
import json
from typing import Dict, Any, List, Union, Callable

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
    print(f"Sending to {bot_token} {chat_token}: {message}")
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
    print(f"Sending image to {chat_token}: {image_path} {caption}")
    try:
        from telegram.ext import Application
        application = Application.builder().token(bot_token).build()

        with open(image_path, 'rb') as image_file:
            await application.bot.send_photo(chat_id=chat_token, photo=image_file, caption=caption, read_timeout=timeout, write_timeout=timeout)
        print(f"Image {image_path} sent successfully!")
    except FileNotFoundError:
        print(f"Error: Image file not found at \"{image_path}\"")
    except Exception as e:
        print(f"Error sending image: {e}")

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
    print(f"Sending video to {chat_token}: {video_path} {caption}")
    try:
        from telegram.ext import Application
        application = Application.builder().token(bot_token).build()

        with open(video_path, 'rb') as video_file:
            await application.bot.send_video(chat_id=chat_token, video=video_file, caption=caption, read_timeout=timeout, write_timeout=timeout)
        print(f"Video {video_path} sent successfully!")
    except FileNotFoundError:
        print(f"Error: Video file not found at {video_path}")
    except Exception as e:
        print(f"Error sending video: {e}")

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
    print(f"Sending audio to {chat_token}: {audio_path} {caption}")
    try:
        from telegram.ext import Application
        application = Application.builder().token(bot_token).build()

        with open(audio_path, 'rb') as audio_file:
            await application.bot.send_audio(chat_id=chat_token, audio=audio_file, caption=caption, read_timeout=timeout, write_timeout=timeout)
        print(f"Audio {audio_path} sent successfully!")
    except FileNotFoundError:
        print(f"Error: Audio file not found at {audio_path}")
    except Exception as e:
        print(f"Error sending audio: {e}")

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
    print(f"Sending animation to {chat_token}: {animation_path} {caption}")
    try:
        from telegram.ext import Application
        application = Application.builder().token(bot_token).build()

        with open(animation_path, 'rb') as animation_file:
            await application.bot.send_animation(chat_id=chat_token, animation=animation_file, caption=caption, read_timeout=timeout, write_timeout=timeout)
        print(f"Animation {animation_path} sent successfully!")
    except FileNotFoundError:
        print(f"Error: Animation file not found at {animation_path}")
    except Exception as e:
        print(f"Error sending animation: {e}")

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
    print(f"Sending document to {chat_token}: {document_path} {caption}")
    try:
        from telegram.ext import Application
        application = Application.builder().token(bot_token).build()

        with open(document_path, 'rb') as document_file:
            await application.bot.send_document(chat_id=chat_token, document=document_file, caption=caption, read_timeout=timeout, write_timeout=timeout)
        print(f"Document {document_path} sent successfully!")
    except FileNotFoundError:
        print(f"Error: Document file not found at {document_path}")
    except Exception as e:
        print(f"Error sending document: {e}")

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
        print(f"Commands have been successfully set to {bot_token} with {commands.keys()}")
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

if __name__ == "__main__":
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
    args = parser.parse_args()

    if args.bot_token == "":
        print("must specify bot token")
        sys.exit(-1)

    updates = get_telegram_updates(args.bot_token, args.updates)
    if "result" in updates and len(updates["result"]) > 0:
        print("Updates: ", updates)

    if args.fetch and len(args.fetch) > 0:
        get_telegram_file(args.bot_token, "", args.fetch, "./")

    sent = False
    if args.image:
        for image in args.image:
            message = args.message
            if not message:
                message = image
            asyncio.run(send_telegram_image(args.bot_token, args.chat_token, image, message, timeout=60))
            sent = True

    if args.video:
        for video in args.video:
            message = args.message
            if not message:
                message = video
            asyncio.run(send_telegram_video(args.bot_token, args.chat_token, video, message, timeout=180))
            sent = True

    if args.audio:
        for audio in args.audio:
            message = args.message
            if not message:
                message = audio
            asyncio.run(send_telegram_audio(args.bot_token, args.chat_token, audio, message, timeout=60))
            sent = True

    if args.document:
        for document in args.document:
            message = args.message
            if not message:
                message = document
            asyncio.run(send_telegram_document(args.bot_token, args.chat_token, document, message, timeout=120))
            sent = True

    if args.animation:
        for animation in args.animation:
            message = args.message
            if not message:
                message = animation
            asyncio.run(send_telegram_document(args.bot_token, args.chat_token, animation, message, timeout=120))
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

