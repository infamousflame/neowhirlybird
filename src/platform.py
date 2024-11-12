"""Classes for the platform widgets."""

from random import random

from kivy.app import App
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.vector import Vector

from player import Player


class BasePlatform(Widget):
    """The base platform widget class."""

    def __init__(self, y: float | None = None, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        width: float = min(Window.width, Window.height) * 0.13
        height: float = min(Window.width, Window.height) * 0.03
        self.pos = (
            random() * (Window.width - width),
            Window.height - height if y is None else y
        )

    def update(self, dt: float, player: Player) -> None:
        raise NotImplementedError


class Platform(BasePlatform):
    """The platform widget class."""

    def update(self, dt: float, player: Player) -> None:
        if (
            self.collide_widget(player)
            and player.y > self.y
            and player.velocity.y < 0
        ):
            player.velocity.y = player.app.config['bounce'] * Window.height


class Cloud(BasePlatform):
    """The cloud widget class."""

    def update(self, dt: float, player: Player) -> None:
        if self.collide_widget(player):
            player.app.game_widget.remove_widget(self)


class BreakablePlatform(BasePlatform):
    """The breakable platform widget class."""

    def update(self, dt: float, player: Player) -> None:
        if (
            self.collide_widget(player)
            and player.y > self.y
            and player.velocity.y < 0
        ):
            self.ids['image'].source = 'assets/images/platform_void.png'
            player.velocity.y = (
                player.app.config['breakable_bounce'] * Window.height
            )


class Springboard(BasePlatform):
    """The springboard widget class."""

    def update(self, dt: float, player: Player) -> None:
        if (
            self.collide_widget(player)
            and player.y > self.y
            and player.velocity.y < 0
        ):
            player.velocity.y = (
                player.app.config['springboard_bounce'] * Window.height
            )


class MovingPlatform(BasePlatform):
    """The moving platform widget class."""

    def __init__(self, y: float | None = None, *args, **kwargs) -> None:
        super().__init__(y, *args, **kwargs)
        self.velocity = Vector(
            App.get_running_app().config['platform_speed'] * Window.width,
            0
        )
        if random() < 0.5:
            self.velocity.x *= -1

    def update(self, dt: float, player: Player) -> None:
        if self.x < 0 or self.x + self.width > Window.width:
            self.velocity.x *= -1
        self.pos = self.velocity * dt + self.pos
        if (
            self.collide_widget(player)
            and player.y > self.y
            and player.velocity.y < 0
        ):
            player.velocity.y = (
                player.app.config['bounce'] * Window.height
            )


class PhasePlatform(BasePlatform):
    """The phase platform widget class."""

    def __init__(self, y: float | None = None, *args, **kwargs) -> None:
        super().__init__(y, *args, **kwargs)
        self.phase: float = 0.0
        self.phase_period: float = App.get_running_app().config['phase_period']

    def update(self, dt: float, player: Player) -> None:
        if (
            self.collide_widget(player)
            and player.y > self.y
            and player.velocity.y < 0
        ):
            player.velocity.y = (
                player.app.config['breakable_bounce'] * Window.height
            )
        self.phase += dt
        if self.phase > self.phase_period:
            self.phase -= self.phase_period
            self.ids['image'].source = (
                'assets/images/platform_void.png'
                if self.ids['image'].source == 'assets/images/platform_phase.png'
                else 'assets/images/platform_phase.png'
            )
