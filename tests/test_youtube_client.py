import unittest
from types import SimpleNamespace
from unittest.mock import Mock, patch

from pytubefix.exceptions import BotDetection

from download import App, TRANSLATIONS


class YoutubeClientTests(unittest.TestCase):
    def make_app(self):
        callbacks = []

        def after(delay, callback, *args):
            callbacks.append((callback, args))

        app = SimpleNamespace(
            texts=TRANSLATIONS["en"],
            after=after,
            update_status=Mock(),
            update_progress=Mock(),
            update_progress_label_only=Mock(),
            enable_widgets=Mock(),
            progress_bar=SimpleNamespace(set=Mock()),
            progress_callback=Mock(),
            _update_ui_after_fetch=App._update_ui_after_fetch,
        )
        return app, callbacks

    def test_url_check_uses_web_and_reports_bot_detection(self):
        app, callbacks = self.make_app()
        url = "https://www.youtube.com/watch?v=test"
        with patch("download.YouTube", side_effect=BotDetection("test")) as youtube:
            App._fetch_qualities_task(app, url)

        youtube.assert_called_once_with(url, client="WEB")
        self.assertEqual(callbacks[0][0], App._update_ui_after_fetch)
        self.assertEqual(callbacks[0][1][1], app.texts["status_bot_detection"])

    def test_single_download_uses_web_and_reports_bot_detection(self):
        app, callbacks = self.make_app()
        url = "https://www.youtube.com/watch?v=test"
        with patch("download.YouTube", side_effect=BotDetection("test")) as youtube:
            result = App._execute_single_download(app, url, "C:\\Downloads", "audio", "")

        self.assertFalse(result)
        youtube.assert_called_once_with(url, client="WEB", on_progress_callback=app.progress_callback)
        self.assertIn((app.update_status, (app.texts["status_bot_detection"], "red")), callbacks)

    def test_batch_search_uses_web_and_video_results(self):
        app, callbacks = self.make_app()
        video = SimpleNamespace(watch_url="https://www.youtube.com/watch?v=test", title="Test")
        app._execute_single_download = Mock(return_value=True)

        with patch("download.Search", return_value=SimpleNamespace(videos=[video])) as search:
            App._batch_download_task(app, ["test query"], "C:\\Downloads", "audio")

        search.assert_called_once_with("test query", client="WEB")
        app._execute_single_download.assert_called_once_with(
            video.watch_url, "C:\\Downloads", "audio", "", video, 1, 1
        )
        self.assertIn((app.update_status, (app.texts["batch_complete"].format(success=1, fail=0), "green")), callbacks)

    def test_batch_video_uses_adaptive_quality_when_no_progressive_mp4(self):
        app, _ = self.make_app()
        app._execute_single_download = Mock(return_value=True)
        progressive = Mock()
        progressive.order_by.return_value.desc.return_value = []
        adaptive = Mock()
        adaptive.order_by.return_value.desc.return_value = [
            SimpleNamespace(resolution="144p")
        ]
        audio = Mock()
        audio.first.return_value = object()
        streams = Mock()
        streams.filter.side_effect = [progressive, audio, adaptive]
        video = SimpleNamespace(
            watch_url="https://www.youtube.com/watch?v=test",
            title="Test", streams=streams,
        )

        with patch("download.Search", return_value=SimpleNamespace(videos=[video])):
            App._batch_download_task(app, ["test query"], "C:\\Downloads", "video")

        app._execute_single_download.assert_called_once_with(
            video.watch_url, "C:\\Downloads", "video", "144p", video, 1, 1
        )

    def test_batch_stops_after_bot_detection(self):
        app, callbacks = self.make_app()
        with patch("download.Search", side_effect=BotDetection("test")) as search:
            App._batch_download_task(app, ["first", "second"], "C:\\Downloads", "audio")

        search.assert_called_once_with("first", client="WEB")
        self.assertIn((app.update_status, (app.texts["status_bot_detection"], "red")), callbacks)

    def test_bot_messages_fit_status_label(self):
        for language, texts in TRANSLATIONS.items():
            with self.subTest(language=language):
                self.assertLessEqual(len(texts["status_bot_detection"]), 80)


if __name__ == "__main__":
    unittest.main()
