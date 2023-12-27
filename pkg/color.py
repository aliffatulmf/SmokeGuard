class LabelColor:
    def __init__(self):
        self.labels = {}

    def add_label(self, label, color):
        if not isinstance(label, str):
            raise ValueError("label harus berupa string")
        if not isinstance(color, tuple) or len(color) != 3:
            raise ValueError("color harus berupa tuple RGB")
        self.labels[label] = color

    def get_color(self, label):
        if label not in self.labels:
            raise ValueError("label tidak ada")
        return self.labels[label]

    def get_all_labels(self):
        return list(self.labels.keys())

    def get_all_colors(self):
        return list(self.labels.values())