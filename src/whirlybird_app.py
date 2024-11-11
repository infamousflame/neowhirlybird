"""Runs the actual game."""

from json import loads

from kivy.app import App
from kivy.clock import Clock
from kivy.lang.builder import Builder
from kivy.properties import ObjectProperty
from kivy.uix.widget import Widget


class GameWidget(Widget):
    """The game widget class."""
    player: ObjectProperty = ObjectProperty(None)

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def update(self, dt: float) -> None:
        self.player.update(dt)


class Player(Widget):
    """The player widget class."""
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.gravity: float = App.get_running_app().config['gravity']
        self.velocity_x: float = 0.0
        self.velocity_y: float = 10.0

    def update(self, dt: float) -> None:
        self.velocity_y -= self.gravity * dt
        self.x += self.velocity_x
        self.y += self.velocity_y


class WhirlybirdApp(App):
    """The Whirlybird app class."""

    def build(self) -> GameWidget:
        with open("assets/config.json") as config_file:
            self.config: dict = loads(config_file.read())
        with open("assets/ui_layout.kv") as kv_file:
            Builder.load_string(kv_file.read())
        self.game_widget: GameWidget = GameWidget()
        Clock.schedule_interval(self.game_widget.update, 1 / 60)
        return self.game_widget
