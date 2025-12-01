import os # Necesario para imprimir y limpiar pantalla

# --- CLASE DE COLORES ---
class Color:
    RESET = "\033[0m"
    ROJO = "\033[91m"
    VERDE = "\033[92m"
    AMARILLO = "\033[93m"
    AZUL = "\033[96m" 
    NEGRITA = "\033[1m"

# 1. Lista principal (Global)
inventario = []

def mostrar_menu():
    print(f"\n{Color.AZUL}========================================{Color.RESET}")
    print(f"{Color.NEGRITA}      GESTION DE INVENTARIO TIENDA      {Color.RESET}")
    print(f"{Color.AZUL}========================================{Color.RESET}")
    print("1. Agregar un producto nuevo")
    print("2. Actualizar existencias")
    print("3. Consultar producto")
    print("4. Eliminar producto")
    print("5. Imprimir Reportes (Pantalla)")
    print(f"6. Guardar en Archivo {Color.AMARILLO}(Backup){Color.RESET}")
    print(f"7. {Color.NEGRITA}Mandar a Impresora (Físico){Color.RESET}") # <--- NUEVO
    print(f"8. Ver Inventario Ordenado {Color.AMARILLO}(Opcional){Color.RESET}")
    print(f"9. {Color.ROJO}Salir{Color.RESET}")
    print(f"{Color.AZUL}========================================{Color.RESET}")

# --- FUNCION AUXILIAR PARA ORDENAR ---
def obtener_cantidad(producto):
    return producto["cantidad"]

def ver_inventario_ordenado():
    print(f"\n{Color.AZUL}--- INVENTARIO ORDENADO (MAYOR A MENOR) ---{Color.RESET}")
    if not inventario:
        print(f"{Color.AMARILLO}Inventario vacio.{Color.RESET}")
        return

    lista_ordenada = sorted(inventario, key=obtener_cantidad, reverse=True)

    for p in lista_ordenada:
        print(f"Nombre: {Color.NEGRITA}{p['nombre']}{Color.RESET} | Stock: {p['cantidad']} | Precio: ${p['precio']}")

def agregar_producto():
    print(f"\n{Color.AZUL}--- AGREGAR PRODUCTO ---{Color.RESET}")
    nombre = input("Ingresa el nombre del producto: ")
    
    if nombre == "":
        print(f"{Color.ROJO}ERROR: El nombre no puede estar vacio.{Color.RESET}")
        return 

    for producto in inventario:
        if producto["nombre"] == nombre:
            print(f"{Color.ROJO}ERROR: Ese producto ya existe. Usa la opcion 2.{Color.RESET}")
            return

    try:
        precio = float(input("Ingresa el precio del producto: "))
        if precio < 0:
            print(f"{Color.ROJO}ERROR: El precio no puede ser negativo.{Color.RESET}")
            return
    except ValueError:
        print(f"{Color.ROJO}ERROR: Debes escribir un numero valido.{Color.RESET}")
        return

    try:
        cantidad = int(input("Ingresa la cantidad inicial: "))
        if cantidad < 0:
            print(f"{Color.ROJO}ERROR: La cantidad no puede ser negativa.{Color.RESET}")
            return
    except ValueError:
        print(f"{Color.ROJO}ERROR: La cantidad debe ser un numero entero.{Color.RESET}")
        return

    nuevo_producto = {
        "nombre": nombre,
        "precio": precio,
        "cantidad": cantidad
    }
    
    inventario.append(nuevo_producto)
    print(f"{Color.VERDE}¡Producto '{nombre}' agregado exitosamente!{Color.RESET}")

def actualizar_cantidad():
    print(f"\n{Color.AZUL}--- ACTUALIZAR CANTIDAD ---{Color.RESET}")
    nombre_buscar = input("Nombre del producto a actualizar: ")
    
    encontrado = False
    for prod in inventario:
        if prod["nombre"] == nombre_buscar:
            encontrado = True
            print(f"Producto encontrado. Cantidad actual: {prod['cantidad']}")
            try:
                nueva_cant = int(input("Ingresa la NUEVA cantidad total: "))
                if nueva_cant >= 0:
                    prod["cantidad"] = nueva_cant
                    print(f"{Color.VERDE}¡Cantidad actualizada correctamente!{Color.RESET}")
                else:
                    print(f"{Color.ROJO}ERROR: No puedes poner cantidad negativa.{Color.RESET}")
            except ValueError:
                print(f"{Color.ROJO}ERROR: Ingresa un numero entero.{Color.RESET}")
            break 
            
    if encontrado == False:
        print(f"{Color.AMARILLO}No se encontro ese producto.{Color.RESET}")

def consultar_producto():
    print(f"\n{Color.AZUL}--- CONSULTAR PRODUCTO ---{Color.RESET}")
    nombre_buscar = input("Nombre del producto a buscar: ")
    
    encontrado = False
    for prod in inventario:
        if prod["nombre"] == nombre_buscar:
            print("-------------------------")
            print(f"Nombre: {Color.NEGRITA}{prod['nombre']}{Color.RESET}")
            print(f"Precio: ${prod['precio']}")
            print(f"Cantidad: {prod['cantidad']}")
            print("-------------------------")
            encontrado = True
            break
            
    if encontrado == False:
        print(f"{Color.AMARILLO}Producto no encontrado.{Color.RESET}")

def eliminar_producto():
    print(f"\n{Color.AZUL}--- ELIMINAR PRODUCTO ---{Color.RESET}")
    nombre_borrar = input("Nombre del producto a eliminar: ")
    
    indice_a_borrar = -1
    for i in range(len(inventario)):
        if inventario[i]["nombre"] == nombre_borrar:
            indice_a_borrar = i
            break
            
    if indice_a_borrar != -1:
        inventario.pop(indice_a_borrar)
        print(f"{Color.VERDE}El producto '{nombre_borrar}' fue eliminado.{Color.RESET}")
    else:
        print(f"{Color.AMARILLO}No se encontro el producto.{Color.RESET}")

def imprimir_reportes():
    print(f"\n{Color.AZUL}--- REPORTES EN PANTALLA ---{Color.RESET}")
    if len(inventario) == 0:
        print(f"{Color.AMARILLO}No hay productos registrados.{Color.RESET}")
        return

    print("1) Productos con STOCK BAJO (menos de 5):")
    hay_bajos = False
    for prod in inventario:
        if prod["cantidad"] < 5:
            print(f" - {Color.ROJO}ALERTA:{Color.RESET} {prod['nombre']} (Quedan: {prod['cantidad']})")
            hay_bajos = True
    if hay_bajos == False:
        print(f" - {Color.VERDE}No hay productos con stock bajo.{Color.RESET}")

    print("\n2) Producto con MAYOR cantidad:")
    prod_mayor = inventario[0]
    for prod in inventario:
        if prod["cantidad"] > prod_mayor["cantidad"]:
            prod_mayor = prod
    print(f" - El mayor es: {Color.NEGRITA}{prod_mayor['nombre']}{Color.RESET} ({prod_mayor['cantidad']} u.)")

    print("\n3) Valor TOTAL del inventario:")
    suma_total = 0
    for prod in inventario:
        total_prod = prod["precio"] * prod["cantidad"]
        suma_total = suma_total + total_prod
    print(f" - Valor total estimado: ${suma_total}")

def guardar_inventario():
    print(f"\n{Color.AZUL}--- GUARDANDO ARCHIVO DE TEXTO ---{Color.RESET}")
    if not inventario:
        print(f"{Color.AMARILLO}Inventario vacio, nada que guardar.{Color.RESET}")
        return False # Retornamos False si falló
    
    try:
        nombre_archivo = "inventario.txt"
        archivo = open(nombre_archivo, "w")
        archivo.write("REPORTE DE INVENTARIO\n")
        archivo.write("=====================\n")
        
        for p in inventario:
            linea = f"Producto: {p['nombre']} | Precio: {p['precio']} | Stock: {p['cantidad']}\n"
            archivo.write(linea)
            
        archivo.close()
        print(f"{Color.VERDE}¡Exito! La informacion se guardo en '{nombre_archivo}'.{Color.RESET}")
        return True # Retornamos True si funcionó
    except:
        print(f"{Color.ROJO}Ocurrio un error al intentar crear el archivo.{Color.RESET}")
        return False

# --- NUEVA FUNCION: IMPRESION FISICA ---
def imprimir_fisico():
    print(f"\n{Color.AZUL}--- ENVIANDO A IMPRESORA ---{Color.RESET}")
    
    # 1. Primero guardamos el archivo para tener qué imprimir
    se_guardo = guardar_inventario()
    
    if se_guardo == True:
        print("Intentando abrir herramienta de impresión...")
        try:
            # Truco de Novato: Usamos os.startfile con la opcion "print"
            # Esto le dice a Windows: "Imprime este archivo de texto"
            os.startfile("inventario.txt", "print")
            print(f"{Color.VERDE}¡Comando enviado! Revisa tu impresora.{Color.RESET}")
        except:
            print(f"{Color.ROJO}ERROR: Esta funcion solo es compatible con Windows.{Color.RESET}")
            print("En otros sistemas, abre 'inventario.txt' e imprime manualmente.")

# --- BLOQUE PRINCIPAL (MAIN) ---

# 1. LOGIN DE SEGURIDAD
print(f"\n{Color.VERDE}*{Color.RESET}")
print(f"{Color.VERDE}* SISTEMA DE INVENTARIO SEGURO *{Color.RESET}")
print(f"{Color.VERDE}*{Color.RESET}")

intentos = 0
acceso_concedido = False

while intentos < 3:
    usuario = input("Usuario: ")
    clave = input("Contraseña: ")
    
    if usuario == "admin" and clave == "1234":
        print(f"\n{Color.VERDE}>>> ACCESO CONCEDIDO. ¡Bienvenido!{Color.RESET}")
        acceso_concedido = True
        break
    else:
        intentos = intentos + 1
        print(f"{Color.ROJO}Datos incorrectos. Intento {intentos} de 3.{Color.RESET}")

if acceso_concedido == False:
    print(f"\n{Color.ROJO}>>> ERROR: Demasiados intentos fallidos. Sistema bloqueado.{Color.RESET}")
    exit()

# 2. MENU PRINCIPAL
continuar = True
while continuar:
    mostrar_menu()
    opcion = input("Elige una opcion (1-9): ")
    
    if opcion == "1":
        agregar_producto()
    elif opcion == "2":
        actualizar_cantidad()
    elif opcion == "3":
        consultar_producto()
    elif opcion == "4":
        eliminar_producto()
    elif opcion == "5":
        imprimir_reportes()
    elif opcion == "6":
        guardar_inventario()
    elif opcion == "7": # <--- NUEVA OPCION
        imprimir_fisico()
    elif opcion == "8":
        ver_inventario_ordenado()
    elif opcion == "9":
        print(f"{Color.AZUL}Saliendo... ¡Adios!{Color.RESET}")
        continuar = False
    else:
        print(f"{Color.ROJO}Opcion no valida.{Color.RESET}")
