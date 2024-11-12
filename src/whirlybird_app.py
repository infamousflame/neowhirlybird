"""Runs the actual game."""

from json import loads
from random import choice, random
from sys import exit as sys_exit

from kivy.app import App
from kivy.clock import Clock
from kivy.lang.builder import Builder
from kivy.uix.widget import Widget

from platform import BreakablePlatform, Cloud, Platform, Springboard
from player import Player


class GameWidget(Widget):
    """The game widget class."""

    PLATFORM_CLASSES = (Platform, Cloud, BreakablePlatform, Springboard)

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.player: Player = self.ids['player_widget']
        self.app: WhirlybirdApp = App.get_running_app()
        self.jumpable_platforms: int = 0

    def update(self, dt: float) -> None:
        self.player.update(dt, self.children)
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
            if random() < (
                self.app.config['platform_spawn_chance']
                * self.player.velocity.y * dt
            ):
                self.add_platform()
        elif self.jumpable_platforms < 5:
            self.add_widget(Platform(self.children, randomise_y=True))
            self.jumpable_platforms += 1
        for child in self.children:
            if child is self.player:
                continue
            if child.center_y < 0 or child.center_y > self.height:
                if isinstance(child, Platform | BreakablePlatform):
                    self.jumpable_platforms -= 1
                self.remove_widget(child)

    def add_platform(self) -> None:
        widget_class: type = choice(self.PLATFORM_CLASSES)
        self.add_widget(widget_class(self.children))
        if widget_class is Platform or widget_class is BreakablePlatform:
            self.jumpable_platforms += 1


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
        Clock.schedule_interval(self.game_widget.update, 1 / 60)
        return self.game_widget
