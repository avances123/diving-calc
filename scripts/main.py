from textual.app import App, ComposeResult
from textual.widgets import Footer, Header, Digits, Static, OptionList, ContentSwitcher, Markdown
from textual.containers import Horizontal, Vertical, VerticalScroll
from textual.widgets.option_list import Option
from pyscuba import gas

MARKDOWN_EXAMPLE = """# Three Flavours Cornetto

The Three Flavours Cornetto trilogy is an anthology series of British
comedic genre films directed by Edgar Wright.
# Three Flavours Cornetto

The Three Flavours Cornetto trilogy is an anthology series of British
comedic genre films directed by Edgar Wright.

# Three Flavours Cornetto

The Three Flavours Cornetto trilogy is an anthology series of British
comedic genre films directed by Edgar Wright.
# Three Flavours Cornetto

The Three Flavours Cornetto trilogy is an anthology series of British
comedic genre films directed by Edgar Wright.

The Three Flavours Cornetto trilogy is an anthology series of British
comedic genre films directed by Edgar Wright.
# Three Flavours Cornetto

The Three Flavours Cornetto trilogy is an anthology series of British
comedic genre films directed by Edgar Wright.

# Three Flavours Cornetto

The Three Flavours Cornetto trilogy is an anthology series of British
comedic genre films directed by Edgar Wright.
# Three Flavours Cornetto

The Three Flavours Cornetto trilogy is an anthology series of British
comedic genre films directed by Edgar Wright.

The Three Flavours Cornetto trilogy is an anthology series of British
comedic genre films directed by Edgar Wright.
# Three Flavours Cornetto

The Three Flavours Cornetto trilogy is an anthology series of British
comedic genre films directed by Edgar Wright.

# Three Flavours Cornetto

The Three Flavours Cornetto trilogy is an anthology series of British
comedic genre films directed by Edgar Wright.
# Three Flavours Cornetto

The Three Flavours Cornetto trilogy is an anthology series of British
comedic genre films directed by Edgar Wright.

The Three Flavours Cornetto trilogy is an anthology series of British
comedic genre films directed by Edgar Wright.
# Three Flavours Cornetto

The Three Flavours Cornetto trilogy is an anthology series of British
comedic genre films directed by Edgar Wright.

# Three Flavours Cornetto

The Three Flavours Cornetto trilogy is an anthology series of British
comedic genre films directed by Edgar Wright.
# Three Flavours Cornetto

The Three Flavours Cornetto trilogy is an anthology series of British
comedic genre films directed by Edgar Wright.
"""


class PyScubaApp(App):
    """A Textual app to manage stopwatches."""
    CSS_PATH = "layout.tcss"
    BINDINGS = [("d", "toggle_dark", "Toggle dark mode")]

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        #yield Static("Menu", classes="menu")
        yield OptionList(
            Option("Calcular MOD", id="mod"),
            Option("Calcular AED", id="aed"),
            classes="menu"
        )
        with ContentSwitcher(initial="mod", classes="derecha"):  
            yield Vertical(
                Static("MOD", classes="datos"),
                Markdown(MARKDOWN_EXAMPLE, classes="teoria"),
                id="mod"
            )
            yield Vertical(
                Static("AED", classes="datos"),
                Markdown(MARKDOWN_EXAMPLE, classes="teoria"),
                id="aed"
            )

        yield Header()
        yield Footer()


    def on_option_list_option_selected(self, event) -> None: 
        self.query_one(ContentSwitcher).current = event.option.id  

    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.theme = (
            "textual-dark" if self.theme == "textual-light" else "textual-light"
        )


if __name__ == "__main__":
    app = PyScubaApp()
    app.run()