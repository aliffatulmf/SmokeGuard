from datetime import datetime


class ImageMetadata:
    def __init__(self, image_data=None, image_name=None, confidence_score=None, image_timestamp: datetime=None):
        self.image_data = image_data
        self.image_name = image_name
        self.confidence_score = round(confidence_score, 4)
        self.image_timestamp: datetime = image_timestamp

    def get(self, attribute_key):
        if hasattr(self, attribute_key) and not callable(getattr(self, attribute_key)):
            return getattr(self, attribute_key)
        else:
            raise AttributeError(f"Attribute {attribute_key} not found or it's a method")