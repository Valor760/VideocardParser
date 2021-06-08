from apscheduler.schedulers.asyncio import AsyncIOScheduler
import asyncio
import os
from datetime import datetime

def current_time():
    print(datetime.utcnow(), "\t (don't forget about +2 hours!)")

def dateks():
    os.system('python parser_dateks.py')

def _1a():
    os.system('python parser_1a.py')

def rde():
    os.system('python parser_rde.py')

def all_at_once():
    current_time()
    dateks()
    _1a()
    rde()
    print()


if __name__ == '__main__':
    all_at_once()


    scheduler = AsyncIOScheduler()

    scheduler.add_job(all_at_once, 'interval', minutes=10)

    scheduler.start()

    try:
        asyncio.get_event_loop().run_forever()
    except:
        pass
