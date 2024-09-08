import toml
from typing import Any

_DEFAULT_CONFIG = {
    "APPLICATION_STYLE": "Fusion",
    "FONT_DPI": 96,
    "MASTER_SHEET_ID": "",
    "MASTER_SHEET_RANGE": "",
}

class Config:
    def __init__(self, config_file: str = 'config.txt'):
        self.config_file = config_file
        self.config_data = self._load_config()

    def _load_config(self) -> dict[str, Any]:
        try:
            return toml.load(self.config_file)
        except FileNotFoundError:
            # raise FileNotFoundError(f"El archivo de configuración '{self.config_file}' no se encuentra.")
            return _DEFAULT_CONFIG
        except toml.TomlDecodeError:
            raise ValueError(f"Error al decodificar el archivo de configuración '{self.config_file}'.")

    def get(self, key: str) -> Any:
        return self.config_data.get(key, None)

    def set(self, key: str, value: Any) -> None:
        self.config_data[key] = value
        self._save_config()

    def _save_config(self) -> None:
        with open(self.config_file, 'w') as file:
            toml.dump(self.config_data, file)
