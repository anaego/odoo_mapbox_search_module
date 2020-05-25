# -*- coding: utf-8 -*-
# from odoo import http


# class Testtask(http.Controller):
#     @http.route('/testtask/testtask/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/testtask/testtask/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('testtask.listing', {
#             'root': '/testtask/testtask',
#             'objects': http.request.env['testtask.testtask'].search([]),
#         })

#     @http.route('/testtask/testtask/objects/<model("testtask.testtask"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('testtask.object', {
#             'object': obj
#         })
