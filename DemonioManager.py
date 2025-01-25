import threading
import time

class Demonio:
    def __init__(self, name):
        self.name = name
        self.running = False
        self.thread = None

    def start(self):
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self.run, daemon=True)
            self.thread.start()
        return f"Demonio '{self.name}' iniciado."

    def stop(self):
        if self.running:
            self.running = False
            if self.thread:
                self.thread.join()
        return f"Demonio '{self.name}' detenido."

    def restart(self):
        self.stop()
        return self.start()

    def run(self):
        """Simula el trabajo del demonio."""
        while self.running:
            print(f"Demonio '{self.name}' está ejecutándose...")
            time.sleep(5)  # Simula actividad del demonio


class DemonioManager:
    def __init__(self):
        self.demonios = {}

    def add_demonio(self, name):
        if name in self.demonios:
            return f"El demonio '{name}' ya existe."
        self.demonios[name] = Demonio(name)
        return f"Demonio '{name}' agregado."

    def start_demonio(self, name):
        if name in self.demonios:
            return self.demonios[name].start()
        return f"El demonio '{name}' no existe."

    def stop_demonio(self, name):
        if name in self.demonios:
            return self.demonios[name].stop()
        return f"El demonio '{name}' no existe."

    def restart_demonio(self, name):
        if name in self.demonios:
            return self.demonios[name].restart()
        return f"El demonio '{name}' no existe."

    def list_demonios(self):
        return [name for name in self.demonios]
