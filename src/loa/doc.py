from pydantic import BaseModel, ConfigDict, field_validator


class Doc(BaseModel):
    model_config = ConfigDict(populate_by_name=True, validate_assignment=True, extra="forbid")

    filename: str
    name: str

    firs: list[str] = []
    """List of FIRs who are parties to the document. The ICAO indicators are user-facing."""

    related_firs: list[str] | None = None
    """Optional list of FIRs where the document is relevant and to be shown by default as well."""

    keywords: list[str] | None = None
    """Optional list of search keywords for document selection."""

    airac: int = 0
    """AIRAC cycle where the current revision of the document became effective."""

    effective_date: str = ""
    """ISO-8601 formatted date where the current revision of the document became effective."""

    @field_validator("airac")
    @classmethod
    def validate_airac(cls, airac: int):
        if airac < 2000 or airac > 3000:
            msg = f"Implausible AIRAC cycle {airac}"
            raise ValueError(msg)

        return airac
