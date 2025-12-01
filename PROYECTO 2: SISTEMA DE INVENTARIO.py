# ==============================================================================
# PROYECTO FINAL: SISTEMA DE INVENTARIO
# MATERIA1
# : PROGRAMACIÓN I
# PROFESOR: LUIS JOSE RAMON
# GRUPO # 2: TEAM FRUTA
# TIENDA: LA FRUTA MARKET
#
# NOTAS:
# Decidimos usar una lista de diccionarios porque es la forma más fácil
# de mantener juntos el nombre, precio y cantidad de cada cosa.
# Usamos archivos de texto (.txt) para que el inventario no se # borre 
# cuando cerramos el programa.
# Le pusimos la opción de cancelar con la letra 'F' en todos lados por si
# el usuario entra a una opción por error.
# Agregamos el cálculo del ITBIS automático y un historial de ventas.
# ==============================================================================

# Esta es nuestra lista principal donde guardamos todos los productos
inventario = []

# --- 1. PARTE DE LOS ARCHIVOS (Para que no se pierdan los datos) ---

def guardar_cambios():
    # Esta función guarda lo que tenemos en memoria en el archivo de texto
    try:
        archivo = open("datos_market.txt", "w")
        for p in inventario:
            # Guardamos separado por comas y con dos decimales en el precio
            archivo.write(f"{p['nombre']},{p['cantidad']},{p['precio']:.2f}\n")
        archivo.close()
    except:
        print("Tuvimos un problema al intentar guardar el archivo.")

def cargar_inicio():
    # Esta función lee el archivo cuando abrimos el programa
    try:
        archivo = open("datos_market.txt", "r")
        for linea in archivo:
            try:
                # Cortamos la línea donde están las comas
                datos = linea.strip().split(",")
                
                # Verificamos que la línea tenga los 3 datos que necesitamos
                if len(datos) == 3: 
                    nuevo_prod = {
                        "nombre": datos[0], 
                        "cantidad": int(datos[1]), 
                        "precio": float(datos[2])
                    }
                    inventario.append(nuevo_prod)
            except:
                # Si una línea está mala, la saltamos y seguimos con la otra
                continue
        archivo.close()
    except:
        # Si no existe el archivo (es la primera vez), no hacemos nada
        pass 

def registrar_historial(nombre_prod, cant, total_cobrado):
    # Esto es un extra: guardamos cada venta en un archivo aparte
    try:
        # Usamos 'a' (append) para agregar al final sin borrar lo anterior
        archivo = open("historial_ventas.txt", "a")
        linea = f"VENTA: Producto: {nombre_prod} | Cant: {cant} | Total: RD${total_cobrado:.2f}\n"
        archivo.write(linea)
        archivo.close()
    except:
        print("No se pudo guardar la venta en el historial.")

# --- 2. FUNCIONES DEL SISTEMA ---

def agregar_nuevo():
    print("\n--- AGREGAR PRODUCTO ---")
    
    # Validamos el nombre (Bucle para que no lo dejen vacío)
    while True:
        # Quitamos las comas para que no se dañe el archivo CSV
        nombre = input("Nombre del producto (o 'F' para cancelar): ").strip().capitalize().replace(",", "")
        
        # Opción de escape
        if nombre.upper() == "F": 
            return

        if nombre == "":
            print("El dato que acabas de colocar no es válido. El nombre es obligatorio.")
            continue
        
        # Revisamos si ya existe para no tener duplicados
        existe = False
        for p in inventario:
            if p["nombre"] == nombre:
                print("El dato que acabas de colocar no es válido. Ese producto ya existe.")
                existe = True
                break
        
        if not existe:
            break 

    # Validación de Cantidad (Bucle de insistencia)
    while True:
        entrada = input("Cantidad inicial (o 'F' para cancelar): ")
        if entrada.upper() == "F": return 

        try:
            cant = int(entrada)
            if cant >= 0: break
            print("El dato que acabas de colocar no es válido. No use negativos.")
        except:
            print("Debes ingresar solo números enteros.")

    # Validación de Precio
    while True:
        entrada = input("Precio RD$ (o 'F' para cancelar): ")
        if entrada.upper() == "F": return 

        try:
            precio = float(entrada)
            if precio >= 0: break
            print("El dato que acabas de colocar no es válido. El precio debe ser positivo.")
        except:
            print("Debes ingresar solo números válidos.")
            
    # Si todo está bien, lo agregamos y guardamos
    inventario.append({"nombre": nombre, "cantidad": cant, "precio": precio})
    print(f"¡Listo! El producto '{nombre}' fue agregado correctamente.")
    guardar_cambios()

def actualizar_stock():
    print("\n--- ACTUALIZAR EXISTENCIAS ---")
    
    # Bucle para buscar (así no te saca si escribes mal el nombre)
    while True:
        busqueda = input("Nombre del producto (o 'F' para cancelar): ").strip().capitalize()
        if busqueda.upper() == "F": return

        producto_encontrado = None
        # Buscamos el producto en la lista
        for p in inventario:
            if p["nombre"] == busqueda:
                producto_encontrado = p
                break
        
        if producto_encontrado:
            print(f"Producto: {producto_encontrado['nombre']} | Cantidad: {producto_encontrado['cantidad']} | Precio: RD${producto_encontrado['precio']:.2f}")
            print("(Si no quieres cambiar el dato, solo dale a ENTER)")
            
            # Actualizar Cantidad
            entrada_cant = input("Nueva Cantidad (o 'F' para cancelar): ")
            if entrada_cant.upper() == "F": return 

            if entrada_cant != "":
                try: 
                    cantidad_temp = int(entrada_cant)
                    if cantidad_temp >= 0:
                        producto_encontrado["cantidad"] = cantidad_temp
                    else:
                        print("No se permiten negativos. Cantidad no actualizada.")
                except: 
                    print("Debes ingresar solo números. Cantidad no actualizada.")
            
            # Actualizar Precio
            entrada_precio = input("Nuevo Precio RD$ (o 'F' para cancelar): ")
            if entrada_precio.upper() == "F": return

            if entrada_precio != "":
                try: 
                    precio_temp = float(entrada_precio)
                    if precio_temp >= 0:
                        producto_encontrado["precio"] = precio_temp
                    else:
                        print("No se permiten negativos. Precio no actualizado.")
                except: 
                    print("Debes ingresar solo números. Precio no actualizado.")
            
            guardar_cambios()
            print("Datos actualizados correctamente.")
            return # Salimos al menú
        else:
            print("No encontramos ese producto. Intenta de nuevo.")

def eliminar_producto():
    print("\n--- ELIMINAR PRODUCTO ---")
    
    while True:
        nombre = input("Nombre a borrar (o 'F' para cancelar): ").strip().capitalize()
        if nombre.upper() == "F": return
        
        encontrado = False
        # Usamos una copia de la lista [:] para borrar de forma segura
        for i in range(len(inventario)):
            if inventario[i]["nombre"] == nombre:
                inventario.pop(i) # Lo sacamos de la lista
                print("Producto eliminado del sistema.")
                guardar_cambios()
                return 
        
        if not encontrado:
            print("No encontramos ese nombre. Intenta de nuevo.")

def ver_lista_productos():
    print("\n--- CONSULTAR INVENTARIO ---")
    if len(inventario) == 0:
        print("El inventario está vacío.")
        return
        
    print("1. Ver orden normal (como llegaron)")
    print("2. Ver ordenado alfabéticamente (A-Z)")
    opcion = input("Opción (o 'F' para cancelar): ")
    if opcion.upper() == "F": return
    
    # Creamos una lista temporal para no desordenar la original
    lista_temporal = list(inventario)
    
    if opcion == "2":
        # Usamos lambda para ordenar por el nombre
        lista_temporal.sort(key=lambda x: x["nombre"])
        
    print("-" * 50)
    print("PRODUCTO \t| CANT \t| PRECIO (RD$)")
    print("-" * 50)
    for p in lista_temporal:
        print(f"{p['nombre']} \t| {p['cantidad']} \t| RD${p['precio']:.2f}")

def reporte_bajo_stock():
    print("\n--- REPORTE STOCK BAJO ---")
    try:
        entrada = input("Avisame si hay menos de (o 'F' para cancelar): ")
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

def reporte_valor_inventario():
    print("\n--- VALOR TOTAL ---")
    total_dinero = 0
    mayor_stock = -1
    nombre_mayor = ""
    
    for p in inventario:
        total_dinero += p["cantidad"] * p["precio"]
        
        # Buscamos cuál es el producto que más hay
        if p["cantidad"] > mayor_stock:
            mayor_stock = p["cantidad"]
            nombre_mayor = p["nombre"]
            
    print(f"Total invertido en el negocio: RD${total_dinero:,.2f}") 
    if nombre_mayor != "":
        print(f"El producto con más stock es: {nombre_mayor}")

def facturar_caja():
    # Esta es nuestra función extra para simular una venta con ITBIS
    print("\n--- CAJA REGISTRADORA ---")
    
    # Bucle para no salir si se equivocan de nombre
    while True:
        busqueda = input("Producto a cobrar (o 'F' para cancelar): ").strip().capitalize()
        if busqueda.upper() == "F": return
        
        producto_encontrado = None
        for p in inventario:
            if p["nombre"] == busqueda:
                producto_encontrado = p
                break
        
        if producto_encontrado:
            # Si lo encontramos, procedemos a la venta
            print(f"Disponible: {producto_encontrado['cantidad']} | Precio: RD${producto_encontrado['precio']:.2f}")
            
            while True:
                entrada = input("¿Cuántos lleva? (o 'F' para cancelar): ")
                if entrada.upper() == "F": return
                
                try:
                    cantidad_llevar = int(entrada)
                    
                    if cantidad_llevar <= 0:
                        print("El dato que acabas de colocar no es válido (debe ser mayor a 0).")
                    elif cantidad_llevar > producto_encontrado["cantidad"]:
                        print(f"El dato que acabas de colocar no es válido. Solo quedan {producto_encontrado['cantidad']}.")
                    else:
                        # Hacemos los cálculos del dinero
                        subtotal = cantidad_llevar * producto_encontrado["precio"]
                        itbis = subtotal * 0.18 # ITBIS de ley (18%)
                        total_pagar = subtotal + itbis
                        
                        # Restamos del inventario
                        producto_encontrado["cantidad"] = producto_encontrado["cantidad"] - cantidad_llevar
                        
                        # Imprimimos el recibo para el cliente
                        print("\n" + "="*35)
                        print("      LA FRUTA MARKET - RECIBO      ")
                        print("="*35)
                        print(f"Producto:   {producto_encontrado['nombre']}")
                        print(f"Cantidad:   {cantidad_llevar}")
                        print(f"Subtotal:   RD${subtotal:.2f}")
                        print(f"ITBIS (18%): RD${itbis:.2f}")
                        print("-" * 35)
                        print(f"TOTAL:      RD${total_pagar:.2f}")
                        print("="*35)
                        print("      Gracias por su compra       ")
                        
                        # Guardamos los cambios y registramos en el historial
                        guardar_cambios()
                        registrar_historial(producto_encontrado['nombre'], cantidad_llevar, total_pagar)
                        
                        # Pausa para ver el ticket
                        input("\nPresione Enter para continuar...")
                        return 
                except:
                    print("Debes ingresar solo números.")
        else:
            print("No encontramos ese producto. Intenta de nuevo.")

# --- MENU PRINCIPAL ---
def menu_principal():
    cargar_inicio() # Cargamos los datos al arrancar
    
    while True:
        print("\n" + "="*40)
        print("      SISTEMA DE INVENTARIO (RD)")
        print("          LA FRUTA MARKET")
        print("="*40)
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
        
        if op == "1": agregar_nuevo()
        elif op == "2": actualizar_stock()
        elif op == "3": eliminar_producto()
        elif op == "4": ver_lista_productos()
        elif op == "5": reporte_bajo_stock()
        elif op == "6": reporte_valor_inventario()
        elif op == "7": facturar_caja()
        elif op == "8": 
            print("Cerrando sistema... ¡Nos vemos!")
            break
        else:
            print("El dato que acabas de colocar no es válido, intenta de nuevo.")

# --- INICIO ---
if __name__ == "__main__":
    menu_principal()
