from odoo import models, fields

class MixinModel(models.AbstractModel):
    _name = 'mixin.model'
    _description = 'Mixin Model with Common Fields'

    name = fields.Char(string='Name', required=True)
