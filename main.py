import tkinter as tk
from tkinter import ttk
import ast
import operator as op

# ---------- Evaluador seguro (sin eval) ----------
# Permite: +, -, *, /, //, %, **, paréntesis y números decimales
ALLOWED_OPS = {
    ast.Add: op.add, ast.Sub: op.sub, ast.Mult: op.mul, ast.Div: op.truediv,
    ast.FloorDiv: op.floordiv, ast.Mod: op.mod, ast.Pow: op.pow,
    ast.USub: op.neg, ast.UAdd: op.pos,
}

def safe_eval(expr: str) -> float:
    def _eval(node):
        if isinstance(node, ast.Num):         # Python <3.8
            return node.n
        if isinstance(node, ast.Constant):    # Python 3.8+
            if isinstance(node.value, (int, float)):
                return node.value
            raise ValueError("Constante no permitida")
        if isinstance(node, ast.BinOp):
            left, right = _eval(node.left), _eval(node.right)
            fn = ALLOWED_OPS.get(type(node.op))
            if not fn: raise ValueError("Operación no permitida")
            return fn(left, right)
        if isinstance(node, ast.UnaryOp):
            fn = ALLOWED_OPS.get(type(node.op))
            if not fn: raise ValueError("Operación no permitida")
            return fn(_eval(node.operand))
        if isinstance(node, ast.Expression):
            return _eval(node.body)
        raise ValueError("Expresión no válida")
    tree = ast.parse(expr, mode="eval")
    return _eval(tree)

# ---------- UI ----------
class ModernCalc(ttk.Frame):
    def __init__(self, master):
        super().__init__(master, padding=16)
        self.expr_var = tk.StringVar(value="")
        self.result_var = tk.StringVar(value="0")

        self.build_styles()
        self.build_layout()
        self.bind_keys(master)

    # Estilos oscuros con ttk
    def build_styles(self):
        self.bg      = "#0f172a"  # slate-900
        self.panel   = "#111827"  # gray-900
        self.btn     = "#1f2937"  # gray-800
        self.btn_op  = "#334155"  # slate-700
        self.btn_eq  = "#2563eb"  # blue-600
        self.btn_dng = "#ef4444"  # red-500
        self.fg      = "#e5e7eb"  # gray-200
        self.fg_mut  = "#9ca3af"  # gray-400

        self.master.configure(bg=self.bg)
        style = ttk.Style()
        # usar 'clam' por compatibilidad de colores
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure("Panel.TFrame", background=self.panel)
        style.configure("Calc.TFrame", background=self.bg)

        # Pantalla (dos líneas: expresión y resultado)
        style.configure(
            "Display.TLabel",
            background=self.panel, foreground=self.fg,
            font=("SF Pro Display", 18), anchor="e", padding=(12, 8)
        )
        style.configure(
            "Result.TLabel",
            background=self.panel, foreground="white",
            font=("SF Pro Display", 32, "bold"), anchor="e", padding=(12, 2)
        )

        # Botones base
        style.configure(
            "Base.TButton",
            background=self.btn, foreground=self.fg,
            font=("Inter", 16), padding=10, borderwidth=0, relief="flat"
        )
        style.map(
            "Base.TButton",
            background=[("pressed", "#111827"), ("active", "#374151")],
            foreground=[("disabled", self.fg_mut)]
        )

        # Botones operador
        style.configure("Op.TButton", background=self.btn_op, foreground=self.fg)
        style.map("Op.TButton",
                  background=[("pressed", "#1f2937"), ("active", "#475569")])

        # Botón igual
        style.configure("Eq.TButton", background=self.btn_eq, foreground="white")
        style.map("Eq.TButton",
                  background=[("pressed", "#1d4ed8"), ("active", "#3b82f6")])

        # Botón peligro (Clear)
        style.configure("Danger.TButton", background=self.btn_dng, foreground="white")
        style.map("Danger.TButton",
                  background=[("pressed", "#dc2626"), ("active", "#f87171")])

    def build_layout(self):
        # Contenedor principal
        self.pack(fill="both", expand=True)
        wrapper = ttk.Frame(self, style="Calc.TFrame")
        wrapper.pack(fill="both", expand=True)

        # Panel pantalla
        display = ttk.Frame(wrapper, style="Panel.TFrame", padding=12)
        display.grid(row=0, column=0, sticky="nsew", padx=0, pady=(0, 12))

        self.lbl_expr = ttk.Label(display, textvariable=self.expr_var, style="Display.TLabel")
        self.lbl_res  = ttk.Label(display, textvariable=self.result_var, style="Result.TLabel")
        self.lbl_expr.pack(fill="x")
        self.lbl_res.pack(fill="x")

        # Rejilla de botones
        grid = ttk.Frame(wrapper, style="Calc.TFrame")
        grid.grid(row=1, column=0, sticky="nsew")

        # Expand
        wrapper.rowconfigure(0, weight=1)
        wrapper.rowconfigure(1, weight=2)
        wrapper.columnconfigure(0, weight=1)
        for r in range(5):
            grid.rowconfigure(r, weight=1, uniform="row")
        for c in range(4):
            grid.columnconfigure(c, weight=1, uniform="col")

        # Definir botones
        buttons = [
            # fila 0
            ("C",  0, 0, "Danger.TButton", self.clear),
            ("⌫",  0, 1, "Op.TButton",     self.backspace),
            ("%",  0, 2, "Op.TButton",     lambda: self.press("%")),
            ("/",  0, 3, "Op.TButton",     lambda: self.press("/")),
            # fila 1
            ("7",  1, 0, "Base.TButton",   lambda: self.press("7")),
            ("8",  1, 1, "Base.TButton",   lambda: self.press("8")),
            ("9",  1, 2, "Base.TButton",   lambda: self.press("9")),
            ("*",  1, 3, "Op.TButton",     lambda: self.press("*")),
            # fila 2
            ("4",  2, 0, "Base.TButton",   lambda: self.press("4")),
            ("5",  2, 1, "Base.TButton",   lambda: self.press("5")),
            ("6",  2, 2, "Base.TButton",   lambda: self.press("6")),
            ("-",  2, 3, "Op.TButton",     lambda: self.press("-")),
            # fila 3
            ("1",  3, 0, "Base.TButton",   lambda: self.press("1")),
            ("2",  3, 1, "Base.TButton",   lambda: self.press("2")),
            ("3",  3, 2, "Base.TButton",   lambda: self.press("3")),
            ("+",  3, 3, "Op.TButton",     lambda: self.press("+")),
            # fila 4
            ("0",  4, 0, "Base.TButton",   lambda: self.press("0")),
            (".",  4, 1, "Base.TButton",   lambda: self.press(".")),
            ("//", 4, 2, "Op.TButton",     lambda: self.press("//")),
            ("=",  4, 3, "Eq.TButton",     self.calculate),
        ]

        for text, r, c, style, cmd in buttons:
            btn = ttk.Button(grid, text=text, style=style, command=cmd, cursor="hand2")
            btn.grid(row=r, column=c, sticky="nsew", padx=6, pady=6)

        # Sutileza: bordes redondeados visuales
        # (ttk no tiene radios reales; este estilo flat + padding y colores logra el look)

    # --------- Lógica ---------
    def press(self, token: str):
        # Evitar dos operadores seguidos (excepto signos unarios en inicio)
        expr = self.expr_var.get()
        if token in "+-*/%." and (not expr or expr[-1] in "+-*/%."):
            # permitir - unario al inicio
            if not (token == "-" and not expr):
                return
        self.expr_var.set(expr + token)

    def clear(self):
        self.expr_var.set("")
        self.result_var.set("0")

    def backspace(self):
        expr = self.expr_var.get()
        if expr:
            self.expr_var.set(expr[:-1])

    def calculate(self):
        expr = self.expr_var.get().strip()
        if not expr:
            return
        try:
            value = safe_eval(expr)
            # Evitar -0.0 y formatear bonito
            if abs(value) == 0:
                value = 0
            self.result_var.set(f"{value:.10g}")  # hasta 10 cifras significativas
            self.expr_var.set(str(value))
        except Exception:
            self.result_var.set("Error")
            # no borramos expr para poder corregir

    # --------- Teclado ---------
    def bind_keys(self, root):
        for key in "0123456789.+-*/%()":
            root.bind(key, lambda e, k=key: self.press(k))
        root.bind("<Return>", lambda e: self.calculate())
        root.bind("<KP_Enter>", lambda e: self.calculate())
        root.bind("<BackSpace>", lambda e: self.backspace())
        root.bind("<Escape>", lambda e: self.clear())
        # Navegación accesible
        root.bind("<Control-c>", lambda e: (root.clipboard_clear(),
                                            root.clipboard_append(self.result_var.get())))

def main():
    root = tk.Tk()
    root.title("Calculadora — Moderna")
    root.geometry("360x520")
    root.minsize(320, 460)
    app = ModernCalc(root)
    # Hacer toda la ventana redimensionable
    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)
    root.mainloop()

if __name__ == "__main__":
    main()