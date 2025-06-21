from odoo import models, fields, api
from datetime import timedelta
 
class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.model_create_multi
    def action_check_sale_order_state(self):
        ten_days_ago = fields.Datetime.now() - timedelta(days=10)
        sale_orders = self.search([
            ('create_date', '>=', ten_days_ago),
            ('state', '=', 'draft')
        ])
        if sale_orders:
            sale_orders.unlink()