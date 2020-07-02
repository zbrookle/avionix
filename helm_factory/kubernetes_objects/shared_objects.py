from typing import Optional

EXISTS = "Exists"
EQUAL = "Equal"


class Toleration:
    def __init__(
        self,
        effect: Optional[str] = None,
        key: Optional[str] = None,
        operator: Optional[str] = EQUAL,
        value: Optional[str] = None,
        toleration_seconds: Optional[int] = None,
    ):
        assert operator in [EXISTS, EQUAL]
        self.effect = effect
        self.key = key
        self.operator = operator
        self.tolerationSeconds = toleration_seconds
        self.value = value
