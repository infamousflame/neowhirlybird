"""Classes for the platform widgets."""

from random import random

from kivy.app import App
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.vector import Vector

from src.player import Player


class BasePlatform(Widget):
    """The base platform widget class."""

    def __init__(self, y: float | None = None, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.pos = (
            random() * (Window.width - self.width),
            Window.height - self.height if y is None else y
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

    def __init__(self, y: float | None = None, *args, **kwargs) -> None:
        super().__init__(y, *args, **kwargs)
        self.active: bool = True

    def update(self, dt: float, player: Player) -> None:
        if (
            self.collide_widget(player)
            and player.y > self.y
            and player.velocity.y < 0
        ):
            if self.active:
                self.active = False
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
        self.active: bool = True

    def update(self, dt: float, player: Player) -> None:
        self.phase += dt
        if self.phase > self.phase_period:
            self.phase -= self.phase_period
            self.active = not self.active
            self.ids['image'].source = (
                'assets/images/platform_phase.png'
                if self.active
                else 'assets/images/platform_void.png'
            )
        if (
            self.collide_widget(player)
            and player.y > self.y
            and player.velocity.y < 0
        ):
            player.velocity.y = (
                player.app.config['breakable_bounce'] * Window.height
            )


class Spikes(BasePlatform):
    """The spikes widget class."""

    def update(self, dt: float, player: Player) -> None:
        if (
            self.collide_widget(player)
            and player.y > self.y
            and player.velocity.y < 0
        ):
            player.app.show_game_over()


class SpikeBall(BasePlatform):
    """The spike ball widget class."""

    def __init__(self, y: float | None = None, *args, **kwargs) -> None:
        super().__init__(y, *args, **kwargs)
        self.velocity = Vector(
            App.get_running_app().config['platform_speed'] * Window.width,
            0
        )
        if random() < 0.5:
            self.velocity.x *= -1
        self.phase: float = 0.0
        self.phase_period: float = App.get_running_app().config['phase_period']
        self.active: bool = True

    def update(self, dt: float, player: Player) -> None:
        if self.x < 0 or self.x + self.width > Window.width:
            self.velocity.x *= -1
        self.pos = self.velocity * dt + self.pos
        self.phase += dt
        if self.phase > self.phase_period:
            self.phase -= self.phase_period
            self.active = not self.active
            self.ids['image'].source = (
                'assets/images/spikeball_enabled.png'
                if self.active
                else 'assets/images/spikeball_disabled.png'
            )
        if (
            self.collide_widget(player)
            and player.y > self.y
            and player.velocity.y < 0
        ):
            if self.active:
                player.app.show_game_over()
            else:
                player.velocity.y = (
                    player.app.config['bounce'] * Window.height
                )
                player.app.game_widget.remove_widget(self)


class HattedPlatform(BasePlatform):
    """A platform with a propeller hat."""

    def __init__(self, y: float | None = None, *args, **kwargs) -> None:
        super().__init__(y, *args, **kwargs)
        self.platform = self.ids['platform']
        self.hat = self.ids['hat']

    def update(self, dt: float, player: Player) -> None:
        if (
            self.platform.collide_widget(player)
            and player.y > self.y
            and player.velocity.y < 0
        ):
            self.remove_widget(self.hat)
            player.hat_timer = player.app.config['hat_duration']


class HattedBreakablePlatform(BasePlatform):
    """A breakable platform with a propeller hat."""

    def __init__(self, y: float | None = None, *args, **kwargs) -> None:
        super().__init__(y, *args, **kwargs)
        self.platform = self.ids['platform']
        self.hat = self.ids['hat']

    def update(self, dt: float, player: Player) -> None:
        if (
            self.platform.collide_widget(player)
            and player.y > self.y
            and player.velocity.y < 0
        ):
            self.remove_widget(self.hat)
            player.hat_timer = player.app.config['hat_duration']
            if self.platform.active:
                self.platform.active = False
                self.platform.ids['image'].source = 'assets/images/platform_void.png'


class HattedMovingPlatform(BasePlatform):
    """A moving platform with a propeller hat."""

    def __init__(self, y: float | None = None, *args, **kwargs) -> None:
        super().__init__(y, *args, **kwargs)
        self.platform = self.ids['platform']
        self.hat = self.ids['hat']

    def update(self, dt: float, player: Player) -> None:
        if self.x < 0 or self.x + self.width > Window.width:
            self.platform.velocity.x *= -1
        self.pos = self.platform.velocity * dt + self.pos
        if (
            self.platform.collide_widget(player)
            and player.y > self.y
            and player.velocity.y < 0
        ):
            self.remove_widget(self.hat)
            player.hat_timer = player.app.config['hat_duration']


class HattedPhasePlatform(BasePlatform):
    """A phase platform with a propeller hat."""

    def __init__(self, y: float | None = None, *args, **kwargs) -> None:
        super().__init__(y, *args, **kwargs)
        self.platform = self.ids['platform']
        self.hat = self.ids['hat']

    def update(self, dt: float, player: Player) -> None:
        self.platform.phase += dt
        if self.platform.phase > self.platform.phase_period:
            self.platform.phase -= self.platform.phase_period
            self.platform.active = not self.platform.active
            self.platform.ids['image'].source = (
                'assets/images/platform_phase.png'
                if self.platform.active
                else 'assets/images/platform_void.png'
            )
        if (
            self.platform.collide_widget(player)
            and player.y > self.y
            and player.velocity.y < 0
        ):
            self.remove_widget(self.hat)
            player.hat_timer = player.app.config['hat_duration']
