from typing import List, Literal, Self, Tuple
from pydantic import BaseModel, model_validator

from validators.runway import validate_runways

TransferTypes = Literal["C", "D"]
ReleaseTypes = Literal["C", "D", "T", "F"]


class Agreement(BaseModel):
    # required:
    from_sector: str
    to_sector: str

    # adep OR ades required
    adep: List[str] | None = None
    ades: List[str] | None = None

    runway: List[str] | None = None
    cop: str | None = None
    route_before: str | None = None
    route_after: str | None = None
    level: int | None = None
    transfer_type: TransferTypes | None = None
    sfl: int | None = None
    level_at: Tuple[int, str] | None = None
    qnh: str | None = None
    releases: ReleaseTypes | None = None
    remark: str | None = None
    vertical: bool | None = None
    areas: List[str] | None = None
    rfl: str | None = None

    class Config:
        """enables validation on assignment, used to make testing more maintainable"""

        validate_assignment = True

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        return Agreement(
            from_sector=data.get("fromSector"),
            to_sector=data.get("toSector"),
            adep=data.get("adep"),
            ades=data.get("ades"),
            runway=data.get("runway"),
            cop=data.get("cop"),
            route_before=data.get("routeBefore"),
            route_after=data.get("routeAfter"),
            level=data.get("level"),
            transfer_type=data.get("transferType"),
            sfl=data.get("sfl"),
            level_at=data.get("levelAt"),
            qnh=data.get("qnh"),
            releases=data.get("releases"),
            remark=data.get("remarks"),
            vertical=data.get("vertical"),
            areas=data.get("areas"),
            rfl=data.get("rfl"),
        )

    @model_validator(mode="after")
    def validate_adep_ades(self) -> Self:
        if not self.adep and not self.ades:
            raise ValueError("Agreement must have ADEP or ADES")

        if self.adep and not isinstance(self.adep, list):
            raise ValueError("ADEP must be of type list")

        if self.ades and not isinstance(self.ades, list):
            raise ValueError("ADES must be of type list")

        return self

    @model_validator(mode="after")
    def validate_runway(self) -> Self:
        # as runway field is optional:
        if not self.runway:
            return self

        self.runway = validate_runways(self.runway)

        return self
