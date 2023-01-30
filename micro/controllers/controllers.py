# -*- coding: utf-8 -*-
# from odoo import http


# class Micro(http.Controller):
#     @http.route('/micro/micro', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/micro/micro/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('micro.listing', {
#             'root': '/micro/micro',
#             'objects': http.request.env['micro.micro'].search([]),
#         })

#     @http.route('/micro/micro/objects/<model("micro.micro"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('micro.object', {
#             'object': obj
#         })
