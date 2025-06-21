from odoo import api, fields, models, _
from odoo.exceptions import UserError


class ProductLabelLayoutDemo(models.TransientModel):
    _inherit = 'product.label.layout'

    print_format = fields.Selection(
        selection_add=[('3X9Xprice', '3x9 format')],
        ondelete={'3X9Xprice': 'set default'}
    )

    @api.depends('print_format')
    def _compute_dimensions(self):
        for wizard in self:
            if 'x' in wizard.print_format:
                columns, rows = wizard.print_format.split('x')[:2]
                wizard.columns = columns.isdigit() and int(columns) or 1
                wizard.rows = rows.isdigit() and int(rows) or 1
            else:
                wizard.columns, wizard.rows = 1, 1

    def _prepare_report_data(self):
        xml_id, data = super()._prepare_report_data()

        if self.print_format == '3X9Xprice':
            xml_id = 'school_management.report_product_template_label_3X9_label'

        return xml_id, data

    def process(self):
        self.ensure_one()
        xml_id, data = self._prepare_report_data()
        if not xml_id:
            raise UserError(_('Unable to find report template for %s format', self.print_format))
        report_action = self.env.ref(xml_id).report_action(None, data=data, config=False)
        report_action.update({'close_on_report_download': True})
        return report_action
