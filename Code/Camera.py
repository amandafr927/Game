class Camera:
    def __init__(self):
        self.offset_x = 0

    def update(self, target, world_width, screen_width):
        target_center = target.x + target.image.get_width() // 2

        self.offset_x = target_center - screen_width // 2

        self.offset_x = max(
            0,
            min(self.offset_x, world_width - screen_width)
        )

    def apply(self, x):
        return x - self.offset_x