class ColorLabel:
    def __init__(self):
        """
        Initializes a new instance of the ColorLabel class.
        """
        self.color_dict = {
            # Frame color is purple with white text
            "cigarette": ((64, 0, 255), (255, 255, 255)),
            # Frame color is sky blue with white text
            "smoke": ((0, 94, 255), (255, 255, 255)),
            # Frame color is orange with white text
            "person": ((255, 65, 0), (255, 255, 255)),
        }

    def register_color(
        self, label: str, frame_color: tuple, text_color: tuple = (255, 255, 255)
    ):
        """
        Registers a new color associated with the given label.

        Parameters:
            label (str): The label for which to register the color.
            frame_color (tuple): The frame color.
            text_color (tuple): The text color.
        """
        self.color_dict[label] = (frame_color, text_color)

    def get_color(self, label: str) -> tuple:
        """
        Generates a color tuple based on the given label.

        Parameters:
            label (str): The label for which to generate the color tuple.

        Returns:
            tuple: A color tuple representing the frame color and text color corresponding to the label.
            If the label is not found in the color dictionary, a default color tuple of red with white text is returned.
        """
        # Frame color is red with white text if label not found
        return self.color_dict.get(label, ((255, 0, 0), (255, 255, 255)))
