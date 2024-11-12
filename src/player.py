"""The player class."""

from kivy.app import App
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.vector import Vector


class Player(Widget):
    """The player widget class."""

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.app: WhirlybirdApp = App.get_running_app()
        self.velocity = Vector(0, self.app.config['bounce'] * Window.height)
        self.acceration = Vector(
            0,
            -self.app.config['gravity'] * Window.height
        )
        Window.bind(on_key_down=self._on_key_down)
        Window.bind(on_key_up=self._on_key_up)

    def _on_key_down(self, window, key, *args) -> None:
        match key:
            case 97:
                self.velocity.x = (
                    -Window.width * self.app.config['horizontal_speed']
                )
                self.ids['image'].source = 'assets/images/player_l.png'
            case 100:
                self.velocity.x = (
                    Window.width * self.app.config['horizontal_speed']
                )
                self.ids['image'].source = 'assets/images/player_r.png'

    def _on_key_up(self, window, key, *args) -> None:
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
        for platform in platforms:
            if platform is self:
                continue
            if self.collide_widget(platform):
                platform.handle_collision(self)
        width: float = Window.width
        if self.center_x < 0:
            self.x += width
        elif self.center_x > width:
            self.x -= width
