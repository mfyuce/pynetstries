import random
import string

import cherrypy
import device_db


@cherrypy.expose
class DeviceDataWebService(object):

    @cherrypy.tools.accept(media='application/json')
    def POST(self, brand, model, os, osVersion):
        return device_db.new_device_data(brand, model, device_db.OsType[os], osVersion)




if __name__ == '__main__':
    conf = {
        '/': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.sessions.on': False,
            'tools.response_headers.on': True,
            'tools.response_headers.headers': [('Content-Type', 'text/javascript')],
        }
    }
    cherrypy.quickstart(DeviceDataWebService(), '/', conf)
