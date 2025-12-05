# from odoo import http


# class CoverLettter(http.Controller):
#     @http.route('/cover_lettter/cover_lettter', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/cover_lettter/cover_lettter/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('cover_lettter.listing', {
#             'root': '/cover_lettter/cover_lettter',
#             'objects': http.request.env['cover_lettter.cover_lettter'].search([]),
#         })

#     @http.route('/cover_lettter/cover_lettter/objects/<model("cover_lettter.cover_lettter"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('cover_lettter.object', {
#             'object': obj
#         })

