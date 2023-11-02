import sys
from datetime import datetime, timedelta

import httpx
import asyncio
import platform


class HttpError(Exception):
    pass

MAX_DAYS = 10

async def request(url: str):
    async with httpx.AsyncClient() as client:
        r = await client.get(url)
        if r.status_code == 200:
            result = r.json()
            return result
        else:
            raise HttpError(f"Error status: {r.status_code} for {url}")


async def main(index_day):
    if index_day > MAX_DAYS:
        raise ValueError("Максимальна кількість днів - 10")
    d = datetime.now() - timedelta(days=int(index_day))
    shift = d.strftime("%d.%m.%Y")
    try:
        response = await request(f'https://api.privatbank.ua/p24api/exchange_rates?date={shift}')
        return response
    except HttpError as err:
        print(err)
        return None


if __name__ == '__main__':
    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    try:
        if len(sys.argv) > 1:
            index_day = int(sys.argv[1])
            r = asyncio.run(main(index_day))
            print(r)
        else:
            print("Вкажіть кількість днів.")
    except ValueError as err:
        print(err)
