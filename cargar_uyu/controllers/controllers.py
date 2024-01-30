# -*- coding: utf-8 -*-
# from odoo import http


# class CargarUyu(http.Controller):
#     @http.route('/cargar_uyu/cargar_uyu', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/cargar_uyu/cargar_uyu/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('cargar_uyu.listing', {
#             'root': '/cargar_uyu/cargar_uyu',
#             'objects': http.request.env['cargar_uyu.cargar_uyu'].search([]),
#         })

#     @http.route('/cargar_uyu/cargar_uyu/objects/<model("cargar_uyu.cargar_uyu"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('cargar_uyu.object', {
#             'object': obj
#         })

