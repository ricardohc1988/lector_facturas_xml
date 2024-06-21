from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import pyperclip
import locale
from lector import LeerFactura


class LectorFacturasApp(Tk):
    """
    Aplicación GUI para cargar y visualizar datos de facturas XML.

    Esta aplicación permite al usuario seleccionar un archivo XML de factura,
    cargarlo, mostrar información relevante como fecha, folio, receptor, etc.,
    y proporciona la opción de copiar ciertos datos al portapapeles.
    """
    def __init__(self):
        """
        Inicializa la ventana principal de la aplicación y configura sus componentes.
        """
        super().__init__()

        # Configurar ventana
        self.title("Lector de facturas")
        self.geometry("620x680")
        self.resizable(False, False)
        self.config(bg='#1B2631')

        # Cargar imagen para icono
        self.icono = PhotoImage(file='logo_th.png')
        self.iconphoto(True, self.icono)

        # Inicializar estilo
        s = ttk.Style()
        s.configure('TFrame', background='#33393b')
        s.configure('TLabel', background='#33393b', foreground='white')

        #Título
        label_titulo = ttk.Label(self, text="Lector de facturas XML", font=('Helvetica', 20, 'bold'), background='#1B2631', foreground='white')
        label_titulo.pack(pady=20, anchor='center')

        # Crear frame para los botones
        frame_botones = Frame(self, bg='#1B2631')
        frame_botones.pack(pady=20)

        # Crear botones
        btn_cargar = Button(frame_botones, text="Cargar factura", command=self.cargar_factura, width=20, height=2, background='#1b1f20', foreground='#ffffff', font=('Helvetica', 12), border=0, relief=FLAT, padx=10, pady=6)
        btn_cargar.pack(side=LEFT, padx=(10, 10), pady=(0, 0))
        btn_salir = Button(frame_botones, text="Salir", command=self.salir, width=20, height=2, background='#1b1f20', foreground='#ffffff', font=('Helvetica', 12), border=0, relief=FLAT, padx=10, pady=6)
        btn_salir.pack(side=LEFT, padx=(0, 10), pady=(0, 0))

        # Crear panel principal
        self.panel_principal = ttk.Frame(self, width=1080, height=610)
        self.panel_principal.pack(pady=20)
        self.panel_principal.pack_propagate(False)

        # Variable para almacenar nombre de las etiquetas de la factura.
        etiquetas_factura = [
            ("Fecha:", "etiqueta_fecha"),
            ("Folio de factura:", "etiqueta_folio"),
            ("Receptor:", "etiqueta_receptor"),
            ("Número de Pedido:", "etiqueta_pedido"),
            ("Número de Remisión:", "etiqueta_remision"),
            ("Total:", "etiqueta_total"),
        ]
        
        # Crear etiquetas
        for i, (text, label_name) in enumerate( etiquetas_factura, start=1):
            label = ttk.Label(self.panel_principal, text=text, font=('Helvetica', 14, 'bold'))
            label.grid(row=i, column=0, sticky='w', padx=(20, 0), pady=5)

            setattr(self, label_name, ttk.Label(self.panel_principal, text="No se ha seleccionado ningún archivo", font=('Helvetica', 12), background='#1b1f20', width=30))
            getattr(self, label_name).grid(row=i, column=1, sticky='w', pady=5)

            btn_copiar = Button(self.panel_principal, text="Copiar", command=lambda label_name=label_name: self.copiar_al_portapapeles(getattr(self, label_name).cget("text")))
            btn_copiar.grid(row=i, column=2, padx=(10, 0), pady=5, sticky='w')

        locale.setlocale(locale.LC_MONETARY, 'es_MX.UTF-8')

        self.factura_cargada = False

    def mostrar_conceptos(self, conceptos):
        """
        Muestra los conceptos (productos) de la factura en un widget Treeview.

        Args:
        - conceptos (list): Lista de diccionarios con los detalles de cada concepto.
        """
        for widget in self.panel_principal.winfo_children():
            if isinstance(widget, ttk.Treeview):
                widget.destroy()

        etiqueta_conceptos = ttk.Label(self.panel_principal, text="Conceptos:", font=('Helvetica', 14, 'bold'))
        etiqueta_conceptos.grid(row=7, column=0, sticky='w', padx=(20, 0), pady=5)

        tree = ttk.Treeview(self.panel_principal, columns=("Código", "Descripción", "Cantidad"), show="headings", height=len(conceptos))
        tree.heading("Código", text="Código")
        tree.heading("Descripción", text="Descripción")
        tree.heading("Cantidad", text="Cantidad")
        tree.column("Código", anchor="center", width=120)
        tree.column("Descripción", anchor="center", width=350)
        tree.column("Cantidad", anchor="center", width=80)

        tree.grid(row=8, column=0, columnspan=3, pady=5, sticky='w')

        for concepto in conceptos:
            tree.insert("", "end", values=(concepto['codigo'], concepto['descripcion'], concepto['cantidad']))

    def cargar_factura(self):
        """
        Abre un cuadro de diálogo para seleccionar un archivo XML de factura,
        carga los datos de la factura seleccionada y actualiza la interfaz gráfica
        con los detalles de la factura.
        """
        archivo = filedialog.askopenfilename(title="Selecciona archivo", filetypes=[("Archivos XML", "*.xml")])
        if archivo:
            factura = LeerFactura(archivo)
            self.datos = factura.datos_completos()
            self.factura_cargada = True
            total = 0
            for i in range(len(self.datos['productos'])):
                total += float(self.datos['productos'][i]['total'])

            self.etiqueta_folio.config(text=self.datos['factura'])
            self.etiqueta_receptor.config(text=self.datos['nombre'])
            self.etiqueta_fecha.config(text=self.datos['fecha'])
            self.etiqueta_pedido.config(text=self.datos['numero_pedido'] if self.datos['numero_pedido'] else "No disponible")
            self.etiqueta_remision.config(text=self.datos['numero_remision'] if self.datos['numero_remision'] else "No disponible")
            self.etiqueta_total.config(text=locale.currency(total, grouping=True))

            self.mostrar_conceptos(self.datos['productos'])

        else:
            return
        
    def copiar_al_portapapeles(self, dato):
        """
        Copia un dato específico al portapapeles del sistema.

        Args:
        - dato (str): Dato a copiar.
        """
        pyperclip.copy(dato)
        messagebox.showinfo('Copiado', f'{dato} copiado al portapapeles.')

    def salir(self):
        """
        Muestra un mensaje de confirmación y cierra la aplicación si el usuario confirma.
        """
        if messagebox.askyesno('Salir', 'Quieres salir del programa?'):
            self.destroy()


if __name__ == '__main__':
    app = LectorFacturasApp()
    app.mainloop()
