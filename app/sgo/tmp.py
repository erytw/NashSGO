import datetime
from data_wrapper import NetschoolCollector
from netschool import SGOProc
import asyncio

# lgdata - кортеж из (login, password, school)
from personal import lgdata

collector = NetschoolCollector()
proc = SGOProc()
time = datetime.datetime.now()
print(asyncio.run(collector.marks(lgdata)))
print(datetime.datetime.now() - time)
