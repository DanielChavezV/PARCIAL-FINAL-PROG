import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from usuario import Usuario
from encuesta import Encuesta
from pregunta import Pregunta
from participante import Participante
from respuesta import Respuesta
from estudio import Estudio
from reporte import Reporte

class SistemaGestionEncuestasGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Gestión de Encuestas")
        self.root.geometry("800x600")

        self.usuario_actual = None
        self.encuesta_actual = None
        self.estudio_actual = None
        self.df = None
        self.reporte_actual = None

        self.encuestas = []
        self.estudios = []

        self.crear_interfaz()

    def crear_interfaz(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill="both")

        self.tab_login = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_login, text="Iniciar Sesión")
        self.crear_tab_login()

        self.tab_encuestas = ttk.Frame(self.notebook)
        self.tab_participantes = ttk.Frame(self.notebook)
        self.tab_estudios = ttk.Frame(self.notebook)
        self.tab_reportes = ttk.Frame(self.notebook)

    def crear_tab_login(self):
        ttk.Label(self.tab_login, text="Usuario:").grid(row=0, column=0, padx=10, pady=10)
        self.entry_usuario = ttk.Entry(self.tab_login)
        self.entry_usuario.grid(row=0, column=1, padx=10, pady=10)

        ttk.Label(self.tab_login, text="Contraseña:").grid(row=1, column=0, padx=10, pady=10)
        self.entry_password = ttk.Entry(self.tab_login, show="*")
        self.entry_password.grid(row=1, column=1, padx=10, pady=10)

        ttk.Button(self.tab_login, text="Iniciar Sesión", command=self.iniciar_sesion).grid(row=2, column=0, columnspan=2, pady=20)

    def iniciar_sesion(self):
        usuario = self.entry_usuario.get()
        password = self.entry_password.get()
        
        if usuario == "admin" and password == "admin":
            self.usuario_actual = Usuario(usuario, "admin@example.com", "Coordinador")
            self.habilitar_funcionalidades()
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")

    def habilitar_funcionalidades(self):
        self.notebook.add(self.tab_encuestas, text="Encuestas")
        self.notebook.add(self.tab_participantes, text="Participantes")
        self.notebook.add(self.tab_estudios, text="Estudios")
        self.notebook.add(self.tab_reportes, text="Reportes")
        
        self.notebook.forget(self.tab_login)
        
        self.crear_contenido_encuestas()
        self.crear_contenido_participantes()
        self.crear_contenido_estudios()
        self.crear_contenido_reportes()

    def crear_contenido_encuestas(self):
        frame = ttk.Frame(self.tab_encuestas)
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        ttk.Button(frame, text="Nueva Encuesta", command=self.nueva_encuesta).pack(pady=5)
        ttk.Button(frame, text="Editar Encuesta", command=self.editar_encuesta).pack(pady=5)
        ttk.Button(frame, text="Ver Encuestas", command=self.ver_encuestas).pack(pady=5)

    def crear_contenido_participantes(self):
        frame = ttk.Frame(self.tab_participantes)
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        ttk.Button(frame, text="Cargar Participantes desde CSV", command=self.cargar_participantes_csv).pack(pady=5)
        ttk.Button(frame, text="Ver Participantes", command=self.ver_participantes).pack(pady=5)

    def crear_contenido_estudios(self):
        frame = ttk.Frame(self.tab_estudios)
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        ttk.Button(frame, text="Nuevo Estudio", command=self.nuevo_estudio).pack(pady=5)
        ttk.Button(frame, text="Ver Estudios", command=self.ver_estudios).pack(pady=5)

    def crear_contenido_reportes(self):
        frame = ttk.Frame(self.tab_reportes)
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        ttk.Button(frame, text="Cargar CSV", command=self.cargar_csv).pack(pady=5)
        ttk.Button(frame, text="Generar Reporte", command=self.generar_reporte).pack(pady=5)
        ttk.Button(frame, text="Exportar Reporte a PDF", command=self.exportar_reporte_pdf).pack(pady=5)

    def nueva_encuesta(self):
        titulo = simpledialog.askstring("Nueva Encuesta", "Ingrese el título de la encuesta:")
        if titulo:
            descripcion = simpledialog.askstring("Nueva Encuesta", "Ingrese la descripción de la encuesta:")
            nueva_encuesta = Encuesta(titulo, descripcion)
            self.encuestas.append(nueva_encuesta)
            self.agregar_preguntas(nueva_encuesta)

    def agregar_preguntas(self, encuesta):
        while True:
            texto = simpledialog.askstring("Nueva Pregunta", "Ingrese el texto de la pregunta (o cancele para terminar):")
            if not texto:
                break
            tipo = simpledialog.askstring("Nueva Pregunta", "Ingrese el tipo de pregunta (abierta/multiple):")
            nueva_pregunta = Pregunta(texto, tipo)
            if tipo == "multiple":
                self.agregar_opciones(nueva_pregunta)
            encuesta.agregar_pregunta(nueva_pregunta)

    def agregar_opciones(self, pregunta):
        while True:
            opcion = simpledialog.askstring("Nueva Opción", "Ingrese una opción (o cancele para terminar):")
            if not opcion:
                break
            pregunta.agregar_opcion(opcion)

    def editar_encuesta(self):
        if not self.encuestas:
            messagebox.showinfo("Información", "No hay encuestas para editar.")
            return
        
        encuesta_seleccionada = self.seleccionar_encuesta("Seleccione una encuesta para editar:")
        if encuesta_seleccionada:
            self.agregar_preguntas(encuesta_seleccionada)

    def ver_encuestas(self):
        if not self.encuestas:
            messagebox.showinfo("Información", "No hay encuestas para mostrar.")
            return
        
        encuesta_info = "\n\n".join([str(encuesta) for encuesta in self.encuestas])
        messagebox.showinfo("Encuestas", encuesta_info)

    def cargar_participantes_csv(self):
        if not self.estudio_actual:
            messagebox.showwarning("Advertencia", "Por favor, cree un estudio primero.")
            return

        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if file_path:
            try:
                self.estudio_actual.cargar_participantes_csv(file_path)
                messagebox.showinfo("Éxito", f"Se cargaron {len(self.estudio_actual.participantes)} participantes.")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo cargar el archivo CSV: {str(e)}")

    def ver_participantes(self):
        if not self.estudio_actual or not self.estudio_actual.participantes:
            messagebox.showinfo("Información", "No hay participantes para mostrar.")
            return
        
        participantes_info = "\n".join([str(participante) for participante in self.estudio_actual.participantes])
        messagebox.showinfo("Participantes", participantes_info)

    def nuevo_estudio(self):
        if not self.encuestas:
            messagebox.showwarning("Advertencia", "Por favor, cree una encuesta primero.")
            return

        nombre = simpledialog.askstring("Nuevo Estudio", "Ingrese el nombre del estudio:")
        if nombre:
            encuesta_seleccionada = self.seleccionar_encuesta("Seleccione una encuesta para el estudio:")
            if encuesta_seleccionada:
                nuevo_estudio = Estudio(nombre, encuesta_seleccionada)
                self.estudios.append(nuevo_estudio)
                self.estudio_actual = nuevo_estudio
                messagebox.showinfo("Éxito", f"Se creó el estudio '{nombre}'.")

    def ver_estudios(self):
        if not self.estudios:
            messagebox.showinfo("Información", "No hay estudios para mostrar.")
            return
        
        estudios_info = "\n\n".join([str(estudio) for estudio in self.estudios])
        messagebox.showinfo("Estudios", estudios_info)

    def seleccionar_encuesta(self, mensaje):
        opciones = [encuesta.titulo for encuesta in self.encuestas]
        seleccion = simpledialog.askstring("Seleccionar Encuesta", mensaje, initialvalue=opciones[0] if opciones else None)
        if seleccion in opciones:
            return next(encuesta for encuesta in self.encuestas if encuesta.titulo == seleccion)
        return None

    def cargar_csv(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if file_path:
            try:
                self.df = pd.read_csv(file_path, encoding='utf-8')
                self.reporte_actual = Reporte(self.df)
                messagebox.showinfo("Éxito", f"Archivo CSV cargado correctamente. {len(self.df)} filas encontradas.")
            except UnicodeDecodeError:
                try:
                    self.df = pd.read_csv(file_path, encoding='latin-1')
                    self.reporte_actual = Reporte(self.df)
                    messagebox.showinfo("Éxito", f"Archivo CSV cargado correctamente. {len(self.df)} filas encontradas.")
                except Exception as e:
                    messagebox.showerror("Error", f"No se pudo cargar el archivo CSV: {str(e)}")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo cargar el archivo CSV: {str(e)}")

    def generar_reporte(self):
        if self.reporte_actual is None:
            messagebox.showwarning("Advertencia", "Por favor, cargue un archivo CSV primero.")
            return

        reporte_window = tk.Toplevel(self.root)
        reporte_window.title("Reporte de Encuesta")
        reporte_window.geometry("800x600")

        notebook = ttk.Notebook(reporte_window)
        notebook.pack(expand=True, fill="both")

        self.crear_tab_resumen(notebook)
        self.crear_tab_grafico_barras(notebook)
        self.crear_tab_grafico_pastel(notebook)
        self.crear_tab_tabla_frecuencias(notebook)

    def crear_tab_resumen(self, notebook):
        tab_resumen = ttk.Frame(notebook)
        notebook.add(tab_resumen, text="Resumen")
        ttk.Label(tab_resumen, text=f"Total de respuestas: {len(self.reporte_actual.df)}").pack(pady=10)

    def crear_tab_grafico_barras(self, notebook):
        tab_grafico = ttk.Frame(notebook)
        notebook.add(tab_grafico, text="Gráfico de Barras")
        
        columnas = list(self.reporte_actual.df.columns)
        columna_seleccionada = tk.StringVar(value=columnas[0] if columnas else "")
        
        ttk.Label(tab_grafico, text="Seleccione una columna:").pack(pady=5)
        combo = ttk.Combobox(tab_grafico, textvariable=columna_seleccionada, values=columnas)
        combo.pack(pady=5)
        
        def actualizar_grafico(*args):
            for widget in tab_grafico.winfo_children()[3:]:
                widget.destroy()
            
            fig = self.reporte_actual.generar_grafico_barras(columna_seleccionada.get())
            if fig:
                canvas = FigureCanvasTkAgg(fig, master=tab_grafico)
                canvas_widget = canvas.get_tk_widget()
                canvas_widget.pack(fill=tk.BOTH, expand=True)
                canvas.draw()
        
        combo.bind("<<ComboboxSelected>>", actualizar_grafico)
        actualizar_grafico()

    def crear_tab_grafico_pastel(self, notebook):
        tab_pastel = ttk.Frame(notebook)
        notebook.add(tab_pastel, text="Gráfico de Pastel")
        
        columnas = list(self.reporte_actual.df.columns)
        columna_seleccionada = tk.StringVar(value=columnas[0] if columnas else "")
        
        ttk.Label(tab_pastel, text="Seleccione una columna:").pack(pady=5)
        combo = ttk.Combobox(tab_pastel, textvariable=columna_seleccionada, values=columnas)
        combo.pack(pady=5)
        
        def actualizar_grafico(*args):
            for widget in tab_pastel.winfo_children()[3:]:
                widget.destroy()
            
            fig = self.reporte_actual.generar_grafico_pastel(columna_seleccionada.get())
            if fig:
                canvas = FigureCanvasTkAgg(fig, master=tab_pastel)
                canvas_widget = canvas.get_tk_widget()
                canvas_widget.pack(fill=tk.BOTH, expand=True)
                canvas.draw()
        
        combo.bind("<<ComboboxSelected>>", actualizar_grafico)
        actualizar_grafico()

    def crear_tab_tabla_frecuencias(self, notebook):
        tab_tabla = ttk.Frame(notebook)
        notebook.add(tab_tabla, text="Tabla de Frecuencias")
        
        columnas = list(self.reporte_actual.df.columns)
        columna_seleccionada = tk.StringVar(value=columnas[0] if columnas else "")
        
        ttk.Label(tab_tabla, text="Seleccione una columna:").pack(pady=5)
        combo = ttk.Combobox(tab_tabla, textvariable=columna_seleccionada, values=columnas)
        combo.pack(pady=5)
        
        def actualizar_tabla(*args):
            for widget in tab_tabla.winfo_children()[3:]:
                widget.destroy()
            
            tabla = self.reporte_actual.generar_tabla_frecuencias(columna_seleccionada.get())
            if tabla is not None:
                tree = ttk.Treeview(tab_tabla, columns=('Opción', 'Frecuencia'), show='headings')
                tree.heading('Opción', text='Opción')
                tree.heading('Frecuencia', text='Frecuencia')
                for _, row in tabla.iterrows():
                    tree.insert('', 'end', values=(row['index'], row[columna_seleccionada.get()]))
                tree.pack(expand=True, fill='both')
        
        combo.bind("<<ComboboxSelected>>", actualizar_tabla)
        actualizar_tabla()

    def exportar_reporte_pdf(self):
        if self.reporte_actual is None:
            messagebox.showwarning("Advertencia", "Por favor, genere un reporte primero.")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")])
        if file_path:
            try:
                self.reporte_actual.exportar_pdf(file_path)
                messagebox.showinfo("Éxito", f"Reporte exportado a {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo exportar el reporte: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = SistemaGestionEncuestasGUI(root)
    root.mainloop()