# -*- coding: utf-8 -*-

import logging

from odoo import fields, models, api
from odoo.exceptions import UserError

logger = logging.getLogger(__name__)

class Presupuesto(models.Model):
    _name = "presupuesto"
    _inherit = ['image.mixin']

    @api.depends('detalle_ids')
    def _compute_total(self):
        for rcord in self:
            sub_total = 0
            for linea in rcord.detalle_ids:
                sub_total += linea.importe
            rcord.base = sub_total
            rcord.impuestos = sub_total * 0.12
            rcord.total = sub_total * 1.12


    name = fields.Char(string='Pelicula')
    clasificacion = fields.Selection(selection=[
        ('G', 'G'), # Publico general
        ('PG', 'PG'),  # Se recomienda la compania de un adulto
        ('PG-13', 'PG-13'),  # Mayores de 13 años
        ('R', 'R'),  # En compania de un adulto obligatorio
        ('NC-17', 'NC-17'),  # Mayores de 18
    ], string='clasificación')
    dsc_clasificacion = fields.Char(string = 'Descripcion clasificacion')
    fch_estreno = fields.Date(string='Fecha estreno')
    puntuacion = fields.Integer(string='Puntuación', related="puntuacion2")
    puntuacion2 = fields.Integer(string='Puntuación')
    active = fields.Boolean(string='Activo', default=True)
    director_id = fields.Many2one(
        comodel_name='res.partner',
        string='Director'
    )

    categoria_director_id = fields.Many2one(
        comodel_name='res.partner.category',
        string='Categoria Director',
        # segunda version
        default=lambda self: self.env.ref('peliculas.category_director') #hace referencia al id del record en /data/categoria.xml

        # primera version
        # default=lambda self: self.env['res.partner.category'].search([('name', '=', 'Director')])
    )

    genero_ids = fields.Many2many(
        comodel_name='genero',
        string='Género'
    )
    vista_general = fields.Text(string='Descripción')
    link_trailer = fields.Char(string='Trailer')
    es_libro = fields.Boolean(string='Version Libro')
    libro = fields.Binary(string='Libro')
    libro_filename = fields.Char(string='Nombre del libro')

    state = fields.Selection(selection=[
        ('borrador', 'Borrador'),
        ('aprobado', 'Aprobado'),
        ('cancelado', 'Cancelado'),
    ], default='borrador', string='Estados', copy=False)
    fch_aprobado = fields.Datetime(string="Fecha aprobado", copy=False)
    num_presupuesto = fields.Char(string='Numero presupuesto', copy=False)
    fch_creacion = fields.Datetime(string='Fecha creacion', copy=False, default=lambda self: fields.Datetime.now())
    actor_ids = fields.Many2many(
        comodel_name='res.partner',
        string='Actores'
    )

    categoria_actor_id = fields.Many2one(
        comodel_name='res.partner.category',
        string='Categoria Actor',
        default=lambda self: self.env.ref('peliculas.category_actor')
    )
    opinion = fields.Html(string='Opinion')

    #relacion con los detalles relacion One2many
    detalle_ids = fields.One2many(
        comodel_name='presupuesto.detalle',
        #relacion del detalle con la cabecera
        inverse_name='presupuesto_id',
        string='Detalles',
    )

    campos_ocultos = fields.Boolean(string='Campos ocultos')

    currency_id = fields.Many2one(
        comodel_name='res.currency',
        string='Moneda',
        default=lambda self: self.env.company.currency_id.id,
    )

    terminos = fields.Text(string='Terminos')
    base = fields.Monetary(string='Base imponible', compute='_compute_total')
    impuestos = fields.Monetary(string='Impuestos', compute='_compute_total')
    total = fields.Monetary(string='Total', compute='_compute_total')

    def aprobar_presupuesto(self):
        logger.info('Entro a la funcion aprobar presupuesto')
        self.state = 'aprobado'
        self.fch_aprobado = fields.Datetime.now()

    def cancelar_presupuesto(self):
        logger.info('Entro a la funcion aprobar presupuesto')
        self.state = 'cancelado'

    def unlink(self):
        logger.info('********Se disparo la funcion unlink')
        for record in self:
            if record.state != 'cancelado':
                raise UserError('Solo se eliminan registros con estado cancelado')
            super(Presupuesto, record).unlink()

    @api.model
    def create(self, variables):
        logger.info('******** variables: {0}'.format(variables))
        sequence_obj = self.env['ir.sequence']
        correlativo = sequence_obj.next_by_code('secuencia.presupuesto.peliculas')
        variables['num_presupuesto'] = correlativo
        return super(Presupuesto, self).create(variables)

    def write(self, variables):
        logger.info('******** variables: {0}'.format(variables))
        if 'clasificacion' in variables:
            raise UserError('La clasificacion no se puede editar')
        return super(Presupuesto, self).write(variables)

    def copy(self, default=None):
        default = dict(default or {})
        default['name'] = self.name + ' (Copia)'
        default['puntuacion2'] = 1
        return super(Presupuesto, self).copy(default)

    @api.onchange('clasificacion')
    def _onchage_clasificacion(self):
        if self.clasificacion:
            if self.clasificacion == 'G':
                self.dsc_clasificacion = 'Publico general'
            if self.clasificacion == 'PG':
                self.dsc_clasificacion = 'Se recomienda la compania de un adulto'
            if self.clasificacion == 'PG-13':
                self.dsc_clasificacion = 'Mayores de 13 años'
            if self.clasificacion == 'R':
                self.dsc_clasificacion = 'En compania de un adulto obligatorio'
            if self.clasificacion == 'NC-17':
                self.dsc_clasificacion = 'Mayores de 18'
        else:
            self.dsc_clasificacion = False

class PresupuestoDetalle(models.Model):
    _name = "presupuesto.detalle"
    
    presupuesto_id = fields.Many2one(
        comodel_name='presupuesto',
        string='Presupuesto',
    )
    name = fields.Many2one(
        comodel_name='recurso.cinematografico', #debe listar los productos del modelo product.product
        string='Recurso',
    )
    descripcion = fields.Char(string='Descripcion',related='name.descripcion')
    contacto_id = fields.Many2one(
        comodel_name='res.partner',
        string='Contacto',
        related='name.contacto_id'
    )
    imagen = fields.Binary(string='Imagen',related='name.imagen')
    cantidad = fields.Float(string='Cantidad', default=1.0, digits=(16, 4))
    precio = fields.Float(string='Precio', digits='Product Price')
    importe = fields.Monetary(string='Importe')

    currency_id = fields.Many2one(
        comodel_name='res.currency',
        string='Moneda',
        related='presupuesto_id.currency_id'
    )
    

    @api.onchange('name')
    def _onchange_name(self):
        if self.name:
            self.precio = self.name.precio

    
    @api.onchange('cantidad', 'precio')
    def _onchange_importe(self):
        self.importe = self.cantidad * self.precio
    
     
    