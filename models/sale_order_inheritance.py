from odoo import models, fields, api
 
class SaleOrder(models.Model):
    _inherit = 'sale.order'
 
    nationality = fields.Char(string="Nationality")
    invoice_date = fields.Char(string="Invoice Date")
    custom_email = fields.Char(string="Custom Email")


class ProductTemplate(models.Model):
    _inherit = 'product.template'
  
    product_priority = fields.Char(string="Product Priority")



