import os
import subprocess

class DemonioManager:
    """Clase para gestionar demonios sin usar systemctl ni service."""
    
    def __init__(self, service_directory="/usr/lib/systemd/system/"):
        self.service_directory = service_directory

    def listar_demonios(self):
        """Lista los archivos .service disponibles en el directorio de servicios."""
        try:
            return [f for f in os.listdir(self.service_directory) if f.endswith('.service')]
        except FileNotFoundError:
            return []

    def leer_demonio(self, nombre_demonio):
        """Lee el archivo .service del demonio especificado y devuelve sus configuraciones."""
        service_file = os.path.join(self.service_directory, f"{nombre_demonio}.service")
        if not os.path.exists(service_file):
            raise FileNotFoundError(f"El demonio {nombre_demonio} no existe en {self.service_directory}")
        
        config = {'ExecStart': None, 'ExecStop': None, 'ExecReload': None}
        with open(service_file, 'r') as f:
            for line in f:
                if line.startswith('ExecStart='):
                    config['ExecStart'] = line.split('=', 1)[1].strip()
                elif line.startswith('ExecStop='):
                    config['ExecStop'] = line.split('=', 1)[1].strip()
                elif line.startswith('ExecReload='):
                    config['ExecReload'] = line.split('=', 1)[1].strip()
        return config

    def ejecutar_accion(self, nombre_demonio, accion):
        """Ejecuta la acción (start, stop, restart) para el demonio especificado."""
        config = self.leer_demonio(nombre_demonio)
        
        if accion == 'start' and config['ExecStart']:
            subprocess.run(config['ExecStart'].split(), check=True)
            return f"Demonio {nombre_demonio} iniciado con éxito."
        elif accion == 'stop' and config['ExecStop']:
            subprocess.run(config['ExecStop'].split(), check=True)
            return f"Demonio {nombre_demonio} detenido con éxito."
        elif accion == 'restart' and config['ExecReload']:
            subprocess.run(config['ExecReload'].split(), check=True)
            return f"Demonio {nombre_demonio} reiniciado con éxito."
        else:
            raise ValueError(f"El demonio {nombre_demonio} no soporta la acción {accion}.")
