#!/usr/bin/env python
"""A simple cmd2 application."""
import cmd2
import argparse
import os
import shutil

class FirstApp(cmd2.Cmd):
    """A simple cmd2 application."""

    def __init__(self):
        super().__init__()

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

    # Comando para crear archivos
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

    # Comando para crear directorios
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

    # Comando para copiar archivos
    copy_parser = cmd2.Cmd2ArgumentParser()
    copy_parser.add_argument('source', help='Archivo o directorio de origen')
    copy_parser.add_argument('destination', help='Archivo o directorio de destino')

    @cmd2.with_argparser(copy_parser)
    def do_copiar(self, args): #comando: copiar
        """Copia un archivo o directorio al destino especificado."""
        try:
            shutil.copy(args.source, args.destination)
            self.poutput(f"Copiado {args.source} a {args.destination}.")
        except Exception as e:
            self.perror(f"Error al copiar: {e}")

    # Comando para mover archivos
    move_parser = cmd2.Cmd2ArgumentParser()
    move_parser.add_argument('source', help='Archivo o directorio de origen')
    move_parser.add_argument('destination', help='Archivo o directorio de destino')

    @cmd2.with_argparser(move_parser)
    def do_mover(self, args): #comando: mover
        """Mueve un archivo o directorio al destino especificado."""
        try:
            shutil.move(args.source, args.destination)
            self.poutput(f"Movido {args.source} a {args.destination}.")
        except Exception as e:
            self.perror(f"Error al mover: {e}")

    # Comando para renombrar archivos
    rename_parser = cmd2.Cmd2ArgumentParser()
    rename_parser.add_argument('source', help='Archivo o directorio actual')
    rename_parser.add_argument('new_name', help='Nuevo nombre del archivo o directorio')

    @cmd2.with_argparser(rename_parser)
    def do_renombrar(self, args): #comando: renombrar
        """Renombra un archivo o directorio."""
        try:
            os.rename(args.source, args.new_name)
            self.poutput(f"Renombrado {args.source} a {args.new_name}.")
        except Exception as e:
            self.perror(f"Error al renombrar: {e}")

    # Comando para listar directorios
    list_parser = cmd2.Cmd2ArgumentParser()
    list_parser.add_argument('directory', nargs='?', default='.', help='Directorio a listar (por defecto: actual)')

    @cmd2.with_argparser(list_parser)
    def do_listar(self, args): #comando: listar
        """Lista el contenido de un directorio."""
        try:
            entries = os.listdir(args.directory)
            for entry in entries:
                self.poutput(entry)
        except Exception as e:
            self.perror(f"Error al listar el directorio: {e}")


if __name__ == '__main__':
    import sys
    c = FirstApp()
    sys.exit(c.cmdloop())
