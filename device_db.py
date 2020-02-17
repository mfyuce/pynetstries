import json
from pony.orm import *
from pony.orm.dbapiprovider import StrConverter
from enum import Enum


class EnumConverter(StrConverter):
    def validate(self, val, obj=None):
        if not isinstance(val, Enum):
            raise ValueError('Must be an Enum. Got {}'.format(val))
        return val

    def py2sql(self, val):
        return val.name

    def sql2py(self, val):
        return self.py_type[val]

    def sql_type(self):
        return 'VARCHAR(30)'


db = Database()


class OsType(Enum):
    Android = "Android"
    iOS = "iOS"


class DeviceData(db.Entity):
    brand = Required(str)
    model = Required(str)
    os = Required(OsType)
    osVersion = Required(str)
    composite_key(brand, model, osVersion)


db.bind(provider='sqlite', filename='database.sqlite', create_db=True)
db.provider.converter_classes.append((Enum, EnumConverter))
db.generate_mapping(create_tables=True)


@db_session
def new_device_data(brand, model, os: OsType, osVersion):
    new_data = DeviceData(brand=brand, model=model, os=os, osVersion=osVersion)
    commit()
    return  str(new_data.id)


@db_session
def device_data_count():
    return count(p for p in DeviceData)


cnt = device_data_count()
print(cnt)
if cnt == 0:
    with open("devices.json", "r") as devices_file:
        data = json.loads(devices_file.read())
        for device in data:
            new_device_data(device["brand"], device["model"], OsType[device["os"]], device["osVersion"])
