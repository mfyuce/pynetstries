import json
from pony.orm import *
from pony.orm.dbapiprovider import StrConverter
from enum import Enum
import json

PAGE = 'page'


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
def new_device_data(brand, model, os: OsType, os_version):
    new_data = DeviceData(brand=brand, model=model, os=os, osVersion=os_version)
    commit()
    return str(new_data.id)


@db_session
def device_data_count():
    return count(p for p in DeviceData)


def json_out(func):
    def wrapper(**kwargs):
        ret = func(**kwargs)
        return json.dumps([p.to_dict() for p in ret], default=str)

    return wrapper


@db_session
@json_out
def query(**kwargs):
    q = select(p for p in DeviceData)
    for key, value in kwargs.items():
        if value and key in DeviceData.__dict__:
            q = q.filter(lambda x: value in kwargs[key])
    if PAGE in kwargs:
        page_num = kwargs[PAGE]
        if page_num:
            q = q.page(int(kwargs[PAGE]), 20)
    return q


cnt = device_data_count()
print(cnt)
if cnt == 0:
    with open("devices.json", "r") as devices_file:
        data = json.loads(devices_file.read())
        for device in data:
            new_device_data(device["brand"], device["model"], OsType[device["os"]], device["osVersion"])
