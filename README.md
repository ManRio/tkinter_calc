# 🧮 Calculadora Moderna con Tkinter

Una calculadora moderna creada en **Python 3** utilizando **Tkinter** y
**ttk** con un diseño oscuro, soporte de teclado y evaluación matemática
segura (sin `eval()`).

---

## 🚀 Características

- 🎨 **Interfaz moderna y oscura** inspirada en diseños minimalistas.
- ⌨️ **Soporte completo de teclado** (números, operadores, Enter,
  Backspace, Escape).
- 🧠 **Evaluador matemático seguro**, sin el uso de `eval()`, usando
  el módulo `ast`.
- 🔢 Soporta operaciones básicas:
  - Suma `+`
  - Resta `-`
  - Multiplicación `*`
  - División `/`
  - División entera `//`
  - Potencias `**`
  - Módulo `%`
  - Paréntesis `( )`
  - Números decimales `.`
- 💾 Copia rápida del resultado al portapapeles con `Ctrl + C`.
- 🪶 Diseño responsive: se adapta al redimensionar la ventana.

---

## 🧩 Requisitos

- **Python 3.8 o superior**
- No requiere librerías externas, solo el módulo estándar `tkinter`
  (viene con Python).

Puedes verificar si tienes Tkinter ejecutando:

```bash
python -m tkinter
```

Si se abre una pequeña ventana de prueba, todo está correcto ✅

---

## ⚙️ Instalación y uso

1.  **Clona o descarga el repositorio**

    ```bash
    git clone https://github.com/tuusuario/calculadora-tkinter.git
    cd calculadora-tkinter
    ```

2.  **Ejecuta el programa**

    ```bash
    python calculadora_moderna.py
    ```

3.  ¡Listo! Aparecerá la calculadora con su interfaz moderna y podrás
    usar tanto el ratón como el teclado.

---

## 🖱️ Controles rápidos

Acción Tecla

---

Calcular resultado **Enter** o **Numpad Enter**
Borrar todo **Esc**
Borrar último dígito **Backspace**
Copiar resultado **Ctrl + C**
Números y operadores Teclado numérico o alfanumérico

---

## 🧠 Evaluador matemático seguro

El código utiliza el módulo `ast` de Python para analizar las
expresiones matemáticas y solo permite operadores definidos de forma
explícita, evitando así la ejecución de código arbitrario.

Esto garantiza que la calculadora sea **segura**, incluso si se modifica
el campo de texto.

---

## 🧑‍💻 Autor

**ManRio**\
📧 <manureina87@gmail.com>\
🐙 [github.com/manrio](https://github.com/manrio)

---

## 🪪 Licencia

Este proyecto está bajo la licencia **MIT**, lo que significa que puedes
usarlo, modificarlo y distribuirlo libremente, siempre que se incluya la
atribución original.
