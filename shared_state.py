class SharedState:
    def __init__(self):
        self._current_profile = None
        self._callbacks = []

    @property
    def current_profile(self):
        return self._current_profile

    @current_profile.setter
    def current_profile(self, profile_name):
        self._current_profile = profile_name
        self._notify_callbacks()

    def register_callback(self, callback):
        self._callbacks.append(callback)

    def _notify_callbacks(self):
        for callback in self._callbacks:
            callback(self._current_profile)
