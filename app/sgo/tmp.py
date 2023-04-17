from datetime import datetime
from data_wrapper import netschool_collector
from netschool import sgoproc
import asyncio

# lgdata - кортеж из (login, password, school)
from personal import lgdata

collector = netschool_collector()
proc = sgoproc()
time = datetime.now()
print(asyncio.run(collector.homework(lgdata)))
print(datetime.now() - time)
