from textual.app import App, ComposeResult
from textual.widgets import Footer, Header, Digits, Static, OptionList, ContentSwitcher, MarkdownViewer, Markdown
from textual.containers import Horizontal, Vertical, VerticalScroll, HorizontalGroup, VerticalGroup
from textual.widgets import Input, Label
from textual.screen import Screen
from textual.message import Message
from textual.reactive import reactive

from pyscuba.calculators.nitrox_calculator import NitroxCalculator
from pyscuba.physics.depth_converter import DepthConverter


class Teoria(Markdown):
    can_focus = False

    def __init__(self, file_path: str, *args, **kwargs) -> None:
        # Lee el contenido del archivo
        with open(file_path, 'r') as file:
            self.markdown_content = file.read()
        super().__init__(self.markdown_content, *args, **kwargs)

    def update_content(self, new_file_path: str) -> None:
        """Método para actualizar el contenido de la teoría según el archivo proporcionado."""
        with open(new_file_path, 'r') as file:
            self.markdown_content = file.read()
        self.update(self.markdown_content)

class CajaCalculos(Static):
    def on_descendant_focus(self):
        self.add_class("focused")
                # Determinar qué tipo de caja tiene el foco y actualizar la teoría
        if isinstance(self, MOD):
            self.app.get_widget_by_id("teoria").update_content("theory/mod.md")
        elif isinstance(self, EAD):
            self.app.get_widget_by_id("teoria").update_content("theory/ead.md")

    def on_descendant_blur(self):
        self.remove_class("focused")
        
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
        self.resultado = ResultadoCalculo("MOD (m)")
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


class EAD(CajaCalculos):
    def compose(self) -> ComposeResult:
        with HorizontalGroup():
            self.input1 = FilaCalculo(label="Depth (m)", placeholder="25")
            self.input2 = FilaCalculo(label="O2 Fraction (%)",  placeholder="36")
            yield self.input1
            yield self.input2
        self.resultado = ResultadoCalculo("EAD (m)")
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
            mod = n.ead(valor2, valor1)
        except (ZeroDivisionError, ValueError):
            mod = 0
        self.resultado.resultado = mod  # Actualiza el resultado



class BEST_MIX(CajaCalculos):
    def compose(self) -> ComposeResult:
        with HorizontalGroup():
            self.input1 = FilaCalculo(label="Depth (m)", placeholder="25")
            self.input2 = FilaCalculo(label="Max ppO2 (bar)", placeholder="1.6")
            yield self.input1
            yield self.input2
        self.resultado = ResultadoCalculo("BEST MIX (%)")
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
            mod = n.best_mix(valor2, valor1)
        except (ZeroDivisionError, ValueError):
            mod = 0
        self.resultado.resultado = mod  # Actualiza el resultado

class PARTIAL_PRESSURE(CajaCalculos):
    def compose(self) -> ComposeResult:
        with HorizontalGroup():
            self.input1 = FilaCalculo(label="Depth (m)", placeholder="25")
            self.input2 = FilaCalculo(label="O2 Fraction (%)",  placeholder="36")
            yield self.input1
            yield self.input2
        self.resultado = ResultadoCalculo("PARTIAL PRESSURE (%)")
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
            mod = n.partial_pressure(valor2, valor1)
        except (ZeroDivisionError, ValueError):
            mod = 0
        self.resultado.resultado = mod  # Actualiza el resultado



class CalculatorScreen(Screen):
    def compose(self) -> ComposeResult:
        with HorizontalGroup():
            with VerticalGroup():
                yield (mod := MOD())
                yield (ead := EAD())
                yield (best_mix := BEST_MIX())
                yield (partial_pressure := PARTIAL_PRESSURE())
            yield (teoria := Teoria("theory/mod.md", id="teoria"))
        mod.border_title = "MOD"
        ead.border_title = "EAD"
        best_mix.border_title = "BEST MIX"
        partial_pressure.border_title = "BEST MIX"
        teoria.border_title = "Teoria"
        yield Footer()
        yield Header()

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