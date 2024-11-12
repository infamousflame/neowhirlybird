"""Runs the actual game."""

from json import loads

from kivy.app import App
from kivy.clock import Clock
from kivy.lang.builder import Builder

from game_widget import GameWidget


class WhirlybirdApp(App):
    """The Whirlybird app class."""

    def build(self) -> GameWidget:
        self.title = "Whirlybird"
        self.icon = "assets/images/player.png"
        with open("assets/config.json") as config_file:
            self.config: dict = loads(config_file.read())
        with open("assets/ui_layout.kv") as kv_file:
            Builder.load_string(kv_file.read())
        self.game_widget: GameWidget = GameWidget()
        self.game_widget.init()
        Clock.schedule_interval(self.game_widget.update, 1 / 60)
        return self.game_widget
