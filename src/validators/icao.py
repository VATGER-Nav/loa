import re
from typing import List


def validate_icao(icao: str) -> str:
    icao = icao.strip().upper()

    pattern = r"^[a-zA-Z0-9]{4}$"
    if not bool(re.match(pattern, icao)):
        raise ValueError("ICAO must be alphanumerical and max 4 chars")

    return icao


def validate_icaos(icaos: List[str]) -> List[str]:
    for i in range(len(icaos)):
        icaos[i] = validate_icao(icaos[i])

    return icaos
