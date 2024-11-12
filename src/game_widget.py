"""The game widget class."""

from random import choice
from sys import exit as sys_exit

from kivy.app import App
from kivy.core.window import Window
from kivy.uix.widget import Widget

from platform import (
    BreakablePlatform, Cloud, MovingPlatform, Platform, Springboard
)

class GameWidget(Widget):
    """The game widget class."""

    PLATFORM_CLASSES = (
        Platform, Cloud, BreakablePlatform, Springboard, MovingPlatform
    )

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.player: Player = self.ids['player_widget']
        self.app: WhirlybirdApp = App.get_running_app()
        self.modulus: float = 0.0

    def init(self) -> None:
        for i in range(self.app.config['platform_frequency']):
            self.add_widget(Platform(
                y = i / self.app.config['platform_frequency'] * Window.height
            ))

    def update(self, dt: float) -> None:
        for child in self.children:
            child.update(dt, self.player)
        if (
            self.player.center_y < 0.125 * self.height
            and self.player.velocity.y < 0
        ):
            cancel_velocity = -self.player.velocity.y
            for child in self.children:
                child.y = cancel_velocity * dt + child.y
            self.player.ids['image'].source = 'assets/images/player_death.png'
            if len(self.children) < 2:
                sys_exit()
        elif (
            self.player.center_y > 0.875 * self.height
            and self.player.velocity.y > 0
        ):
            cancel_velocity = -self.player.velocity.y
            for child in self.children:
                child.y = cancel_velocity * dt + child.y
            self.modulus += self.player.velocity.y * dt / Window.height
            if (
            self.modulus > 1 / self.app.config['platform_frequency']
            ):
                self.modulus -= 1 / self.app.config['platform_frequency']
                self.add_platform()
        for child in self.children:
            if child is self.player:
                continue
            if child.center_y < 0 or child.center_y > self.height:
                self.remove_widget(child)

    def add_platform(self) -> None:
        widget_class: type = choice(self.PLATFORM_CLASSES)
        self.add_widget(widget_class())