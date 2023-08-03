# -*- coding: utf-8 -*-
# from odoo import http


# class OmInheritence(http.Controller):
#     @http.route('/om_inheritence/om_inheritence/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/om_inheritence/om_inheritence/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('om_inheritence.listing', {
#             'root': '/om_inheritence/om_inheritence',
#             'objects': http.request.env['om_inheritence.om_inheritence'].search([]),
#         })

#     @http.route('/om_inheritence/om_inheritence/objects/<model("om_inheritence.om_inheritence"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('om_inheritence.object', {
#             'object': obj
#         })
