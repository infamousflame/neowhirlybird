"""Runs the actual game."""

from json import loads
from random import random, randrange

from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.lang.builder import Builder
from kivy.vector import Vector
from kivy.uix.widget import Widget


class GameWidget(Widget):
    """The game widget class."""

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.player: Player = self.ids["player_widget"]

    def update(self, dt: float) -> None:
        if len(self.children) < 5:
            self.add_widget(PlatformWidget(randomise_y=True))
        self.player.update(dt, self.children)
        if self.player.center_y > 0.875 * self.height and self.player.velocity.y > 0:
            cancel_velocity = -self.player.velocity.y
            for child in self.children:
                child.y = cancel_velocity * dt + child.y
            if random() < App.get_running_app().config['platform_spawn_chance']:
                self.add_widget(PlatformWidget())
        for child in self.children:
            if child.center_y < 0:
                self.remove_widget(child)


class BasePlatform(Widget):
    """The base platform widget class."""

    def __init__(self, randomise_y: bool = False, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.pos = (
            randrange(0, App.get_running_app().game_widget.width),
            randrange(0, App.get_running_app().game_widget.height) if randomise_y
            else App.get_running_app().game_widget.height
        )

class PlatformWidget(BasePlatform):
    """The platform widget class."""


class Player(Widget):
    """The player widget class."""

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.velocity = Vector(0, App.get_running_app().config["bounce"])
        self.acceration = Vector(0,
            -App.get_running_app().config["gravity"]
        )
        Window.bind(on_key_down=self.on_key_down)
        Window.bind(on_key_up=self.on_key_up)

    def on_key_down(self, window, key, *args) -> None:
        match key:
            case 97:
                self.velocity.x = -300
            case 100:
                self.velocity.x = 300

    def on_key_up(self, window, key, *args) -> None:
        match key:
            case 97:
                if self.velocity.x < 0:
                    self.velocity.x = 0
            case 100:
                if self.velocity.x > 0:
                    self.velocity.x = 0

    def update(self, dt: float, platforms: list) -> None:
        self.pos = self.velocity * dt + self.pos
        self.velocity += self.acceration * dt
        if self.velocity.y < 0:
            for platform in platforms:
                if platform is self:
                    continue
                if (
                    self.collide_widget(platform)
                    and self.y > platform.y
                ):
                    self.velocity.y = App.get_running_app().config["bounce"]
        if self.center_x < 0:
            self.x += App.get_running_app().game_widget.width
        elif self.center_x > App.get_running_app().game_widget.width:
            self.x -= App.get_running_app().game_widget.width


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
