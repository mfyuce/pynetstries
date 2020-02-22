import cherrypy

import device_db


class DeviceDataWebService(object):
    @cherrypy.tools.accept(media='application/json')
    @cherrypy.expose
    def index(self, brand=None, model=None, os=None, osVersion=None):
        if not brand:
            return ""
        return device_db.new_device_data(brand, model, device_db.OsType[os], osVersion)

    @cherrypy.expose(['devices'])
    # @cherrypy.tools.json_out() # not working with Enum for now
    def devices(self, brand=None, model=None, os=None, osVersion=None, page=None):
        return device_db.query(brand=brand, model=model, os=device_db.OsType[os] if os else None, osVersion=osVersion, page=page)


if __name__ == '__main__':
    cherrypy.quickstart(DeviceDataWebService())
