def color_label(label: str):
    if label == "cigarette":
        return (64, 0, 255), (255, 255, 255)

    if label == "smoke":
        return (0, 94, 255), (255, 255, 255)  # orange

    if label == "person":
        # return (0, 255, 200), (0, 0, 0)  # lime
        return (255, 65, 0), (255, 255, 255)  # blue

    return (0, 0, 0), (255, 255, 255)
