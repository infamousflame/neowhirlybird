"""Classes for the platform widgets."""

from random import random

from kivy.app import App
from kivy.core.window import Window
from kivy.uix.widget import Widget

from player import Player


class BasePlatform(Widget):
    """The base platform widget class."""

    def __init__(
        self, platforms: list, y: float | None = None, *args, **kwargs
    ) -> None:
        super().__init__(*args, **kwargs)
        width: float = min(Window.width, Window.height) * 0.13
        height: float = min(Window.width, Window.height) * 0.03
        self.pos = (
            random() * (Window.width - width),
            Window.height - height if y is None else y
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


class BreakablePlatform(BasePlatform):
    """The breakable platform widget class."""

    def handle_collision(self, player: Player) -> None:
        if player.y > self.y and player.velocity.y < 0:
            self.ids['image'].source = 'assets/images/platform_void.png'
            player.velocity.y = (
                player.app.config['breakable_bounce'] * Window.height
            )


class Springboard(BasePlatform):
    """The springboard widget class."""

    def handle_collision(self, player: Player) -> None:
        if player.y > self.y and player.velocity.y < 0:
            player.velocity.y = (
                player.app.config['springboard_bounce'] * Window.height
            )
