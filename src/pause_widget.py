"""A widget displayed when the game is paused."""

from kivy.app import App
from kivy.uix.widget import Widget

class PauseWidget(Widget):
    """A widget displayed when the game is paused."""
    pass

class PlayButton(Widget):
    """A button displayed when the game is paused, triggers a resume."""
    
    def on_touch_up(self, touch):
        if self.collide_point(*touch.pos):
            App.get_running_app().resume()
