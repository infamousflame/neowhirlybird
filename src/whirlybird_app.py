"""Runs the actual game."""

from datetime import datetime
from json import loads

from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.lang.builder import Builder

from src.game_widget import GameWidget
from src.game_over_widget import GameOverWidget


class WhirlybirdApp(App):
    """The Whirlybird app class."""

    def __init__(self) -> None:
        super().__init__()
        self.root = None

    def build(self) -> GameWidget:
        self.title = 'Whirlybird'
        self.icon = 'assets/images/icon.png'
        with open('assets/config.json', 'rt') as config_file:
            self.config: dict = loads(config_file.read())
        now: datetime = datetime.now()
        self.config['hat_sprite'] = (
            'christmas_hat'
            if now.month == 12 and 11 <= now.day <= 25
            else 'hat'
        )
        with open('assets/ui_layout.kv', 'rt') as kv_file:
            Builder.load_string(kv_file.read())
        return self.start()

    def start(self) -> None:
        first: bool = True
        if self.root is not None:
            first = False
            Window.remove_widget(self.root)
        self.game_widget: GameWidget = GameWidget()
        self.game_widget.init()
        Clock.schedule_interval(self.game_widget.update, 1 / 60)
        self.root = self.game_widget
        if not first:
            Window.add_widget(self.root)
        return self.root

    def show_game_over(self) -> None:
        Clock.unschedule(self.game_widget.update)
        Window.remove_widget(self.root)
        self.root = GameOverWidget()
        Window.add_widget(self.root)
