# -*- coding: utf-8 -*-
# from odoo import http


# class Confirmation(http.Controller):
#     @http.route('/confirmation/confirmation/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/confirmation/confirmation/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('confirmation.listing', {
#             'root': '/confirmation/confirmation',
#             'objects': http.request.env['confirmation.confirmation'].search([]),
#         })

#     @http.route('/confirmation/confirmation/objects/<model("confirmation.confirmation"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('confirmation.object', {
#             'object': obj
#         })
