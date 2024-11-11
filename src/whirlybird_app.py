"""The Whirlybird app class."""

from kivy.app import App
from kivy.lang.builder import Builder
from kivy.uix.widget import Widget


class GameWidget(Widget):
    """The game widget class."""


class Player(Widget):
    """The player widget class."""


class WhirlybirdApp(App):
    """The Whirlybird app class."""

    def build(self):
        with open("assets/ui_layout.kv") as kv_file:
            Builder.load_string(kv_file.read())
        self.game_widget = GameWidget()
        return self.game_widget
