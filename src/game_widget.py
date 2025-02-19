"""The game widget class."""

from random import choices

from kivy.app import App
from kivy.core.window import Window
from kivy.uix.widget import Widget

from src.platform import (
    BasePlatform, BreakablePlatform, Cloud, HattedBreakablePlatform,
    HattedMovingPlatform, HattedPhasePlatform, HattedPlatform,
    MovingPlatform, PhasePlatform,Platform, SpikeBall, Spikes, Springboard
)
from src.player import Player


class GameWidget(Widget):
    """The game widget class."""

    PLATFORM_CLASSES: tuple = (
        Platform, Cloud, BreakablePlatform, Springboard, MovingPlatform,
        PhasePlatform, Spikes, SpikeBall, HattedPlatform,
        HattedBreakablePlatform, HattedMovingPlatform, HattedPhasePlatform
    )
    WEIGHTS: tuple = ()

    JUMPABLE_PLATFORM_INDICES: tuple = (0, 2, 3, 4, 5, 8, 9, 10, 11)
    JUMPABLE_PLATFORM_CLASSES: tuple = ()
    JUMPABLE_WEIGHTS: tuple = ()

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.player: Player = self.ids['player_widget']
        self.app: WhirlybirdApp = App.get_running_app()
        self.modulus: float = 0.0
        self.jumpable_modulus: int = 0
        self.score: float = 0.0
        self.score_label = self.ids['score_label']

    def init(self) -> None:
        for i in range(self.app.config['platform_frequency']):
            self.add_widget(Platform(
                y=(i / self.app.config['platform_frequency'] * Window.height)
            ))
        self.WEIGHTS = tuple(self.app.config['weights'])
        self.JUMPABLE_PLATFORM_CLASSES = tuple(
            self.PLATFORM_CLASSES[i] for i in self.JUMPABLE_PLATFORM_INDICES
        )
        self.JUMPABLE_WEIGHTS = tuple(
            self.WEIGHTS[i] for i in self.JUMPABLE_PLATFORM_INDICES
        )
        self.player.init()

    def update(self, dt: float) -> None:
        for child in self.children:
            if isinstance(child, BasePlatform):
                child.update(dt, self.player)
        self.player.update(dt)
        if (
            self.player.center_y < 0.125 * self.height
            and self.player.velocity.y < 0
        ):
            cancel_velocity = -self.player.velocity.y
            for child in self.children:
                if isinstance(child, BasePlatform | Player):
                    child.y = cancel_velocity * dt + child.y
            self.player.movement_state = self.player.state_type.FALLING
            if len(self.children) < 3:
                self.app.show_game_over()
        elif (
            self.player.center_y > 0.875 * self.height
            and self.player.velocity.y > 0
        ):
            self.score += self.player.velocity.y * dt / Window.height
            cancel_velocity = -self.player.velocity.y
            for child in self.children:
                if child is self.player:
                    print('child is player')
                if isinstance(child, BasePlatform | Player):
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
        self.score_label.text = f'{100 * self.score:.0f}'

    def add_platform(self) -> None:
        self.jumpable_modulus += 1
        if self.jumpable_modulus >= self.app.config['garunteed_jumpable_in']:
            self.add_widget(
                choices(
                    self.JUMPABLE_PLATFORM_CLASSES, self.JUMPABLE_WEIGHTS
                )[0]()
            )
            self.jumpable_modulus = 0
        else:
            platform = choices(self.PLATFORM_CLASSES, self.WEIGHTS)[0]()
            self.add_widget(platform)
            if isinstance(platform, self.JUMPABLE_PLATFORM_CLASSES):
                self.jumpable_modulus = 0
