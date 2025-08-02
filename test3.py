import arcade

WINDOW_WIDTH = 600
WINDOW_HEIGHT = 400
WINDOW_TITLE = "Arcade Built-in Music Preview"
BUTTON_WIDTH = 300
BUTTON_HEIGHT = 50

MUSIC_TRACKS = [
    ":resources:music/1918.mp3",
    ":resources:music/funkyrobot.mp3",
]

class MusicButton(arcade.SpriteSolidColor):
    def __init__(self, music_path, center_x, center_y):
        super().__init__(BUTTON_WIDTH, BUTTON_HEIGHT, arcade.color.WHITE)
        self.music_path = music_path
        self.sound = arcade.load_sound(music_path, streaming=True)
        self.center_x = center_x
        self.center_y = center_y

    def play(self):
        print(f"Playing: {self.music_path}")
        arcade.play_sound(self.sound)

class MusicPlayerView(arcade.View):
    def __init__(self):
        super().__init__()
        self.button_list = arcade.SpriteList()
        self.texts = []

    def setup(self):
        start_y = WINDOW_HEIGHT - 100
        spacing = 80

        for i, music in enumerate(MUSIC_TRACKS):
            center_x = WINDOW_WIDTH // 2
            center_y = start_y - i * spacing

            button = MusicButton(music, center_x, center_y)
            self.button_list.append(button)
            self.texts.append((music.split("/")[-1], center_x, center_y))

    def on_draw(self):
        self.clear()
        self.button_list.draw()

        for label, x, y in self.texts:
            arcade.draw_text(
                label,
                x,
                y,
                arcade.color.BLACK,
                font_size=14,
                anchor_x="center",
                anchor_y="center"
            )

    def on_mouse_press(self, x, y, button, modifiers):
        for sprite in arcade.get_sprites_at_point((x, y), self.button_list):
            if isinstance(sprite, MusicButton):
                sprite.play()

def main():
    window = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)
    view = MusicPlayerView()
    view.setup()
    window.show_view(view)
    arcade.run()

if __name__ == "__main__":
    main()
