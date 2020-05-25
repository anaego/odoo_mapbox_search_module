# -*- coding: utf-8 -*-

from odoo import models, fields, api
from mapbox import Geocoder


class Place(models.Model):
    _name = 'testtask.place'
    _description = 'Test task place model'

    place_name = fields.Char(required=True)
    coordinates = fields.Char()
    city = fields.Char()
    country = fields.Char()

    @api.model
    @api.returns('self',
                 upgrade=lambda self, value, args, offset=0, limit=None, order=None,
                                count=False: value if count else self.browse(value),
                 downgrade=lambda self, value, args, offset=0, limit=None, order=None,
                                  count=False: value if count else value.ids)
    def search(self, args, offset=0, limit=None, order=None, count=False):
        """Overring odoo's search function for custom search logic"""
        res = self._search(args, offset=offset, limit=limit, order=order, count=count)
        if not res and len(args) != 0:
            search_phrase = args[0][2]
            geocoder = Geocoder(access_token=os.environ['MAPBOX_ACCESS_TOKEN'])
            response = geocoder.forward(search_phrase).geojson()['features'][0]
            place_name = response["place_name"]
            coordinates = response["geometry"]["coordinates"]
            city = response["text"] if "place" in response["place_type"] else None
            country = response["text"] if "country" in response["place_type"] else None
            result = self.create([{"place_name": place_name, "coordinates": coordinates,
                                   "city": city, "country": country}])
            res.append(result.id)
        return res if count else self.browse(res)
