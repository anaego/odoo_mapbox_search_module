# -*- coding: utf-8 -*-
import os

from mapbox import Geocoder

from odoo import models, fields, api


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
        """
        Overring odoo's search function for custom search logic;
        Works for searches with "or" condition as well
        """
        res = []
        # If it's just a search of all elements
        if len(args) == 0:
            res = self._search(args, offset=offset, limit=limit, order=order,
                               count=count)
        # for multiple "or" search conditions
        search_phrases = [condition for condition in args if len(condition) > 1]
        for search_phrase in search_phrases:
            # Search in database
            temp_res = self._search([search_phrase], offset=offset, limit=limit,
                                    order=order, count=count)
            if not temp_res:
                # If no info in database, search it in mapbox
                geocoder = Geocoder(access_token="pk.eyJ1IjoiYW5hZWdvIiwiYSI6ImNrYW12YzMyeTE3eWUydHRkMndibGFyd3kifQ.At3CmGu9R8ZJS_Tpt9ngFQ")
                # geocoder = Geocoder(access_token=os.environ['MAPBOX_ACCESS_TOKEN'])
                response = geocoder.forward(search_phrase[2]).geojson()['features'][0]
                place_name = response["place_name"]
                coordinates = response["geometry"]["coordinates"]
                city = response["text"] if "place" in response["place_type"] else None
                country = response["text"] if "country" in response[
                    "place_type"] else None
                temp_res = [
                    self.create([{"place_name": place_name, "coordinates": coordinates,
                                  "city": city, "country": country}]).id]
            # Append found database or mapbox info to the final result
            res += temp_res
        return res if count else self.browse(res)
