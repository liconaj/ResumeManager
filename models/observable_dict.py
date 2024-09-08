class ObservableDict(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._callback = None

    def set_callback(self, callback):
        """Establece la función callback que se ejecutará cuando el diccionario sea modificado."""
        self._callback = callback

    def _trigger_callback(self):
        """Llama al callback si está definido."""
        if self._callback is not None:
            self._callback()

    # Sobreescribimos los métodos para detectar cambios
    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        self._trigger_callback()

    def __delitem__(self, key):
        super().__delitem__(key)
        self._trigger_callback()

    def update(self, *args, **kwargs):
        super().update(*args, **kwargs)
        self._trigger_callback()

    def clear(self):
        super().clear()
        self._trigger_callback()
