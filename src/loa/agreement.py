from typing import Literal, Self

from pydantic import BaseModel, ConfigDict, field_validator, model_validator

from .validators.runway import validate_runways

TransferTypes = Literal["C", "D"] | None
"""
`"C"` for transfer of traffic climbing to the specified `level`, `"D"` for descending,
`None` for traffic to be at `level`.
"""

ReleaseTypes = Literal["C", "D", "T", "F"] | None
"""
If traffic is:

- `"D"`: released for descent
- `"C"`: released for climb
- `"T"`: released for turns
- `"F"`: fully released
- `None`: not released

"""


class Agreement(BaseModel):
    model_config = ConfigDict(populate_by_name=True, validate_assignment=True, extra="forbid")

    from_sector: str
    to_sector: str

    adep: list[str] | None = None
    """ICAO identifier of departure airports, one of which must match for the agreement
    to apply. If `adep` and `ades` are specified one of each must match."""

    ades: list[str] | None = None
    """ICAO identifier of destination airports, one of which must match for the agreement
    to apply. If `adep` and `ades` are specified one of each must match."""

    runway: list[str] | None = None
    """Active runway of one of the airports in `ades` or `adep`."""

    cop: str | None = None
    """Coordination point of the agreement, `None` if the agreement shall apply to any
    traffic from `from_sector` to `to_sector`."""

    route_before: str | None = None
    """Route elements prior to the `cop`. This can be an airway or IFPS compatible
    route elements: i.e. `"T161"`, `"KOSIX L986 MAG"`"""

    route_after: str | None = None
    """Route elements after the `cop`. This can be an airway or IFPS compatible
    route elements: i.e. `"T161"`, `"KOSIX L986 MAG"`"""

    level: int | None = None
    """Flight level at which the traffic is to be transferred. `None` for traffic that
    needs individual coordination."""

    transfer_type: TransferTypes = None
    """`"C"` for transfer of traffic climbing to the specified `level`, `"D"` for descending,
    `ǹull` for traffic to be at `level`."""

    sfl: int | None = None
    """Supplementary flight level, the level out of which the traffic has to be climbing,
    descending. (`transfer_type`)"""

    level_at: tuple[int, str] | None = None
    """
    Additional specification for the location where the traffic has to meet the transfer
    conditions:

    - `None`: 0.5 * radar separation to border
    - `[-5, "KPT"]`: latest 5 nm prior to `KPT`
    - `[15, "MAH"]`: latest 15 nm after `MAH`
    - `[0, "RUDNO"]`: latest at or abeam `RUDNO`
    """

    qnh: str | None = None
    """
    For agreements where traffic is transferred at an altitude, the value of this property
    is the ICAO code of the reference QNH, i.e. 8000ft on EDDM QNH:

    ```toml
    [[agreements]]
    cop = "TITIG"
    level = 80
    sfl = 120
    ades = ["LOWS"]
    transferType = "D"
    qnh = "EDDM"
    from_sector = "ed/DMSL"
    to_sector = "lo/LOWS_APP"
    ```
    """

    releases: ReleaseTypes = None
    """Release given, see `ReleaseTypes`"""

    remarks: str | None = None
    """Further remarks for more specific releases or conditions."""

    vertical: bool = False
    """Boolean value if the agreement specifies a silent vertical transfer."""

    areas: list[str] = []

    rfl: str | None = None

    @model_validator(mode="after")
    def validate_adep_ades(self) -> Self:
        if not self.adep and not self.ades:
            msg = "Agreement must have ADEP or ADES"
            raise ValueError(msg)

        return self

    @field_validator("runway")
    @classmethod
    def validate_runway(cls, runway: list[str]):
        # as runway field is optional:
        if not runway:
            return

        return validate_runways(runway)
