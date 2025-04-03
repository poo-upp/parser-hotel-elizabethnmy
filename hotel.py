from datetime import datetime, timedelta
from collections import Counter

class Habitacion:
    def __init__(self, numero, capacidad, precio, disponible=True):
        self.numero = numero
        self.capacidad = capacidad
        self.precio = precio
        self._disponible = disponible  

    @property
    def disponible(self):
        return self._disponible

    @disponible.setter
    def disponible(self, estado):
        self._disponible = estado

    def __eq__(self, otra):
        return (self.numero == otra.numero and
                self.capacidad == otra.capacidad and
                self.precio == otra.precio)

    def __add__(self, otra):
        return self.precio + otra.precio

class HabitacionSimple(Habitacion):
    def __init__(self, numero):
        super().__init__(numero, capacidad=1, precio=450)
    
    def __str__(self):
        return "Habitacion simple"

class HabitacionDoble(Habitacion):
    def __init__(self, numero, balcon=False):
        super().__init__(numero, capacidad=2, precio=900)
        self.balcon = balcon  
    
    def __str__(self):
        return "Habitacion doble"
    
class Suite(Habitacion):
    def __init__(self, numero, jacuzzi=False):
        super().__init__(numero, capacidad=4, precio=2500)
        self.jacuzzi = jacuzzi 
        
    def __str__(self):
        return "Suite"

class Cliente:
    def __init__(self, nombre, correo):
        self.nom = nombre
        self.correo = correo
        self.reservas = []

class Reserva:
    def __init__(self, cliente, habitaciones, fecha_inicio, num_noches):
        self.cliente = cliente
        self.habitaciones = habitaciones
        self.fecha_inicio = fecha_inicio
        self.num_noches = num_noches
        
    
        fecha_inicio_obj = datetime.strptime(fecha_inicio, "%d-%m-%Y")
        fecha_fin_obj = fecha_inicio_obj + timedelta(days=num_noches)
        self.fecha_fin = fecha_fin_obj.strftime("%d-%m-%Y")
        
        self.num_habitaciones = len(habitaciones)
        self.num_personas = sum(h.capacidad for h in habitaciones)
        self.precio_total = sum(h.precio for h in habitaciones)
        
        self.cliente.reservas.append(self)

        for habitacion in habitaciones:
            habitacion.disponible = False


def parser(documento):
    cliente = None
    correo = None
    num_noches = None
    fecha_inicio = None
    habitaciones = []
    
    leyendo_habitaciones = False
    
    with open(documento, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()  
            
            if not line:
                continue
                
            if "Nombre del cliente" in line:
                for next_line in file:
                    next_line = next_line.strip()
                    if next_line:
                        cliente = Cliente(next_line, '')
                        break
            
            elif "correo" in line:
                parts = line.split()
                correo = parts[1]
                if cliente:
                    cliente.correo = correo
            
            elif "numero de noches" in line:
                parts = line.split()
                num_noches = int(parts[-1])
            
            elif "fecha inicio" in line:
                parts = line.split()
                fecha_inicio = parts[-1]
            
            elif "----Habitaciones-----" in line:
                if not leyendo_habitaciones:
                    leyendo_habitaciones = True
                else:
                    leyendo_habitaciones = False
            
            elif leyendo_habitaciones:
                if "simple" in line.lower():
                    habitaciones.append(HabitacionSimple(len(habitaciones) + 1))
                elif "doble" in line.lower():
                    habitaciones.append(HabitacionDoble(len(habitaciones) + 1))
                elif "suite" in line.lower():
                    habitaciones.append(Suite(len(habitaciones) + 1))
  
    if cliente and num_noches and fecha_inicio and habitaciones:
        reserva = Reserva(cliente, habitaciones, fecha_inicio, num_noches)
        return reserva
    else:
        print("No se pudieron extraer todos los datos necesarios del archivo.")
        return None


def generar_reporte(reserva, archivo_salida="output.txt"):
    
    tipo_habitaciones = Counter([str(h) for h in reserva.habitaciones])
    
    with open(archivo_salida, 'w', encoding='utf-8') as file:
        file.write(f"¡Hola {reserva.cliente.nom}! aqui tienes los detalles de te reserva:\n\n")
        file.write(f"Check-in: \t{reserva.fecha_inicio}\n")
        file.write(f"Checl out:\t{reserva.fecha_fin}\n\n")
        file.write(f"Reservaste\t[{reserva.num_noches}] noches, [{reserva.num_habitaciones}] habitaciones, [{reserva.num_personas}] personas\n\n")
        file.write("Detalles de reserva\n")
        
        for tipo, cantidad in tipo_habitaciones.items():
            file.write(f"[{cantidad}] \t{tipo}\n")
        
        file.write(f"\ne-mail de contacto\t[{reserva.cliente.correo}]\n\n\n")
        file.write("Detalles del precio:\n")
    
        precio_total = 0
        for tipo_hab in ["Habitacion simple", "Habitacion doble", "Suite"]:
            cantidad = tipo_habitaciones.get(tipo_hab, 0)
            if cantidad > 0:
                precio = 0
                if tipo_hab == "Habitacion simple":
                    precio = 400.00
                elif tipo_hab == "Habitacion doble":
                    precio = 900.00
                elif tipo_hab == "Suite":
                    precio = 2500.00
                    
                file.write(f"[{cantidad}] \t{tipo_hab}")
                if tipo_hab == "Habitacion simple" or tipo_hab == "Habitacion doble":
                    file.write(f"\t\t {precio:.2f}$\n")
                else:  
                    file.write(f"\t\t\t\t{precio:.2f}$\n")
                precio_total += precio * cantidad
                
        file.write("-" * 46 + "\n")
        file.write(f"Total:\t\t\t\t\t\t\t{precio_total:.2f}$\n")
        
    print(f"Reporte generado en {archivo_salida}")


if __name__ == "__main__":
    archivo_entrada = "input.txt"
    reserva = parser(archivo_entrada)
    
    if reserva:
        generar_reporte(reserva, "output.txt")
        print(f"Cliente: {reserva.cliente.nom}")
        print(f"Correo: {reserva.cliente.correo}")
        print(f"Fecha de inicio: {reserva.fecha_inicio}")
        print(f"Fecha de fin: {reserva.fecha_fin}")
        print(f"Número de noches: {reserva.num_noches}")
        print(f"Número de habitaciones: {reserva.num_habitaciones}")
        print(f"Número de personas: {reserva.num_personas}")
        print(f"Precio total: {reserva.precio_total}")