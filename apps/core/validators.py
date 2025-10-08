import re
from typing import NoReturn

from django.core.exceptions import ValidationError


def is_hex_color(attrs: dict[str, str]) -> dict[str, str] | NoReturn:
    """Check to make sure color is a hex color"""

    color: str = attrs.get("color", "")
    if bool(re.fullmatch(r"#(?:[0-9a-fA-F]{3}|[0-9a-f-A-F]{6})", color)):
        return attrs
    raise ValidationError("Color has to be a hex color")
