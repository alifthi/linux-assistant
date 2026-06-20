from pyfiglet import Figlet
from rich.console import Console
from rich.markdown import Markdown
from prompt_toolkit.styles import Style
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
import questionary

class console_utils:
    def __init__(self, config):
        self.config = config
        self.console = Console()
        self.banner = Figlet(font="slant").renderText("Linux Assistant")
        self.intro_md = Markdown("Welcome! Enjoy your linux more.")
        self.custom_style = Style.from_dict({
            'question': 'magenta',
            'answer': 'gray',
            'pointer': 'yellow'})
        
        commands = ["/model",
                    "/quit"]
        self.completer = WordCompleter(commands)

    def release_banner(self):
        self.console.print(self.banner, style="cyan")
        self.console.print(self.intro_md)
    
    def get_user_input(self):
        cmd = questionary.text(
            "➜",
            style=self.custom_style,
            qmark="",
            completer=self.completer
        ).ask()

        if cmd is None:
            raise SystemExit

        if cmd == "/model":
            
            model = questionary.select(
                "Select model:",
                choices=self.config.get_models_list(),
                style=self.custom_style
            ).ask()

            res = self.config.change_model(model)
            cmd = self.get_user_input()
        return cmd  
    
    def print_text(self, text, color, end = ''):
        self.console.print(f"[{color}]{text}", end=end)
