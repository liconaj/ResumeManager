import json
from typing import Any, Dict

class Config:
    def __init__(self, config_file: str = 'config.json'):
        self.config_file = config_file
        self.config_data = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        try:
            with open(self.config_file, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            raise FileNotFoundError(f"El archivo de configuración '{self.config_file}' no se encuentra.")
        except json.JSONDecodeError:
            raise ValueError(f"Error al decodificar el archivo de configuración '{self.config_file}'.")

    def get(self, key: str) -> Any:
        #if key not in self.config_data:
        #    raise KeyError(f"La clave '{key}' no está presente en el archivo de configuración.")
        return self.config_data.get(key, None)

    def set(self, key: str, value: Any) -> None:
        self.config_data[key] = value
        self._save_config()

    def _save_config(self) -> None:
        with open(self.config_file, 'w') as file:
            json.dump(self.config_data, file, indent=4)
