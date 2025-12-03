import os

# ==============================================================================
# PROYECTO FINAL: SISTEMA DE INVENTARIO
# MATERIA: PROGRAMACIÓN I
# GRUPO: TEAM FRUTA
#
#
# ---ALGUNAS NOTAS:---
#
# * Decidimos usar una lista para manejar los productos y archivos de texto
#   para que los datos no se borren al salir del programa.
#
# * Implementamos una lógica de "carrito" en la caja para poder cobrar varios
#   productos juntos al final. Incluimos cálculo de ITBIS automático y un
#   historial de ventas para llevar el control de todo lo facturado.
#
# * Para no perder tiempo, le pusimos bucles a las opciones. Así podemos
#   agregar o vender muchas cosas seguidas sin que el sistema nos saque al
#   menú principal a cada rato.
#
# * Protegimos el código para que no se cierre con error si alguien escribe
#   letras en los números. También pusimos la opción de cancelar con la
#   letra 'F' en cualquier momento por si uno se equivoca.
#
# * Al actualizar productos, usamos variables temporales para que si uno
#   cancela la edición a la mitad, no se queden los datos guardados a medias.
# ==============================================================================

# --- VARIABLES FIJAS (CONSTANTES) ---
ARCHIVO_DATOS = "datos_market.txt"
ARCHIVO_HISTORIAL = "historial_ventas.txt"
TASA_ITBIS = 0.18

# Nuestra lista para guardar todo (Memoria RAM)
inventario = []

# --- FUNCIÓN PARA LIMPIAR LA PANTALLA ---
def limpiar():
    try:
        # Intentamos borrar de forma "profesional"
        if os.name == 'nt':
            os.system("cls")
        else:
            os.system("clear")
    except:
        pass
   
# --- 1. MANEJO DE ARCHIVOS ---

def guardar_cambios():
    # Aquí guardaremos todo lo que está en la lista dentro del archivo
    try:
        archivo = open(ARCHIVO_DATOS, "w")
        for p in inventario:
            archivo.write(f"{p['nombre']},{p['cantidad']},{p['precio']:.2f}\n")
        archivo.close()
    except:
        print("Tuvimos un problema al intentar guardar el archivo.")


def cargar_inicio():
    # Verificamos si el archivo existe para evitar errores raros
    if os.path.exists(ARCHIVO_DATOS):
        try:
            archivo = open(ARCHIVO_DATOS, "r")
            for linea in archivo:
                try:
                    datos = linea.strip().split(",")
                    if len(datos) == 3:
                        nuevo_prod = {
                            "nombre": datos[0],
                            "cantidad": int(datos[1]),
                            "precio": float(datos[2])
                        }
                        inventario.append(nuevo_prod)
                except:
                    continue # Si una línea está mala, la saltamos
            archivo.close()
        except Exception as e:
            print("AVISO: Tuvimos un problema al cargar los datos.")
            print(f"Error: {e}")
            input("Presiona ENTER para iniciar vacío (ten cuidado)...")
    else:
        # Si no existe, es la primera vez, Tranquilos
        pass


def registrar_historial(nombre_prod, cant, total_cobrado):
    try:
        archivo = open(ARCHIVO_HISTORIAL, "a")
        linea = f"VENTA: Producto: {nombre_prod} | Cant: {cant} | Total: RD${total_cobrado:.2f}\n"
        archivo.write(linea)
        archivo.close()
    except:
        print("No se pudo guardar la venta en el historial.")


# --- 2. FUNCIONES DEL SISTEMA ---

def agregar_nuevo():
    limpiar()
    print("\n--- AGREGAR PRODUCTO ---")
    
    while True:
        print("\n--- Nuevo Ingreso ---")

        # 1. Pedir Nombre
        while True:
            nombre = input("Nombre del producto (o 'F' para cancelar): ").strip().capitalize().replace(",", "")

            if nombre.upper() == "F":
                return 

            if nombre == "":
                print("El dato que acabas de colocar no es válido. El nombre es obligatorio.")
                continue

            existe = False
            for p in inventario:
                if p["nombre"] == nombre:
                    print("El dato que acabas de colocar no es válido. Ese producto ya existe.")
                    existe = True
                    break

            if not existe:
                break

        # 2. Pedir Cantidad
        while True:
            entrada = input(f"Cantidad de '{nombre}' (o 'F' para cancelar): ")
            if entrada.upper() == "F": return

            try:
                cant = int(entrada)
                if cant >= 0: break
                print("El dato que acabas de colocar no es válido. No use negativos.")
            except:
                print("Debes ingresar solo números enteros.")

        # 3. Pedir Precio
        while True:
            entrada = input(f"Precio de '{nombre}' RD$ (o 'F' para cancelar): ")
            if entrada.upper() == "F": return

            try:
                precio = float(entrada)
                if precio >= 0: break
                print("El dato que acabas de colocar no es válido. El precio debe ser positivo.")
            except:
                print("Debes ingresar solo números válidos.")

        # Guardamos en la lista y en el archivo
        inventario.append({"nombre": nombre, "cantidad": cant, "precio": precio})
        print(f"¡Listo! El producto '{nombre}' fue agregado correctamente.")
        guardar_cambios()
        
        # Pregunta para seguir agregando sin salir
        print("-" * 30)
        seguir = input("¿Quieres agregar otro producto? (S/N): ")
        if seguir.strip().upper() == "N":
            return 


def actualizar_stock():
    limpiar()
    print("\n--- ACTUALIZAR EXISTENCIAS ---")
    print("Nota: Escribe 'F' en el nombre para volver al menú.")

    while True:
        print("\n--- Buscar Producto ---")
        busqueda = input("Nombre del producto (o 'F' para salir): ").strip().capitalize()
        
        if busqueda.upper() == "F": 
            return

        encontrado = False
        
        for p in inventario:
            if p["nombre"] == busqueda:
                encontrado = True
                print(f"Producto: {p['nombre']} | Cantidad: {p['cantidad']} | Precio: RD${p['precio']:.2f}")
                print("(Si no quieres cambiar el dato, solo dale a ENTER)")

                # Variables temporales para no dañar nada si cancelan
                temp_cantidad = p["cantidad"]
                temp_precio = p["precio"]
                hubo_cambios = False

                # 1. Modificar Cantidad
                entrada_cant = input("Nueva Cantidad (o 'F' para salir): ")
                if entrada_cant.upper() == "F": return

                if entrada_cant != "":
                    try:
                        temp_cantidad = int(entrada_cant)
                        if temp_cantidad != p["cantidad"]:
                            hubo_cambios = True
                    except:
                        print("Debes ingresar solo números. Se dejaste la cantidad igual.")

                # 2. Modificar Precio
                entrada_precio = input("Nuevo Precio RD$ (o 'F' para salir): ")
                if entrada_precio.upper() == "F": return

                if entrada_precio != "":
                    try:
                        temp_precio = float(entrada_precio)
                        if temp_precio != p["precio"]:
                            hubo_cambios = True
                    except:
                        print("Debes ingresar solo números. Se dejaste el precio igual.")

                # Guardamos solo si de verdad cambió algo
                if hubo_cambios:
                    p["cantidad"] = temp_cantidad
                    p["precio"] = temp_precio
                    guardar_cambios()
                    print("¡Datos actualizados correctamente!")
                else:
                    print("Ningún dato fue actualizado.")
                
                break 

        if not encontrado:
            print("No encontramos ese producto en el sistema.")

        # Pregunta para seguir actualizando
        print("-" * 30)
        seguir = input("¿Deseas actualizar otro producto? (S/N): ")
        if seguir.strip().upper() == "N":
            return 


def eliminar_producto():
    limpiar()
    print("\n--- ELIMINAR PRODUCTO ---")

    while True:
        print("\n--- Borrar ---")
        nombre = input("Nombre a borrar (o 'F' para salir): ").strip().capitalize()
        if nombre.upper() == "F": return

        borrado = False
        # Usamos [:] para hacer una copia y borrar seguro
        for p in inventario[:]:
            if p["nombre"] == nombre:
                inventario.remove(p)
                print("Producto eliminado del sistema.")
                guardar_cambios()
                borrado = True
                break

        if not borrado:
            print("No encontramos ese nombre.")
        
        print("-" * 30)
        seguir = input("¿Deseas eliminar otro producto? (S/N): ")
        if seguir.strip().upper() == "N":
            return


def ver_lista_productos():
    limpiar()
    print("\n--- CONSULTAR INVENTARIO ---")
    if len(inventario) == 0:
        print("El inventario está vacío.")
        input("Presiona ENTER para volver...")
        return

    print("1. Ver orden normal (como llegaron)")
    print("2. Ver ordenado alfabéticamente (A-Z)")
    opcion = input("Opción (o 'F' para cancelar): ")
    if opcion.upper() == "F": return

    lista_temporal = list(inventario)

    if opcion == "2":
        lista_temporal.sort(key=lambda x: x["nombre"])

    print("-" * 50)
    print("PRODUCTO \t| CANT \t| PRECIO (RD$)")
    print("-" * 50)
    for p in lista_temporal:
        print(f"{p['nombre']} \t| {p['cantidad']} \t| RD${p['precio']:.2f}")

    print("-" * 50)
    input("Presiona ENTER para volver al menú...")


def reporte_bajo_stock():
    limpiar()
    print("\n--- REPORTE STOCK BAJO ---")
    try:
        entrada = input("Avísame si hay menos de (o 'F' para cancelar): ")
        if entrada.upper() == "F": return

        minimo = int(entrada)
        encontrado = False

        for p in inventario:
            if p["cantidad"] < minimo:
                print(f"ATENCIÓN: {p['nombre']} tiene pocas unidades ({p['cantidad']}).")
                encontrado = True

        if not encontrado:
            print("Todo bien. No hay productos en alerta.")
    except:
        print("Debes ingresar solo números enteros.")

    input("\nPresiona ENTER para volver...")


def reporte_valor_inventario():
    limpiar()
    print("\n--- VALOR TOTAL ---")
    total_dinero = 0
    mayor_stock = -1
    nombre_mayor = ""

    for p in inventario:
        total_dinero += p["cantidad"] * p["precio"]

        if p["cantidad"] > mayor_stock:
            mayor_stock = p["cantidad"]
            nombre_mayor = p["nombre"]

    print(f"Total invertido en el negocio: RD${total_dinero:,.2f}")
    if nombre_mayor != "":
        print(f"El producto con más stock es: {nombre_mayor}")

    input("\nPresiona ENTER para volver...")


def facturar_caja():
    limpiar()
    print("\n--- CAJA REGISTRADORA ---")
    
    while True: # Bucle de clientes
        
        # Creamos un carrito vacío para el cliente
        carrito = [] 
        print(f"\n>>> ATENDIENDO CLIENTE <<<")

        # --- FASE 1: LLENAR EL CARRITO ---
        while True:
            print(f"\n--- En el carrito: {len(carrito)} productos ---")
            busqueda = input("Producto a agregar (o 'F' para cobrar): ").strip().capitalize()
            
            if busqueda.upper() == "F":
                break # Sale de agregar y va a cobrar
            
            encontrado = False
            for p in inventario:
                if p["nombre"] == busqueda:
                    encontrado = True
                    print(f"Producto: {p['nombre']} | Precio: RD${p['precio']:.2f} | Stock: {p['cantidad']}")
                    
                    try:
                        cant = int(input("¿Cuántos lleva?: "))
                        
                        if cant <= 0:
                            print("El dato que acabas de colocar no es válido (mayor a 0).")
                        elif cant > p["cantidad"]:
                            print(f"No hay tantos. Solo quedan {p['cantidad']}.")
                        else:
                            # Agregamos al carrito temporalmente
                            carrito.append({
                                "nombre": p["nombre"],
                                "cantidad": cant,
                                "precio": p["precio"]
                            })
                            print(f"--> Agregado: {cant} x {p['nombre']}")
                    except:
                        print("Debes ingresar solo números.")
                    break 
            
            if not encontrado:
                print("No encontramos ese producto.")

        # --- FASE 2: COBRAR ---
        if len(carrito) > 0:
            print("\n" + "="*35)
            print("      LA FRUTA MARKET - FACTURA")
            print("="*35)
            
            subtotal_general = 0
            
            # Recorremos el carrito para procesar todo junto
            for item in carrito:
                costo_item = item['cantidad'] * item['precio']
                subtotal_general += costo_item
                
                # AHORA SÍ restamos del inventario real
                for p_real in inventario:
                    if p_real['nombre'] == item['nombre']:
                        p_real['cantidad'] -= item['cantidad']
                        break
                
                # Imprimimos línea
                print(f"{item['cantidad']} x {item['nombre']} - RD${costo_item:.2f}")
                
                # Guardamos en historial
                total_con_itbis_item = costo_item * (1 + TASA_ITBIS)
                registrar_historial(item['nombre'], item['cantidad'], total_con_itbis_item)

            # Totales finales
            itbis_total = subtotal_general * TASA_ITBIS
            gran_total = subtotal_general + itbis_total
            
            print("-" * 35)
            print(f"Subtotal:    RD${subtotal_general:.2f}")
            print(f"ITBIS (18%): RD${itbis_total:.2f}")
            print(f"TOTAL:       RD${gran_total:.2f}")
            print("="*35)
            print("       Gracias por su compra        ")
            
            guardar_cambios()
            input("\n(Presiona ENTER para entregar factura...)")
        else:
            print("\nEl carrito estaba vacío. No se hizo venta.")

        # --- PREGUNTA FINAL ---
        print("-" * 30)
        seguir = input("¿Hay otro cliente en la fila? (S/N): ")
        if seguir.strip().upper() == "N":
            return
        
        limpiar() # Limpiamos para el siguiente cliente de La Fruta Market


# --- MENU PRINCIPAL ---
def menu_principal():
    cargar_inicio()

    while True:
        limpiar()
        print("\n" + "=" * 40)
        print("      SISTEMA DE INVENTARIO (RD)")
        print("          LA FRUTA MARKET")
        print("=" * 40)
        print("1. Agregar Mercancía")
        print("2. Actualizar Producto")
        print("3. Eliminar Producto")
        print("4. Consultar Inventario (Ordenar)")
        print("5. Reporte: Stock Bajo")
        print("6. Reporte: Valor Total")
        print("7. Facturar (Caja con ITBIS)")
        print("8. Salir")
        print("-" * 40)

        op = input("Seleccione una opción: ")

        if op == "1":
            agregar_nuevo()
        elif op == "2":
            actualizar_stock()
        elif op == "3":
            eliminar_producto()
        elif op == "4":
            ver_lista_productos()
        elif op == "5":
            reporte_bajo_stock()
        elif op == "6":
            reporte_valor_inventario()
        elif op == "7":
            facturar_caja()
        elif op == "8":
            print("Cerrando sistema... ¡Nos vemos!")
            break
        else:
            print("El dato que acabas de colocar no es válido, intenta de nuevo.")
            input("Enter para continuar...")


if _name_ == "_main_":
    menu_principal()
