import unittest
import json

from imageio.image import ImageInfo, ImageIO


class TestImageIO(unittest.TestCase):
    def setUp(self):
        self.image_info = ImageInfo()
        self.image_info.name = "test_image"
        self.image_info.filename = "test_image.jpg"
        self.image_info.timestamp = 1633029442
        self.image_info.parameter = {
            "confidence": 0.5,
            "iou": 0.5,
            "hardware": "cpu",
            "agnostic_nms": True,
            "augment": False
        }

        self.image_io = ImageIO(self.image_info)
        self.image_io.write()

    def test_store(self):
        with open("images/images.json", "r", encoding="utf-8") as image_json:
            data = json.load(image_json)
            self.assertEqual(data["images"][0]["name"], self.image_info.name)
            self.assertEqual(data["images"][0]["filename"], self.image_info.filename)
            self.assertEqual(data["images"][0]["timestamp"], self.image_info.timestamp)
            self.assertEqual(data["images"][0]["parameter"], self.image_info.parameter)

    def tearDown(self) -> None:
        with open("images/images.json", "w", encoding="utf-8") as image_json:
            json.dump({"images": []}, image_json, indent=4)


if __name__ == '__main__':
    unittest.main()
