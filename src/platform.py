"""Classes for the platform widgets."""

from random import random

from kivy.app import App
from kivy.core.window import Window
from kivy.uix.widget import Widget

from player import Player

class BasePlatform(Widget):
    """The base platform widget class."""

    def __init__(self, platforms: list, randomise_y: bool = False, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        width: float = min(Window.width, Window.height) * 0.13
        height: float = min(Window.width, Window.height) * 0.03
        self.pos = (
            random() * (Window.width - width),
            random() * (Window.height - height) if randomise_y
            else Window.height * 0.97
        )

class Platform(BasePlatform):
    """The platform widget class."""

    def handle_collision(self, player: Player) -> None:
        if player.y > self.y and player.velocity.y < 0:
            player.velocity.y = player.app.config['bounce'] * Window.height


class Cloud(BasePlatform):
    """The cloud widget class."""

    def handle_collision(self, player: Player) -> None:
        App.get_running_app().game_widget.remove_widget(self)