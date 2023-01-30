# -*- coding: utf-8 -*-
# from odoo import http


# class Validacion(http.Controller):
#     @http.route('/validacion/validacion', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/validacion/validacion/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('validacion.listing', {
#             'root': '/validacion/validacion',
#             'objects': http.request.env['validacion.validacion'].search([]),
#         })

#     @http.route('/validacion/validacion/objects/<model("validacion.validacion"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('validacion.object', {
#             'object': obj
#         })
