from prompt_toolkit import Application
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.widgets import TextArea, Frame
from prompt_toolkit.layout import Layout, HSplit
from prompt_toolkit.styles import Style
from prompt_toolkit.lexers import PygmentsLexer
from prompt_toolkit.application import run_in_terminal

from pygments.lexers import get_lexer_for_filename
from pygments.util import ClassNotFound

import os

def run(args, commands):
    if not args:
        print("Usage: nano <filename>")
        return

    filename = args[0]
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            text = f.read()
    else:
        text = ""

    # Try to guess the lexer based on file extension
    try:
        lexer_instance = get_lexer_for_filename(filename)
        lexer_class = type(lexer_instance)
        lexer = PygmentsLexer(lexer_class)
    except ClassNotFound:
        lexer = None

    editor = TextArea(
        text=text,
        multiline=True,
        line_numbers=True,
        wrap_lines=False,
        lexer=lexer
    )

    bindings = KeyBindings()

    @bindings.add("c-s")
    def save_file(event):
        run_in_terminal(lambda: print(f"\n[saved] {filename}"))
        with open(filename, "w", encoding="utf-8") as f:
            f.write(editor.text)

    @bindings.add("c-q")
    def quit_editor(event):
        event.app.exit()

    app = Application(
        layout=Layout(HSplit([Frame(editor)])),
        key_bindings=bindings,
        full_screen=True,
        mouse_support=True,
        style=Style.from_dict({
            "frame.border": "#00afff",
            "text-area": "#ffffff",
        }),
    )

    app.run()
