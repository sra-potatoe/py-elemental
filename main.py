import tkinter as tk
from tkinter import messagebox
import csv
from datetime import datetime
import firebase_admin
from firebase_admin import credentials, firestore
from PIL import Image, ImageTk 

cred = credentials.Certificate(r"C:\Users\Erick\Documents\proyecto\class-py-elemental-firebase-adminsdk-487m7-ca6ea5cf6f.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

class FinanzasApp:
    def __init__(self, master):
        self.master = master
        master.title("Gestor de Finanzas Personales")
        master.configure(bg="#f0f0f0")
        
        self.ingresos = []
        self.egresos = []

        self.logo_image = Image.open(r"C:\Users\Erick\Documents\proyecto\logo.png")
        self.logo_image = self.logo_image.resize((50, 50))  # Elimina Image.ANTIALIAS
        self.logo = ImageTk.PhotoImage(self.logo_image)
        
        logo_frame = tk.Frame(master, bg="#f0f0f0")
        logo_frame.pack(pady=10)
        
        self.logo_label = tk.Label(logo_frame, image=self.logo, bg="#f0f0f0")
        self.logo_label.pack(side=tk.LEFT)

        title_frame = tk.Frame(master, bg="#f0f0f0")
        title_frame.pack(pady=10)
        
        self.title_label = tk.Label(title_frame, text="Gestor de Finanzas Personales", font=("Arial", 20), bg="#f0f0f0")
        self.title_label.pack()
        
        self.dashboard_frame = tk.Frame(master, bg="#ffffff", bd=2, relief=tk.SUNKEN)
        self.dashboard_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        self.ingreso_label = tk.Label(self.dashboard_frame, text="Total Ingresos: $0.00", font=("Arial", 16), bg="#ffffff")
        self.ingreso_label.pack(pady=5)

        self.egreso_label = tk.Label(self.dashboard_frame, text="Total Egresos: $0.00", font=("Arial", 16), bg="#ffffff")
        self.egreso_label.pack(pady=5)

        self.ingreso_button = tk.Button(master, text="Registrar Ingresos", command=self.registrar_ingresos, width=20, bg="#4CAF50", fg="white")
        self.ingreso_button.pack(pady=5)

        self.egreso_button = tk.Button(master, text="Registrar Egresos", command=self.registrar_egresos, width=20, bg="#f44336", fg="white")
        self.egreso_button.pack(pady=5)

        self.reporte_button = tk.Button(master, text="Generar Reporte", command=self.generar_reporte, width=20, bg="#2196F3", fg="white")
        self.reporte_button.pack(pady=5)

        self.salir_button = tk.Button(master, text="Salir", command=master.quit, width=20, bg="#9E9E9E", fg="white")
        self.salir_button.pack(pady=5)

        self.cargar_datos() 
        self.actualizar_dashboard() 

    def cargar_datos(self):
        ingresos_ref = db.collection('ingresos').stream()
        self.ingresos = [{'fecha': doc.id, 'ingreso': doc.to_dict()['ingreso']} for doc in ingresos_ref]

        # Cargar egresos desde Firestore
        egresos_ref = db.collection('egresos').stream()
        self.egresos = [{'fecha': doc.id, 'egreso': doc.to_dict()['egreso']} for doc in egresos_ref]

    def registrar_ingresos(self):
        self.open_ingreso_window()

    def registrar_egresos(self):
        self.open_egreso_window()

    def generar_reporte(self):
        self.open_reporte_window()

    def open_ingreso_window(self):
        self.ingreso_window = tk.Toplevel(self.master)
        self.ingreso_window.title("Registro de Ingresos")
        self.ingreso_window.configure(bg="#f0f0f0")

        self.label_ingreso = tk.Label(self.ingreso_window, text="Ingreso:", bg="#f0f0f0")
        self.label_ingreso.pack()
        self.ingreso_entry = tk.Entry(self.ingreso_window)
        self.ingreso_entry.pack()

        self.submit_button = tk.Button(self.ingreso_window, text="Agregar", command=self.agregar_ingreso, bg="#4CAF50", fg="white")
        self.submit_button.pack()

    def agregar_ingreso(self):
        try:
            ingreso = float(self.ingreso_entry.get())
            fecha = datetime.now().strftime('%Y-%m-%d')
            self.ingresos.append({'fecha': fecha, 'ingreso': ingreso})
            self.guardar_datos()  # Guardar en Firestore
            messagebox.showinfo("Éxito", f"Ingreso agregado: {ingreso}")

            self.actualizar_dashboard()
            self.ingreso_window.destroy()
        except ValueError:
            messagebox.showerror("Error", "Por favor ingrese un valor válido para el ingreso.")

    def open_egreso_window(self):
        self.egreso_window = tk.Toplevel(self.master)
        self.egreso_window.title("Registro de Egresos")
        self.egreso_window.configure(bg="#f0f0f0")

        self.label_egreso = tk.Label(self.egreso_window, text="Egreso:", bg="#f0f0f0")
        self.label_egreso.pack()
        self.egreso_entry = tk.Entry(self.egreso_window)
        self.egreso_entry.pack()

        self.submit_button = tk.Button(self.egreso_window, text="Agregar", command=self.agregar_egreso, bg="#f44336", fg="white")
        self.submit_button.pack()

    def agregar_egreso(self):
        try:
            egreso = float(self.egreso_entry.get())
            fecha = datetime.now().strftime('%Y-%m-%d')
            self.egresos.append({'fecha': fecha, 'egreso': egreso})
            self.guardar_datos() 
            messagebox.showinfo("Éxito", f"Egreso agregado: {egreso}")

            self.actualizar_dashboard()
            self.egreso_window.destroy()
        except ValueError:
            messagebox.showerror("Error", "Por favor ingrese un valor válido para el egreso.")

    def open_reporte_window(self):
        self.reporte_window = tk.Toplevel(self.master)
        self.reporte_window.title("Generación de Reportes")
        self.reporte_window.configure(bg="#f0f0f0")

        self.reporte_button_csv = tk.Button(self.reporte_window, text="Generar CSV", command=self.generar_csv, bg="#2196F3", fg="white")
        self.reporte_button_csv.pack(pady=5)

        self.reporte_button_txt = tk.Button(self.reporte_window, text="Generar Resumen", command=self.generar_resumen, bg="#2196F3", fg="white")
        self.reporte_button_txt.pack(pady=5)

    def generar_csv(self):
        with open('reportes.csv', mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=['fecha', 'ingreso', 'egreso'])
            writer.writeheader()
            for ingreso in self.ingresos:
                writer.writerow({'fecha': ingreso['fecha'], 'ingreso': ingreso['ingreso'], 'egreso': ''})
            for egreso in self.egresos:
                writer.writerow({'fecha': egreso['fecha'], 'ingreso': '', 'egreso': egreso['egreso']})
        messagebox.showinfo("Éxito", "Reporte CSV generado con éxito")

    def generar_resumen(self):
        total_ingresos = sum(item['ingreso'] for item in self.ingresos)
        total_egresos = sum(item['egreso'] for item in self.egresos)
        resumen = f"Total Ingresos: {total_ingresos}\nTotal Egresos: {total_egresos}\nBalance: {total_ingresos - total_egresos}"
        with open('reporte.txt', 'w') as file:
            file.write(resumen)
        messagebox.showinfo("Éxito", "Resumen generado con éxito")

    def guardar_datos(self):
        # Guardar datos en Firestore
        for ingreso in self.ingresos:
            db.collection('ingresos').document(ingreso['fecha']).set({'ingreso': ingreso['ingreso']})

        for egreso in self.egresos:
            db.collection('egresos').document(egreso['fecha']).set({'egreso': egreso['egreso']})

    def actualizar_dashboard(self):
        total_ingresos = sum(item['ingreso'] for item in self.ingresos)
        total_egresos = sum(item['egreso'] for item in self.egresos)

        self.ingreso_label.config(text=f"Total Ingresos: ${total_ingresos:.2f}")
        self.egreso_label.config(text=f"Total Egresos: ${total_egresos:.2f}")

if __name__ == "__main__":
    root = tk.Tk()
    app = FinanzasApp(root)
    root.mainloop()
