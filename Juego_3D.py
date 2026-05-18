import tkinter as tk
from tkinter import messagebox, font
import random

# ========== LÓGICA DEL JUEGO (igual que antes) ==========
def generar_pregunta(nivel):
    """Genera una pregunta según el nivel y devuelve (texto_pregunta, respuesta_correcta)"""
    if nivel == 1:  # Fácil: suma/resta de dos enteros entre -20 y 20
        a = random.randint(-20, 20)
        b = random.randint(-20, 20)
        operador = random.choice(['+', '-'])
        if operador == '+':
            respuesta = a + b
            pregunta = f"{a} + {b}"
        else:
            respuesta = a - b
            pregunta = f"{a} - {b}"
        return pregunta, respuesta

    elif nivel == 2:  # Medio: multiplicación o división exacta
        if random.choice([True, False]):
            a = random.randint(-12, 12)
            b = random.randint(-12, 12)
            while a == 0 or b == 0:
                a = random.randint(-12, 12)
                b = random.randint(-12, 12)
            respuesta = a * b
            pregunta = f"{a} × {b}"
        else:
            divisor = random.randint(-12, 12)
            while divisor == 0:
                divisor = random.randint(-12, 12)
            cociente = random.randint(-12, 12)
            dividendo = divisor * cociente
            respuesta = cociente
            pregunta = f"{dividendo} ÷ {divisor}"
        return pregunta, respuesta

    else:  # Nivel 3: Difícil, operación combinada
        tipos = [
            lambda a,b,c: (f"({a} + {b}) × {c}", (a + b) * c),
            lambda a,b,c: (f"({a} - {b}) × {c}", (a - b) * c),
            lambda a,b,c: (f"{a} × ({b} + {c})", a * (b + c)),
            lambda a,b,c: (f"{a} × ({b} - {c})", a * (b - c)),
            lambda a,b,c: (f"{a} + {b} × {c}", a + b * c),
            lambda a,b,c: (f"{a} - {b} × {c}", a - b * c),
            lambda a,b,c: (f"({a} + {b}) ÷ {c}", (a + b) // c),
            lambda a,b,c: (f"({a} - {b}) ÷ {c}", (a - b) // c),
        ]
        a = random.randint(-10, 10)
        b = random.randint(-10, 10)
        c = random.randint(-10, 10)
        while c == 0:
            c = random.randint(-10, 10)
        funcion = random.choice(tipos)
        pregunta, respuesta = funcion(a, b, c)
        return pregunta, respuesta


# ========== INTERFAZ GRÁFICA ==========
class JuegoSignosApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Ley de Signos en Acción - Juego Matemático")
        self.root.geometry("600x550")
        self.root.resizable(False, False)
        self.root.configure(bg="#2C3E50")

        # Variables del juego
        self.nivel = None
        self.vidas = 3
        self.puntaje = 0
        self.rondas = 0
        self.pregunta_actual = ""
        self.respuesta_actual = 0

        # Colores
        self.colores = {
            "bg": "#2C3E50",
            "frame": "#34495E",
            "btn": "#1ABC9C",
            "btn_hover": "#16A085",
            "text": "#ECF0F1",
            "correcto": "#2ECC71",
            "incorrecto": "#E74C3C"
        }

        # Fuentes
        self.fuente_titulo = font.Font(family="Helvetica", size=24, weight="bold")
        self.fuente_pregunta = font.Font(family="Helvetica", size=28, weight="bold")
        self.fuente_normal = font.Font(family="Helvetica", size=12)

        self.crear_widgets()
        self.mostrar_pantalla_inicio()

    def crear_widgets(self):
        # Marco principal
        main_frame = tk.Frame(self.root, bg=self.colores["bg"])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Título
        self.titulo = tk.Label(main_frame, text="⚡ LEY DE SIGNOS ⚡", font=self.fuente_titulo,
                               bg=self.colores["bg"], fg=self.colores["text"])
        self.titulo.pack(pady=10)

        # Marco para nivel (se mostrará al inicio)
        self.frame_nivel = tk.Frame(main_frame, bg=self.colores["bg"])
        self.frame_nivel.pack(pady=20)

        tk.Label(self.frame_nivel, text="Selecciona un nivel:", font=self.fuente_normal,
                 bg=self.colores["bg"], fg=self.colores["text"]).pack()

        btn_frame = tk.Frame(self.frame_nivel, bg=self.colores["bg"])
        btn_frame.pack(pady=10)

        self.btn_facil = self.crear_boton(btn_frame, "Fácil (sumas/restas)", 1)
        self.btn_facil.pack(side=tk.LEFT, padx=5)

        self.btn_medio = self.crear_boton(btn_frame, "Medio (× ÷)", 2)
        self.btn_medio.pack(side=tk.LEFT, padx=5)

        self.btn_dificil = self.crear_boton(btn_frame, "Difícil (combinadas)", 3)
        self.btn_dificil.pack(side=tk.LEFT, padx=5)

        # Marco del juego (inicialmente oculto)
        self.frame_juego = tk.Frame(main_frame, bg=self.colores["bg"])
        # Puntuación y vidas
        info_frame = tk.Frame(self.frame_juego, bg=self.colores["bg"])
        info_frame.pack(fill=tk.X, pady=10)

        self.label_puntaje = tk.Label(info_frame, text="🏆 Puntaje: 0", font=self.fuente_normal,
                                      bg=self.colores["bg"], fg="#F1C40F")
        self.label_puntaje.pack(side=tk.LEFT, padx=20)

        self.label_vidas = tk.Label(info_frame, text="❤️❤️❤️", font=self.fuente_normal,
                                    bg=self.colores["bg"], fg="#E74C3C")
        self.label_vidas.pack(side=tk.RIGHT, padx=20)

        # Pregunta
        self.label_pregunta = tk.Label(self.frame_juego, text="", font=self.fuente_pregunta,
                                       bg=self.colores["bg"], fg=self.colores["text"])
        self.label_pregunta.pack(pady=40)

        # Entrada y botón respuesta
        entrada_frame = tk.Frame(self.frame_juego, bg=self.colores["bg"])
        entrada_frame.pack(pady=10)

        self.entry_respuesta = tk.Entry(entrada_frame, font=self.fuente_normal, width=10,
                                        justify='center', bd=3, relief=tk.GROOVE)
        self.entry_respuesta.pack(side=tk.LEFT, padx=5)
        self.entry_respuesta.bind("<Return>", lambda event: self.verificar_respuesta())

        self.btn_responder = self.crear_boton(entrada_frame, "Responder", None)
        self.btn_responder.config(command=self.verificar_respuesta)
        self.btn_responder.pack(side=tk.LEFT, padx=5)

        # Mensaje de retroalimentación
        self.label_mensaje = tk.Label(self.frame_juego, text="", font=self.fuente_normal,
                                      bg=self.colores["bg"])
        self.label_mensaje.pack(pady=20)

        # Botón nuevo juego (oculto inicialmente)
        self.btn_nuevo = tk.Button(self.frame_juego, text="🔄 Nuevo juego", command=self.reiniciar,
                                   bg=self.colores["btn"], fg="white", font=self.fuente_normal,
                                   relief=tk.RAISED, bd=2, padx=10, pady=5)
        # No lo empaquetamos aún

    def crear_boton(self, parent, texto, nivel):
        btn = tk.Button(parent, text=texto, command=lambda: self.iniciar_juego(nivel),
                        bg=self.colores["btn"], fg="white", font=self.fuente_normal,
                        relief=tk.RAISED, bd=2, padx=10, pady=5, activebackground=self.colores["btn_hover"])
        return btn

    def mostrar_pantalla_inicio(self):
        """Muestra la pantalla de selección de nivel y oculta el juego"""
        self.frame_nivel.pack()
        self.frame_juego.pack_forget()

    def iniciar_juego(self, nivel):
        """Inicializa el juego con el nivel seleccionado"""
        self.nivel = nivel
        self.vidas = 3
        self.puntaje = 0
        self.rondas = 0
        self.actualizar_puntaje_vidas()
        self.frame_nivel.pack_forget()
        self.frame_juego.pack(fill=tk.BOTH, expand=True)
        self.btn_nuevo.pack_forget()  # ocultar botón nuevo si estaba visible
        self.generar_nueva_pregunta()
        self.entry_respuesta.delete(0, tk.END)
        self.entry_respuesta.focus()

    def generar_nueva_pregunta(self):
        """Crea una nueva pregunta y la muestra"""
        if self.vidas > 0:
            texto, resp = generar_pregunta(self.nivel)
            self.pregunta_actual = texto
            self.respuesta_actual = resp
            self.label_pregunta.config(text=f"{texto} = ?")
            self.label_mensaje.config(text="")
            self.entry_respuesta.delete(0, tk.END)
        else:
            self.fin_juego()

    def verificar_respuesta(self):
        """Verifica la respuesta del usuario"""
        try:
            respuesta_usuario = int(self.entry_respuesta.get())
        except ValueError:
            self.label_mensaje.config(text="⚠️ Ingresa un número entero", fg="orange")
            return

        if respuesta_usuario == self.respuesta_actual:
            # Respuesta correcta
            self.puntaje += 10
            self.label_mensaje.config(text="✅ ¡Correcto! +10 puntos", fg=self.colores["correcto"])
            self.actualizar_puntaje_vidas()
            # Siguiente pregunta después de 1 segundo
            self.root.after(1000, self.generar_nueva_pregunta)
        else:
            # Respuesta incorrecta
            self.vidas -= 1
            self.actualizar_puntaje_vidas()
            self.label_mensaje.config(text=f"❌ Incorrecto. Respuesta: {self.respuesta_actual}. Pierdes una vida.",
                                      fg=self.colores["incorrecto"])
            if self.vidas == 0:
                self.root.after(1500, self.fin_juego)
            else:
                self.root.after(1500, self.generar_nueva_pregunta)

        self.rondas += 1

    def actualizar_puntaje_vidas(self):
        self.label_puntaje.config(text=f"🏆 Puntaje: {self.puntaje}")
        corazones = "❤️" * self.vidas if self.vidas > 0 else "💀"
        self.label_vidas.config(text=corazones)

    def fin_juego(self):
        """Termina el juego y muestra resumen"""
        self.label_pregunta.config(text="JUEGO TERMINADO")
        self.entry_respuesta.config(state=tk.DISABLED)
        self.btn_responder.config(state=tk.DISABLED)
        mensaje_final = f"Puntaje final: {self.puntaje} puntos\nRondas jugadas: {self.rondas}"
        if self.puntaje >= 50:
            mensaje_final += "\n🌟 ¡Excelente! Dominas la ley de signos."
        elif self.puntaje >= 20:
            mensaje_final += "\n👍 Buen trabajo, sigue practicando."
        else:
            mensaje_final += "\n📚 No te desanimes, estudia la ley de signos y vuelve."
        self.label_mensaje.config(text=mensaje_final, fg="white")
        # Mostrar botón nuevo juego
        self.btn_nuevo.pack(pady=10)

    def reiniciar(self):
        """Reinicia completamente el juego (vuelve a inicio)"""
        self.entry_respuesta.config(state=tk.NORMAL)
        self.btn_responder.config(state=tk.NORMAL)
        self.frame_juego.pack_forget()
        self.mostrar_pantalla_inicio()


if __name__ == "__main__":
    root = tk.Tk()
    app = JuegoSignosApp(root)
    root.mainloop()