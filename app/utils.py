import re

def normalize_br_phone(raw: str) -> str | None:
    """Normaliza para E.164 Brasil (+55). Retorna None se inválido."""
    if not raw:
        return None
    digits = re.sub(r"\D+", "", str(raw))
    if not digits:
        return None

    digits = digits.lstrip("0")

    if len(digits) == 11:
        return f"+55{digits}"
    if len(digits) == 10:
        return f"+55{digits[:2]}9{digits[2:]}"
    if len(digits) in (13, 14) and digits.startswith("55"):
        return f"+{digits}"
    if len(digits) == 12 and digits.startswith("55"):
        return f"+55{digits[2:4]}9{digits[4:]}"

    return None
