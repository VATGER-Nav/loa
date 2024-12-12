from typing import List


def validate_runway(runway: str):
    runway = runway.strip().upper()

    if len(runway) < 2 or len(runway) > 3:
        raise ValueError(f"Invalid ruwnay format: '{runway}'")

    if not runway[:2].isdigit():
        raise ValueError(f"Invalid runway number: '{runway}'")

    runway_number = int(runway[:2])
    if not 1 <= runway_number <= 36:
        raise ValueError(f"Runway number out of range: '{runway}'")

    if len(runway) == 3:
        suffix = runway[2]
        if suffix not in {"L", "C", "R"}:
            raise ValueError(f"Invalid runway suffix: '{runway}'")

    return runway


def validate_runways(runways: List[str]):
    for i in range(len(runways)):
        runways[i] = validate_runway(runways[i])

    return runways
