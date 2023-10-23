def color_label(label: str):
    """
    Generates a color tuple based on the given label.

    Parameters:
        label (str): The label for which to generate the color tuple.

    Returns:
        tuple: A color tuple representing the frame color and text color corresponding to the label.
        If the label is not found in the color dictionary, a default color tuple of red with white text is returned.
    """
    color_dict = {
        # Frame color is purple with white text
        "cigarette": ((64, 0, 255), (255, 255, 255)),
        # Frame color is sky blue with white text
        "smoke": ((0, 94, 255), (255, 255, 255)),
        # Frame color is orange with white text
        "person": ((255, 65, 0), (255, 255, 255))
    }

    # Frame color is red with white text if label not found
    return color_dict.get(label, ((255, 0, 0), (255, 255, 255)))
