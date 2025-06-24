from odoo import models, fields, api
 
class SaleOrder(models.Model):
    _inherit = 'sale.order'
 
    nationality = fields.Char(string="Nationality")
    invoice_date = fields.Char(string="Invoice Date")
    custom_email = fields.Char(string="Custom Email")
    custom_note = fields.Text(string="Custom Note")


class ProductTemplate(models.Model):
    _inherit = 'product.template'
  
    product_priority = fields.Char(string="Product Priority")


class ProductProduct(models.Model):
    _inherit = "product.product"

    minimum_order_qty = fields.Integer(string="Minimum Order Quantity", default=2)
    new_arrival = fields.Boolean(String="New Arrival")