def validate_runway(runway: str):
    runway = runway.strip().upper()

    if len(runway) < 2 or len(runway) > 3:
        msg = f"Invalid ruwnay format: '{runway}'"
        raise ValueError(msg)

    if not runway[:2].isdigit():
        msg = f"Invalid runway number: '{runway}'"
        raise ValueError(msg)

    runway_number = int(runway[:2])
    if not 1 <= runway_number <= 36:
        msg = f"Runway number out of range: '{runway}'"
        raise ValueError(msg)

    if len(runway) == 3:
        suffix = runway[2]
        if suffix not in {"L", "C", "R"}:
            msg = f"Invalid runway suffix: '{runway}'"
            raise ValueError(msg)

    return runway


def validate_runways(runways: list[str]):
    for i in range(len(runways)):
        runways[i] = validate_runway(runways[i])

    return runways
