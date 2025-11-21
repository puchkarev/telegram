import unittest
from unittest.mock import patch, MagicMock
import os
import sys
import submodules.telegram.tele as tele

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
    def test_get_telegram_updates(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = {"ok": True, "result": []}
        mock_get.return_value = mock_response

        updates = tele.get_telegram_updates("bot_token", 0)
        self.assertEqual(updates, {"ok": True, "result": []})
        mock_get.assert_called_with("https://api.telegram.org/botbot_token/getUpdates")

    @patch('submodules.telegram.tele.asyncio.run')
    def test_send_telegram_file_image(self, mock_asyncio_run):
        tele.send_telegram_file("bot_token", "chat_token", "image.jpg")
        mock_asyncio_run.assert_called()

    @patch('submodules.telegram.tele.asyncio.run')
    def test_send_telegram_file_video(self, mock_asyncio_run):
        tele.send_telegram_file("bot_token", "chat_token", "video.mp4")
        mock_asyncio_run.assert_called()

    @patch('submodules.telegram.tele.asyncio.run')
    def test_send_telegram_file_audio(self, mock_asyncio_run):
        tele.send_telegram_file("bot_token", "chat_token", "audio.mp3")
        mock_asyncio_run.assert_called()
    
    @patch('submodules.telegram.tele.asyncio.run')
    def test_send_telegram_file_animation(self, mock_asyncio_run):
        tele.send_telegram_file("bot_token", "chat_token", "animation.gif")
        mock_asyncio_run.assert_called()

    @patch('submodules.telegram.tele.asyncio.run')
    def test_send_telegram_file_document(self, mock_asyncio_run):
        tele.send_telegram_file("bot_token", "chat_token", "document.txt")
        mock_asyncio_run.assert_called()

    @patch('submodules.telegram.tele.get_telegram_updates', return_value={"ok": True, "result": []})
    @patch('submodules.telegram.tele.send_telegram')
    def test_main_message(self, mock_send_telegram, mock_get_updates):
        tele.main(['--message', 'test message', '--bot_token', 'bot_token', '--chat_token', 'chat_token'])
        mock_send_telegram.assert_called_with("bot_token", "chat_token", "test message")

if __name__ == '__main__':
    unittest.main()
