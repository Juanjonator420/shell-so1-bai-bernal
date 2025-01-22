#!/usr/bin/env python
"""A simple cmd2 application."""
import cmd2
import argparse
import os
import shutil
import pwd
import grp
import subprocess
import json
from DemonioManager import DemonioManager #Importa DemonioManager

HORARIOS_LOG = 'usuario_horarios_log' # Archivo de logs de horarios
TRANSFERENCIAS_LOG = 'Shell_transferencias' # Archivo de log de transferencias
USERS_FILE = 'usuarios.json' # Archivo para almacenar la información de los usuarios

class FirstApp(cmd2.Cmd):
    """A simple cmd2 application."""

    def __init__(self):
        super().__init__()
        self.current_directory = os.getcwd()  # Ruta actual al iniciar la shell
        self.demonio_manager = DemonioManager()
        self.HORARIOS_LOG = 'usuario_horarios_log'

        # Make maxrepeats settable at runtime
        self.maxrepeats = 3
        self.add_settable(cmd2.Settable('maxrepeats', int, 'max repetitions for speak command', self))

    # Comandos básicos de prueba:
    #--------------------------------------------------------------------------------------------------------------------
    speak_parser = cmd2.Cmd2ArgumentParser()
    speak_parser.add_argument('-p', '--piglatin', action='store_true', help='atinLay')
    speak_parser.add_argument('-s', '--shout', action='store_true', help='N00B EMULATION MODE')
    speak_parser.add_argument('-r', '--repeat', type=int, help='output [n] times')
    speak_parser.add_argument('words', nargs='+', help='words to say')

    @cmd2.with_argparser(speak_parser)
    def do_speak(self, args): #comando de prueba: speak
        """Repeats what you tell me to."""
        words = []
        for word in args.words:
            if args.piglatin:
                word = '%s%say' % (word[1:], word[0])
            if args.shout:
                word = word.upper()
            words.append(word)
        repetitions = args.repeat or 1
        for _ in range(min(repetitions, self.maxrepeats)):
            # .poutput handles newlines, and accommodates output redirection too
            self.poutput(' '.join(words))

    # Comandos solicitados segun la descripcion de la shell:
    #-------------------------------------------------------------------------------------------------------------------

    # Comando para crear archivos - extra
    create_file_parser = cmd2.Cmd2ArgumentParser()
    create_file_parser.add_argument('filename', help='Nombre del archivo a crear')

    @cmd2.with_argparser(create_file_parser)
    def do_creararchivo(self, args): #comando: creararchivo
        """Crea un archivo vacío."""
        try:
            with open(args.filename, 'w') as f:
                pass  # Crea un archivo vacío
            self.poutput(f"Archivo {args.filename} creado.")
        except Exception as e:
            self.perror(f"Error al crear el archivo: {e}")

    # Comando para crear directorios - 5 solicitado
    create_dir_parser = cmd2.Cmd2ArgumentParser()
    create_dir_parser.add_argument('dirname', help='Nombre del directorio a crear')

    @cmd2.with_argparser(create_dir_parser)
    def do_creardir(self, args): #comando: creardir
        """Crea un directorio."""
        try:
            os.makedirs(args.dirname, exist_ok=True)
            self.poutput(f"Directorio {args.dirname} creado.")
        except Exception as e:
            self.perror(f"Error al crear el directorio: {e}")

    # Comando para copiar archivos - 1 solicitado
    copy_parser = cmd2.Cmd2ArgumentParser()
    copy_parser.add_argument('source', help='Archivo o directorio de origen')
    copy_parser.add_argument('destination', help='Archivo o directorio de destino')

    @cmd2.with_argparser(copy_parser)
    def do_copiar(self, args): # comando: copiar
        """Copia un archivo o directorio al destino especificado."""
        source_path = os.path.abspath(os.path.join(self.current_directory, args.source))
        destination_path = os.path.abspath(os.path.join(self.current_directory, args.destination))

        try:
            if os.path.exists(source_path):
                shutil.copy(source_path, destination_path)
                self.poutput(f"Copiado {source_path} a {destination_path}.")
            else:
                self.perror(f"El archivo o directorio {args.source} no existe.")
        except Exception as e:
            self.perror(f"Error al copiar: {e}")


    # Comando para mover archivos - 2 solicitado
    move_parser = cmd2.Cmd2ArgumentParser()
    move_parser.add_argument('source', help='Archivo o directorio de origen')
    move_parser.add_argument('destination', help='Archivo o directorio de destino')

    @cmd2.with_argparser(move_parser)
    def do_mover(self, args): # comando: mover
        """Mueve un archivo o directorio al destino especificado."""
        source_path = os.path.abspath(os.path.join(self.current_directory, args.source))
        destination_path = os.path.abspath(os.path.join(self.current_directory, args.destination))

        try:
            if os.path.exists(source_path):
                shutil.move(source_path, destination_path)
                self.poutput(f"Movido {source_path} a {destination_path}.")
            else:
                self.perror(f"El archivo o directorio {args.source} no existe.")
        except Exception as e:
            self.perror(f"Error al mover: {e}")


    # Comando para renombrar archivos - 3 solicitado
    rename_parser = cmd2.Cmd2ArgumentParser()
    rename_parser.add_argument('source', help='Archivo o directorio actual')
    rename_parser.add_argument('new_name', help='Nuevo nombre del archivo o directorio')

    @cmd2.with_argparser(rename_parser)
    def do_renombrar(self, args): # comando: renombrar
        """Renombra un archivo o directorio."""
        source_path = os.path.abspath(os.path.join(self.current_directory, args.source))
        new_name_path = os.path.abspath(os.path.join(self.current_directory, args.new_name))

        try:
            if os.path.exists(source_path):
                os.rename(source_path, new_name_path)
                self.poutput(f"Renombrado {source_path} a {new_name_path}.")
            else:
                self.perror(f"El archivo o directorio {args.source} no existe.")
        except Exception as e:
            self.perror(f"Error al renombrar: {e}")


    #---------------------------------------------------------------------------------------------------------------
    # Comando para listar directorios - 4 solicitado
    list_parser = cmd2.Cmd2ArgumentParser()
    list_parser.add_argument('directory', nargs='?', default='', help='Directorio a listar (por defecto: actual)')

    @cmd2.with_argparser(list_parser)
    def do_listar(self, args): # comando: listar
        """Lista el contenido de un directorio."""
        directory_to_list = os.path.abspath(os.path.join(self.current_directory, args.directory))
        try:
            entries = os.listdir(directory_to_list)
            for entry in entries:
                self.poutput(entry)
        except Exception as e:
            self.perror(f"Error al listar el directorio: {e}")

    # Comando para cambiar de directorio - 6 solicitado
    change_dir_parser = cmd2.Cmd2ArgumentParser()
    change_dir_parser.add_argument('directory', help='Ruta del directorio al que desea cambiar')

    @cmd2.with_argparser(change_dir_parser)
    def do_ir(self, args): # comando: ir
        """Cambia al directorio especificado."""
        new_directory = os.path.abspath(os.path.join(self.current_directory, args.directory))
        if os.path.isdir(new_directory):  # Verifica si el directorio existe
            self.current_directory = new_directory  # Actualiza la ruta actual
            self.poutput(f"Directorio cambiado a: {self.current_directory}")
        else:
            self.perror(f"El directorio {args.directory} no existe.")
    # comando: ir . para volver al directorio actual y ir.. para volver a la ruta padre


    #---------------------------------------------------------------------------------------------------------------
    # Comando para cambiar permisos de archivos - 7 solicitado
    permissions_parser = cmd2.Cmd2ArgumentParser()
    permissions_parser.add_argument('mode', help='Permisos en formato octal (e.g., 755)')
    permissions_parser.add_argument('files', nargs='+', help='Archivos o directorios a los que cambiar los permisos')

    @cmd2.with_argparser(permissions_parser)
    def do_permisos(self, args):  # comando: permisos
        """Cambia los permisos de un archivo o conjunto de archivos."""
        try:
            mode = int(args.mode, 8)  # Convierte los permisos octales a entero
            for file in args.files:
                file_path = os.path.abspath(os.path.join(self.current_directory, file))
                if os.path.exists(file_path):
                    os.chmod(file_path, mode)
                    self.poutput(f"Permisos de {file_path} cambiados a {args.mode}.")
                else:
                    self.perror(f"El archivo o directorio {file} no existe.")
        except ValueError:
            self.perror("El modo de permisos debe estar en formato octal (por ejemplo: 755).")
        except Exception as e:
            self.perror(f"Error al cambiar permisos: {e}")


    #---------------------------------------------------------------------------------------------------------------
    # Comando para cambiar propietario y grupo de archivos - 8 solicitado
    owner_parser = cmd2.Cmd2ArgumentParser()
    owner_parser.add_argument('owner', help='Nuevo propietario (nombre de usuario o UID)')
    owner_parser.add_argument('group', help='Nuevo grupo (nombre del grupo o GID)')
    owner_parser.add_argument('files', nargs='+', help='Archivos o directorios a los que cambiar el propietario')

    @cmd2.with_argparser(owner_parser)
    def do_propietario(self, args):  # comando: propietario
        """Cambia el propietario y grupo de un archivo o conjunto de archivos."""
        try:
            # Obtiene UID y GID
            uid = int(args.owner) if args.owner.isdigit() else pwd.getpwnam(args.owner).pw_uid
            gid = int(args.group) if args.group.isdigit() else grp.getgrnam(args.group).gr_gid

            for file in args.files:
                file_path = os.path.abspath(os.path.join(self.current_directory, file))
                if os.path.exists(file_path):
                    os.chown(file_path, uid, gid)
                    self.poutput(f"Propietario y grupo de {file_path} cambiados a {args.owner}:{args.group}.")
                else:
                    self.perror(f"El archivo o directorio {file} no existe.")
        except KeyError:
            self.perror("El propietario o grupo no existen.")
        except Exception as e:
            self.perror(f"Error al cambiar propietario: {e}")


    #---------------------------------------------------------------------------------------------------------------
    # Comando para cambiar la contraseña de un usuario - 9 solicitado
    password_parser = cmd2.Cmd2ArgumentParser()
    password_parser.add_argument('username', help='Nombre de usuario para cambiar la contraseña')

    @cmd2.with_argparser(password_parser)
    def do_contraseña(self, args):  # comando: contraseña
        """Cambia la contraseña de un usuario."""
        try:
            # Llama al comando del sistema para cambiar la contraseña
            result = subprocess.run(['passwd', args.username], check=True)
            if result.returncode == 0:
                self.poutput(f"Contraseña para {args.username} cambiada correctamente.")
            else:
                self.perror(f"Error al cambiar la contraseña de {args.username}.")
        except subprocess.CalledProcessError as e:
            self.perror(f"Error al ejecutar el comando: {e}")
        except Exception as e:
            self.perror(f"Error inesperado: {e}")


    #---------------------------------------------------------------------------------------------------------------
    # Comando para agregar usuarios - 10 solicitado
    user_parser = cmd2.Cmd2ArgumentParser()
    user_parser.add_argument('username', help='Nombre del nuevo usuario')
    user_parser.add_argument('-n', '--nombre', required=True, help='Nombre completo del usuario')
    user_parser.add_argument('-H', '--horario', required=True, help='Horario de trabajo del usuario')  # Cambiado -h a -H
    user_parser.add_argument('-l', '--lugares', nargs='+', default=['localhost'], help='Posibles lugares de conexión (IPs o localhost)')

    @cmd2.with_argparser(user_parser)
    def do_usuario(self, args):  # comando: usuario
        """Agrega un nuevo usuario y registra sus datos personales."""
        try:
            subprocess.run(['useradd', args.username], check=True)

            user_data = {
                'username': args.username,
                'nombre': args.nombre,
                'horario': args.horario,
                'lugares': args.lugares
            }

            if os.path.exists(USERS_FILE):
                with open(USERS_FILE, 'r') as f:
                    users = json.load(f)
            else:
                users = {}

            users[args.username] = user_data

            with open(USERS_FILE, 'w') as f:
                json.dump(users, f, indent=4)

            self.poutput(f"Usuario {args.username} agregado correctamente.")
        except subprocess.CalledProcessError as e:
            self.perror(f"Error al agregar el usuario {args.username}: {e}")
        except Exception as e:
            self.perror(f"Error inesperado: {e}")


    #--------------------------------------------------------------------------------------------------------------- volver a revisar

    # Comando para listar demonios - 11 solicitado
    @cmd2.with_argument_list
    def do_listardemonios(self, args):
        """Lista los demonios disponibles en el sistema."""
        demonios = self.demonio_manager.listar_demonios()
        if demonios:
            self.poutput("\n".join(demonios))
        else:
            self.poutput("No se encontraron demonios disponibles.")

    # Comando para manejar demonios
    daemon_parser = cmd2.Cmd2ArgumentParser()
    daemon_parser.add_argument('action', choices=['start', 'stop', 'restart'], help='Acción para el demonio')
    daemon_parser.add_argument('daemon', help='Nombre del demonio (sin .service)')

    @cmd2.with_argparser(daemon_parser)
    def do_demonio(self, args):
        """Levanta, detiene o reinicia un demonio."""
        try:
            mensaje = self.demonio_manager.ejecutar_accion(args.daemon, args.action)
            self.poutput(mensaje)
        except FileNotFoundError as e:
            self.perror(str(e))
        except ValueError as e:
            self.perror(str(e))
        except subprocess.CalledProcessError as e:
            self.perror(f"Error al ejecutar la acción: {e}")
        except Exception as e:
            self.perror(f"Error inesperado: {e}")


    #--------------------------------------------------------------------------------------------------------------- 


    # Comando para ejecutar comandos arbitrarios del sistema - 12 solicitado
    system_command_parser = cmd2.Cmd2ArgumentParser()
    system_command_parser.add_argument('command', help='Comando del sistema a ejecutar')
    system_command_parser.add_argument('args', nargs=argparse.REMAINDER, help='Argumentos del comando del sistema')

    @cmd2.with_argparser(system_command_parser)
    def do_ejecutar(self, args):  # comando: ejecutar
        """Ejecuta comandos arbitrarios del sistema."""
        try:
            # Verifica que el comando no esté entre los comandos prohibidos
            forbidden_commands = ['ir', 'usuario', 'contraseña', 'demonio']
            if args.command in forbidden_commands:
                self.perror(f"El comando {args.command} está prohibido.")
                return

            # Ejecuta el comando
            result = subprocess.run([args.command] + args.args, text=True, capture_output=True)
            if result.returncode == 0:
                self.poutput(result.stdout)
            else:
                self.perror(result.stderr)
        except Exception as e:
            self.perror(f"Error al ejecutar el comando: {e}")


    #--------------------------------------------------------------------------------------------------------------- 

    #Registrar el inicio de sesión y la salida sesión del usuario. - 13 solicitado
    # Define el parser para el comando sesion
    sesion_parser = cmd2.Cmd2ArgumentParser()
    sesion_parser.add_argument('accion', choices=['iniciar', 'cerrar'], help='Acción de la sesión (iniciar o cerrar)')

    def registrar_horario(self, usuario, accion, horario_permitido):
        """Registra el horario de inicio o salida en un archivo de log."""
        from datetime import datetime
        ahora = datetime.now()
        hora_actual = ahora.strftime("%H:%M:%S")
        fecha_actual = ahora.strftime("%Y-%m-%d")
        fuera_de_rango = not (horario_permitido[0] <= hora_actual <= horario_permitido[1])

        mensaje = f"{fecha_actual} {hora_actual} - Usuario: {usuario} - Acción: {accion}"
        if fuera_de_rango:
            mensaje += " - Fuera de rango"
        
        with open(HORARIOS_LOG, 'a') as log:
            log.write(mensaje + '\n')

        return mensaje

    @cmd2.with_argparser(sesion_parser)
    def do_sesion(self, args):  # comando: sesion
        """Inicia o cierra sesión de un usuario."""
        usuario = "actual"  # Aquí puedes obtener el usuario del sistema
        accion = args.accion.lower()
        horario_permitido = ("08:00:00", "18:00:00")  # Horario permitido

        mensaje = self.registrar_horario(usuario, accion, horario_permitido)
        self.poutput(mensaje)


    #--------------------------------------------------------------------------------------------------------------- 

    #Ejecutar una transferencia por ftp o scp. - 14 solicitado
    transfer_parser = cmd2.Cmd2ArgumentParser()
    transfer_parser.add_argument('method', choices=['ftp', 'scp'], help='Método de transferencia (ftp o scp)')
    transfer_parser.add_argument('source', help='Archivo fuente')
    transfer_parser.add_argument('destination', help='Destino del archivo')

    @cmd2.with_argparser(transfer_parser)
    def do_transferir(self, args):  # comando: transferir
        """Ejecuta una transferencia por FTP o SCP y la registra."""
        try:
            if args.method == 'ftp':
                # Código para FTP
                self.poutput(f"Transfiriendo {args.source} a {args.destination} vía FTP...")
                # Aquí agregarías la lógica para transferir por FTP usando ftplib
            elif args.method == 'scp':
                # Código para SCP
                self.poutput(f"Transfiriendo {args.source} a {args.destination} vía SCP...")
                subprocess.run(['scp', args.source, args.destination], check=True)

            # Registrar la transferencia
            with open(TRANSFERENCIAS_LOG, 'a') as log:
                log.write(f"Transferencia {args.method.upper()}: {args.source} -> {args.destination}\n")

            self.poutput("Transferencia completada y registrada.")
        except Exception as e:
            self.perror(f"Error en la transferencia: {e}")


if __name__ == '__main__':
    import sys
    c = FirstApp()
    sys.exit(c.cmdloop())
