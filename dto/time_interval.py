from pydantic import BaseModel, root_validator
from fastapi import HTTPException


class TimeInterval(BaseModel):
    from_ts: int
    to_ts: int

    @root_validator(pre=True)
    def check_time(cls, values):
        if values["from_ts"] > values["to_ts"]:
            raise HTTPException(status_code=422, detail="`to_ts` must be greater or equal to  `from_ts`.")
        if values["from_ts"] == values["to_ts"]:
            values["to_ts"] += 1
        return values