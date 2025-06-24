from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.http import request
from odoo import http



class WebsiteSaleInherit(WebsiteSale):
    def _prepare_product_values(self, product, category, search, **kwargs):
        values = super(WebsiteSaleInherit, self)._prepare_product_values(product, category, search, **kwargs)
        values['minimum_order_qty'] = product.product_variant_id.minimum_order_qty
        return values

    def _prepare_product_values(self, product, category, search, **kwargs):
        values = super(WebsiteSaleInherit, self)._prepare_product_values(product, category, search, **kwargs)
        values['sales_count'] = product.sales_count  
        return values


    @http.route(['/shop'], type='http', auth="public", website=True)
    def shop(self, **kwargs):
        response = super(WebsiteSaleInherit, self).shop(**kwargs)

        new_arrival_products = request.env['product.product'].sudo().search([('new_arrival', '=', True)]) or []
        response.qcontext['new_arrival_products'] = new_arrival_products
        return response
