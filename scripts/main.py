from textual.app import App, ComposeResult
from textual.widgets import Footer, Header, Digits, Static, OptionList, ContentSwitcher, Markdown
from textual.containers import Horizontal, Vertical, VerticalScroll, HorizontalGroup, VerticalGroup
from textual.widgets import Input, Label
from textual.screen import Screen
from pyscuba.calculators.nitrox_calculator import NitroxCalculator


class Teoria(Markdown):
    pass

class CajaCalculos(Static):
    pass
        
class FilaCalculo(Static):
    def __init__(self, label: str, placeholder="Inserta el dato...") -> None:
        self.label = label
        self.placeholder = placeholder
        super().__init__()

    def compose(self) -> ComposeResult:
        with VerticalGroup():
            yield Label(self.label, classes="label-variable")
            yield Input(type="number", placeholder=self.placeholder)

class ResultadoCalculo(Static):
    def __init__(self, label: str, resultado: float, *args, **kwargs) -> None:
        self.label = label
        self.resultado = str(resultado)
        super().__init__()

    def compose(self) -> ComposeResult:
        yield Label(self.label)
        yield Digits(self.resultado)


class MOD(CajaCalculos):
    def compose(self) -> ComposeResult:
        with HorizontalGroup():
            yield FilaCalculo(label="Max ppO2 (bar)", placeholder="Ej. 1.6")
            yield FilaCalculo(label="O2 Fraction (%)")
        yield ResultadoCalculo("jfiods", 324432, classes="derecha-resultado")

class EAD(CajaCalculos):
    def compose(self) -> ComposeResult:
        with HorizontalGroup():
            yield FilaCalculo(label="Depth (m)", placeholder="Ej. 25")
            yield FilaCalculo(label="Oxygen (%)")
        yield ResultadoCalculo("jfiods", 3242, classes="derecha-resultado")

class BEST_MIX(CajaCalculos):
    def compose(self) -> ComposeResult:
        with HorizontalGroup():
            yield FilaCalculo(label="Depth (m)", placeholder="Ej. 25")
            yield FilaCalculo(label="Max ppO2 (bar)", placeholder="Ej. 1.6")
        yield ResultadoCalculo("jfiods", 324432, classes="derecha-resultado")

class CalculatorScreen(Screen):
    def compose(self) -> ComposeResult:
        with HorizontalGroup():
            with VerticalGroup():
                yield (mod := MOD())
                yield (ead := EAD())
                yield (best_mix := BEST_MIX())
            yield (teoria := Teoria("", id="teoria"))
        mod.border_title = "MOD"
        ead.border_title = "EAD"
        best_mix.border_title = "BEST MIX"
        teoria.border_title = "Teoria"

class PyScubaApp(App):
    """A Textual app to manage stopwatches."""
    CSS_PATH = "layout.tcss"
    BINDINGS = [
        ("n", "nitrox_calculator", "Toggle Nitrox Calculator"),
        ("t", "trimix_calculator", "Toggle Trimix Calculator")
    ]

    def on_ready(self) -> None:
        self.push_screen(CalculatorScreen())




if __name__ == "__main__":
    app = PyScubaApp()
    app.run()