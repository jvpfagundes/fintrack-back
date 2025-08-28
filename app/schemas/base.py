from pydantic import BaseModel


class DateRangeSchema(BaseModel):
    dat_start: str
    dat_end: str


class DateTimeRangeSchema(BaseModel):
    datm_start: str
    datm_end: str