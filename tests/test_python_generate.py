import importlib.util
import os
from pathlib import Path
import sys
import tempfile
import types
import unittest
from unittest.mock import Mock, patch


EXAMPLE = Path(__file__).resolve().parents[1] / "examples" / "python_generate.py"


class DownloadImagesTest(unittest.TestCase):
    def test_downloads_each_image_url_from_task_result(self):
        requests_stub = types.ModuleType("requests")
        requests_stub.get = Mock()
        requests_stub.post = Mock()
        response = Mock(content=b"synthetic image bytes")
        requests_stub.get.return_value = response

        with patch.dict(os.environ, {"APIMART_API_KEY": "synthetic-key"}), patch.dict(
            sys.modules, {"requests": requests_stub}
        ):
            spec = importlib.util.spec_from_file_location("python_generate", EXAMPLE)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

        task = {"result": {"images": [{"url": "https://example.invalid/output.png"}]}}
        with tempfile.TemporaryDirectory() as output_dir:
            saved = module.download_images(task, Path(output_dir))
            self.assertEqual(saved, [Path(output_dir) / "output.png"])
            self.assertEqual(saved[0].read_bytes(), b"synthetic image bytes")

        requests_stub.get.assert_called_once_with(
            "https://example.invalid/output.png", timeout=120
        )
        response.raise_for_status.assert_called_once_with()
        requests_stub.post.assert_not_called()


if __name__ == "__main__":
    unittest.main()
