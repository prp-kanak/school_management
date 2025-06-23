from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.http import request
from odoo import http

class ProductStockController(WebsiteSale):
    @http.route(['/shop'], type='http', auth='public', website=True)
    def shop(self, **kwargs):
        
        response = super(ProductStockController, self).shop(**kwargs)
        
        response.qcontext['products_with_stock'] = {
            product.id: product.virtual_available
            for product in request.env['product.template'].sudo().search([])
        }
        return response