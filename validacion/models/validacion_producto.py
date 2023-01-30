#-*- coding: utf-8 -*-

from odoo import models, fields, api


class Producto(models.Model):
    _name = 'validacion.producto'
    _description = 'validacion.producto'

    apellido = fields.Char()
    ciudad = fields.Char()
