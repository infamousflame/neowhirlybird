"""The Whirlybird app class."""

from kivy.app import App
from kivy.lang.builder import Builder

from game_widget import GameWidget


class WhirlybirdApp(App):
    """The Whirlybird app class."""

    def build(self):
        with open("assets/ui_layout.kv") as kv_file:
            Builder.load_string(kv_file.read())
        self.game_widget = GameWidget()
        return self.game_widget
