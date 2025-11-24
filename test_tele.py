import unittest
from unittest.mock import patch, MagicMock, call
import os
import sys
import tele

class TestTele(unittest.TestCase):

    def test_look_for(self):
        message = "hello world"
        self.assertEqual(tele.look_for(message, " ", 5, 5), 5)
        self.assertEqual(tele.look_for(message, "o", 10, 5), 7)
        self.assertEqual(tele.look_for(message, "z", 10, 10), -1)

    @patch('requests.post')
    def test_send_telegram(self, mock_post):
        tele.send_telegram("bot_token", "chat_token", "test message")
        mock_post.assert_called_with(
            "https://api.telegram.org/botbot_token/sendMessage",
            data={"chat_id": "chat_token", "text": "test message"}
        )

    @patch('requests.post')
    def test_send_telegram_chunking(self, mock_post):
        # Create a message longer than chunk_size (4090)
        # We'll use a message with 5000 'a's
        long_message = "a" * 5000
        tele.send_telegram("bot_token", "chat_token", long_message)
        
        # Should be called twice
        self.assertEqual(mock_post.call_count, 2)
        
        # Verify first chunk
        first_call_args = mock_post.call_args_list[0]
        self.assertEqual(first_call_args[1]['data']['text'], "a" * 4090)
        
        # Verify second chunk
        second_call_args = mock_post.call_args_list[1]
        self.assertEqual(second_call_args[1]['data']['text'], "a" * (5000 - 4090))

    @patch('requests.get')
    def test_get_telegram_file(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "ok": True,
            "result": {
                "file_path": "path/to/file.jpg",
                "file_unique_id": "unique_id"
            }
        }
        mock_response.status_code = 200
        mock_response.content = b"file content"
        mock_get.return_value = mock_response

        with patch('builtins.open', unittest.mock.mock_open()) as mock_open:
            filename = tele.get_telegram_file("bot_token", "chat_token", "file_id", ".")
            self.assertTrue(filename.endswith(".jpg"))
            mock_open.assert_called_once()

    @patch('requests.get')
    def test_get_telegram_file_error(self, mock_get):
        mock_response = MagicMock()
        # Simulate Telegram API error response
        mock_response.json.return_value = {"ok": False, "description": "Bad Request"}
        mock_get.return_value = mock_response

        # Suppress print output for cleaner test run
        with patch('builtins.print'):
            filename = tele.get_telegram_file("bot_token", "chat_token", "bad_file_id", ".")
            self.assertEqual(filename, "")

    @patch('requests.get')
    def test_get_telegram_updates(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = {"ok": True, "result": []}
        mock_get.return_value = mock_response

        updates = tele.get_telegram_updates("bot_token", 0)
        self.assertEqual(updates, {"ok": True, "result": []})
        mock_get.assert_called_with("https://api.telegram.org/botbot_token/getUpdates")

    @patch('tele.asyncio.run')
    def test_send_telegram_file_image(self, mock_asyncio_run):
        tele.send_telegram_file("bot_token", "chat_token", "image.jpg")
        mock_asyncio_run.assert_called()

    @patch('tele.asyncio.run')
    def test_send_telegram_file_video(self, mock_asyncio_run):
        tele.send_telegram_file("bot_token", "chat_token", "video.mp4")
        mock_asyncio_run.assert_called()

    @patch('tele.asyncio.run')
    def test_send_telegram_file_audio(self, mock_asyncio_run):
        tele.send_telegram_file("bot_token", "chat_token", "audio.mp3")
        mock_asyncio_run.assert_called()
    
    @patch('tele.asyncio.run')
    def test_send_telegram_file_animation(self, mock_asyncio_run):
        tele.send_telegram_file("bot_token", "chat_token", "animation.gif")
        mock_asyncio_run.assert_called()

    @patch('tele.asyncio.run')
    def test_send_telegram_file_document(self, mock_asyncio_run):
        tele.send_telegram_file("bot_token", "chat_token", "document.txt")
        mock_asyncio_run.assert_called()

    @patch('tele.get_telegram_updates', return_value={"ok": True, "result": []})
    @patch('tele.send_telegram')
    def test_main_message(self, mock_send_telegram, mock_get_updates):
        tele.main(['--message', 'test message', '--bot_token', 'bot_token', '--chat_token', 'chat_token'])
        mock_send_telegram.assert_called_with("bot_token", "chat_token", "test message")

    @patch('tele.get_telegram_updates', return_value={"ok": True, "result": []})
    @patch('tele.send_telegram_file')
    @patch('tele.send_telegram_image')
    def test_main_file_args(self, mock_send_telegram_image, mock_send_telegram_file, mock_get_updates):
        # Mock the async function to return a magic mock (which acts as the coroutine)
        # We need to make sure we don't get unawaited coroutine warnings if we can help it, 
        # but pure mocks usually don't trigger it unless we return a real coroutine.
        # Since send_telegram_image is async, main calls asyncio.run(send_telegram_image(...))
        # Wait, main calls asyncio.run(send_telegram_image(...)).
        # We need to mock asyncio.run as well? 
        # No, send_telegram_image is defined in tele.py. If we mock it, we replace the function.
        # If we replace the function with a standard Mock, asyncio.run(Mock()) will fail because Mock is not awaitable.
        # So we need to mock asyncio.run inside main, OR make our mock awaitable.
        pass

    @patch('tele.asyncio.run')
    @patch('tele.get_telegram_updates', return_value={"ok": True, "result": []})
    @patch('tele.send_telegram_file')
    @patch('tele.send_telegram_image')
    def test_main_with_image(self, mock_send_image, mock_send_file, mock_get_updates, mock_asyncio_run):
        tele.main(['--image', 'test.jpg', '--bot_token', 'bot_token', '--chat_token', 'chat_token'])
        # main calls: asyncio.run(send_telegram_image(...))
        # send_telegram_image is now a Mock. 
        # asyncio.run is now a Mock.
        # It should verify that send_telegram_image was called (passed to asyncio.run is harder to verify without side effects)
        # Actually, main calls: asyncio.run(send_telegram_image(args.bot_token, args.chat_token, image, message, timeout=60))
        # This executes the function call send_telegram_image(...) *before* passing result to asyncio.run.
        # So checking mock_send_image.assert_called_with(...) is correct.
        mock_send_image.assert_called_with("bot_token", "chat_token", "test.jpg", "test.jpg", timeout=60)
        mock_send_file.assert_not_called()

    @patch('tele.get_telegram_updates', return_value={"ok": True, "result": []})
    @patch('tele.send_telegram_file')
    def test_main_with_file(self, mock_send_file, mock_get_updates):
        tele.main(['--file', 'test.txt', '--bot_token', 'bot_token', '--chat_token', 'chat_token'])
        mock_send_file.assert_called_with("bot_token", "chat_token", "test.txt", "test.txt", timeout=360)

    @patch('tele.asyncio.run')
    @patch('telegram.Bot')
    def test_telegram_set_commands(self, mock_bot_cls, mock_asyncio_run):
        mock_bot = MagicMock()
        mock_bot_cls.return_value = mock_bot
        # Mock the async method set_my_commands. 
        # Since it's awaited in the source, we need to handle it.
        # But here asyncio.run is mocked, so we just check if the coroutine was created/passed.
        
        commands = {"start": "Start bot", "help": "Get help"}
        tele.telegram_set_commands("bot_token", commands)
        
        # Verify Bot initialized
        mock_bot_cls.assert_called_with(token="bot_token")
        
        # Verify asyncio.run called
        mock_asyncio_run.assert_called()


if __name__ == '__main__':
    unittest.main()