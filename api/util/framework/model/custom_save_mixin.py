class CustomSaveMixin:
    def save_without_signals(self) -> None:
        self._disable_signals = True
        self.save()  # type: ignore[attr-defined]
        self._disable_signals = False
