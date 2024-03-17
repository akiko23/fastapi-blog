from typing import Any, Callable, Dict, Hashable, NoReturn


class Stub:
    def __init__(
        self,
        dependency: Callable[[Any, ...], Any],  # type: ignore[misc]
        **kwargs: Dict[Hashable, Any],
    ) -> None:
        self._dependency = dependency
        self._kwargs = kwargs

    def __call__(self) -> NoReturn:
        raise NotImplementedError

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Stub):
            return (
                self._dependency == other._dependency and self._kwargs == other._kwargs
            )
        else:
            if not self._kwargs:
                return bool(self._dependency == other)
            return False

    def __hash__(self) -> int:
        if not self._kwargs:
            return hash(self._dependency)
        serial = (
            self._dependency,
            *self._kwargs.items(),
        )
        return hash(serial)
