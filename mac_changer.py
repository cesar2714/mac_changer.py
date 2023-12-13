import subprocess
import optparse
import re

#subprocess: Se utiliza para ejecutar comandos del sistema operativo desde el script.
#optparse: Se utiliza para analizar opciones de línea de comandos.
#re: Módulo de expresiones regulares.

def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Interface para cambiar la direccion MAC")
    parser.add_option("-m", "--mac", dest="new_mac", help="Nueva Direccion MAC")
    (options, arguments) = parser.parse_args()
    if not options.interface:
        parser.error('[-] Por favor indica la interfaz de red y su nueva direccion MAC, ambos parametros a la vez. Use -h para ayuda.')
    elif not options.new_mac:
        parser.error('[-] Por favor indica ambos parametros a la vez. Ejp: -i eth0 -m <la MAC de tu eleccion>. Use -h para ayuda.')    
    return options

#Define una función que utiliza optparse para analizar las opciones de línea de comandos. 
#Las opciones incluyen la interfaz (-i o --interface) y la nueva dirección MAC (-m o --mac).
#Devuelve un objeto que contiene las opciones analizadas.

def change_mac(interface, new_mac):
    print("[+] Cambiando Direccion MAC para " + interface + " a " + new_mac)
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])

#Esta función cambia la dirección MAC de la interfaz especificada.
#Utiliza la biblioteca subprocess para ejecutar comandos del sistema operativo, deshabilita la interfaz, >>>
#>>> cambia la dirección MAC y vuelve a habilitar la interfaz.

def get_current_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface])
    ifconfig_result_str = ifconfig_result.decode('utf-8')  # Convertir bytes a cadena de texto

    mac_address_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result_str)

    if mac_address_search_result:
        return mac_address_search_result.group(0)
    else:
        print("[-] No se pudo leer la direccion MAC")


#Esta función obtiene la dirección MAC actual de la interfaz especificada.
#Utiliza subprocess para ejecutar el comando ifconfig y luego usa expresiones regulares para extraer >>>
#>>> la dirección MAC del resultado.

options = get_arguments()

current_mac = get_current_mac(options.interface)
print("Current MAC = " + str(current_mac))

change_mac(options.interface, options.new_mac)

current_mac = get_current_mac(options.interface)
if current_mac == options.new_mac:
    print("[+] Direccion MAC ha sido cambiada de forma exitosa a " + current_mac)
else:
    print("[-] Ha ocurrido un problema al intentar cambiar su direccion MAC. Verifique sus pasos e intente de nuevo")

#Obtiene las opciones de línea de comandos.

#Obtiene la dirección MAC actual y la muestra.

#Cambia la dirección MAC usando la función change_mac.

#Obtiene la nueva dirección MAC y la compara con la especificada para verificar si el cambio fue exitoso.