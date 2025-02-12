import re


def validate_icao(icao: str) -> str:
    icao = icao.strip().upper()

    pattern = r"^[a-zA-Z0-9]{4}$"
    if not bool(re.match(pattern, icao)):
        msg = "ICAO must be alphanumerical and max 4 chars"
        raise ValueError(msg)

    return icao


def validate_icaos(icaos: list[str]) -> list[str]:
    return list(map(validate_icao, icaos))
