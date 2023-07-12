import struct
import aiofiles
from async_lru import alru_cache
from fastapi import HTTPException
from dto import Header
from main import Point

# encoding LE
ENCODING = "<7l1f"


@alru_cache(maxsize=1000)
async def get_temp(filename: str, point: Point):
    fp = await aiofiles.open(f"./data/{filename}", mode="rb")

    header_bin = await fp.read(32)
    header = Header(*struct.unpack(ENCODING, header_bin))
    X, Y = int(header.multiplier * point.lat), int(header.multiplier * point.lon)

    if not(header.minX <= X <= header.maxX and header.minY <= Y <= header.maxY):
        return None

    cols = (header.maxX - header.minX) // header.dx
    nx_step = (X - header.minX) // header.dx
    ny_step = (Y - header.minY) // header.dy

    try:
        await fp.seek(8 * nx_step + 8 * cols * ny_step)
        content = await fp.read(32)
    except Exception as err:
        print(err)
        raise HTTPException(status_code=400, detail="Read file index has come EOF.")

    data = struct.unpack(ENCODING, content)
    return {'temp': data[-1]}

