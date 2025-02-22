from textual.app import App, ComposeResult
from textual.widgets import Footer, Header, Digits, Static, OptionList, ContentSwitcher, Markdown
from textual.containers import Horizontal, Vertical, VerticalScroll, HorizontalGroup, VerticalGroup
from textual.widgets import Input, Label
from textual.screen import Screen
from textual.reactive import reactive

from pyscuba.calculators.nitrox_calculator import NitroxCalculator
from pyscuba.physics.depth_converter import DepthConverter


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
            self.input = Input(type="number", placeholder=self.placeholder)
            yield self.input

class ResultadoCalculo(Static):

    resultado: float|None = reactive(0)
    
    def __init__(self, label):
        self.label = label
        super().__init__()  # Llama al constructor de Base

    def compose(self) -> ComposeResult:
        yield Label(self.label)
        self.digits_widget = Digits(str(self.resultado))  # Guarda el widget Digits en un atributo
        yield self.digits_widget

    def watch_resultado(self, value: float) -> None:
        """Se ejecuta automáticamente cuando cambia 'resultado'."""
        if hasattr(self, 'digits_widget'):  # Asegúrate de que el widget Digits existe
            self.digits_widget.update(str(value))  # A

class MOD(CajaCalculos):
    def compose(self) -> ComposeResult:
        with HorizontalGroup():
            self.input1 = FilaCalculo(label="Max ppO2 (bar)", placeholder="Ej. 1.6")
            self.input2 = FilaCalculo(label="O2 Fraction (%)")
            yield self.input1
            yield self.input2
        self.resultado = ResultadoCalculo("MOD")
        yield self.resultado

    def on_input_changed(self, event: Input.Changed) -> None:
        """Calcula el nuevo resultado cuando cambia un input."""
        try:
            valor1 = float(self.input1.input.value) if self.input1.input.value else 0
            valor2 = float(self.input2.input.value) if self.input2.input.value else 0
        except ValueError:
            valor1 = valor2 = 0  # Si hay un valor no numérico


        d = DepthConverter.for_salt_water(0) # Agua del mar
        n = NitroxCalculator(d)
        try:
            mod = n.mod(valor1, valor2)
        except (ZeroDivisionError, ValueError):
            mod = 0
        

        self.resultado.resultado = mod  # Actualiza el resultado


class CalculatorScreen(Screen):
    def compose(self) -> ComposeResult:
        with HorizontalGroup():
            with VerticalGroup():
                yield (mod := MOD())
            yield (teoria := Teoria("", id="teoria"))
        mod.border_title = "MOD"
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