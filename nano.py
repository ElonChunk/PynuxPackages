from prompt_toolkit import Application
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.widgets import TextArea, Frame
from prompt_toolkit.layout import Layout, HSplit
from prompt_toolkit.styles import Style
from prompt_toolkit.lexers import PygmentsLexer
from prompt_toolkit.application import run_in_terminal
from pygments.lexers import get_lexer_for_filename
from pygments.util import ClassNotFound
from prompt_toolkit.filters import Condition
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

    # Try to detect syntax highlighter
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
        lexer=lexer,
    )

    # Input field for find (hidden by default)
    find_bar = TextArea(
        height=1,
        prompt='🔍 Find: DOES NOT WORK YET! COMING IN 1.0.5V ',
        style='class:findbar',
        multiline=False,
        wrap_lines=False
    )
    find_bar.visible = False  # Hide until Ctrl+F

    # Help bar
    helpbar = TextArea(
        text="[Ctrl+S: Save ✓]  [Ctrl+Q: Quit ✓]  [Ctrl+F: Find | DOES NOT WORK YET]",
        style="class:helpbar",
        height=1,
        focusable=False,
    )

    # Layout
    root_container = HSplit([
        Frame(editor),
        find_bar,
        helpbar
    ])

    # Key bindings
    bindings = KeyBindings()

    @bindings.add("c-s")
    def save(event):
        with open(filename, "w", encoding="utf-8") as f:
            f.write(editor.text)
        run_in_terminal(lambda: print(f"\n[saved] {filename}"))

    @bindings.add("c-q")
    def quit(event):
        event.app.exit()

    @bindings.add("c-f")
    def start_find(event):
        find_bar.text = ""
        find_bar.visible = True
        app.layout.focus(find_bar)

    @bindings.add("enter", filter=Condition(lambda: find_bar.has_focus))
    def do_find(event):
        query = find_bar.text
        if not query.strip():
            find_bar.visible = False
            app.layout.focus(editor)
            return

        text = editor.text
        pos = text.find(query)
        if pos != -1:
            editor.buffer.cursor_position = pos
        else:
            run_in_terminal(lambda: print("[Find] Not found."))

        find_bar.visible = False
        app.layout.focus(editor)

    style = Style.from_dict({
        "frame.border": "#00afff",
        "text-area": "#ffffff",
        "helpbar": "bg:#333333 #aaaaaa",
        "findbar": "bg:#222222 #00ffcc",
    })

    app = Application(
        layout=Layout(root_container),
        key_bindings=bindings,
        full_screen=True,
        mouse_support=True,
        style=style,
    )

    app.run()
