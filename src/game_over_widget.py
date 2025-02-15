"""A widget displayed when the game is over."""

from kivy.app import App
from kivy.uix.widget import Widget


class GameOverWidget(Widget):
    """A widget displayed when the game is over."""


class GameOverLabel(Widget):
    """A label displayed when the game is over."""


class RetryButton(Widget):
    """A button displayed when the game is over, triggers a restart."""

    def on_touch_up(self, touch):
        if self.collide_point(*touch.pos):
            App.get_running_app().start()
