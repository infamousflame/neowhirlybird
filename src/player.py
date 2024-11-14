"""The player class."""

from enum import Enum

from kivy.app import App
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.vector import Vector


class MovementState(Enum):
    """The player movement state enum."""
    FACING_LEFT = 0
    FACING_RIGHT = 1
    FALLING = 2


class Player(Widget):
    """The player widget class."""

    state_type = MovementState

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.app: WhirlybirdApp = App.get_running_app()
        self.velocity: Vector = Vector(0, self.app.config['bounce'] * Window.height)
        self.acceration: Vector = Vector(
            0,
            -self.app.config['gravity'] * Window.height
        )
        self.horizontal_speed: float = self.app.config['horizontal_speed']
        self.movement_state: MovementState = self.state_type.FACING_RIGHT
        self.old_state: MovementState = self.state_type.FACING_RIGHT
        self.hat_timer: float = 0
        Window.bind(on_key_down=self._on_key_down)
        Window.bind(on_key_up=self._on_key_up)

    def _on_key_down(self, window, key, *args) -> None:
        match key:
            case 97:
                self.velocity.x = (
                    -Window.width * self.horizontal_speed
                )
                self.movement_state = self.state_type.FACING_LEFT
            case 100:
                self.velocity.x = (
                    Window.width * self.horizontal_speed
                )
                self.movement_state = self.state_type.FACING_RIGHT

    def _on_key_up(self, window, key, *args) -> None:
        match key:
            case 97:
                if self.velocity.x < 0:
                    self.velocity.x = 0
            case 100:
                if self.velocity.x > 0:
                    self.velocity.x = 0

    def update(self, dt: float) -> None:
        self.pos = self.velocity * dt + self.pos
        if self.hat_timer > 0:
            self.hat_timer -= dt
            self.velocity.y = self.app.config['hat_speed'] * Window.height
        else:
            self.velocity += self.acceration * dt
        width: float = Window.width
        if self.center_x < 0:
            self.x += width
        elif self.center_x > width:
            self.x -= width
        self.ids['image'].source = (
            (
                'assets/images/player_l_hat.png'
                if self.hat_timer > 0.0 else
                'assets/images/player_l.png'
            )
            if self.movement_state is self.state_type.FACING_LEFT
            else (
                'assets/images/player_r_hat.png'
                if self.hat_timer > 0.0 else
                'assets/images/player_r.png'
            )
            if self.movement_state is self.state_type.FACING_RIGHT
            else 'assets/images/player_death.png'
            if self.movement_state is self.state_type.FALLING
            else 'assets/images/player.png'
        )
        self.old_state = self.movement_state
