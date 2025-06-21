from odoo import fields, models, api
from odoo.exceptions import UserError
import xlsxwriter
import io 
import base64

class WizardDemo(models.TransientModel):
    _name = 'wizard.demo'
    _description = 'Wizard Demo'

    start_date = fields.Date(string="Start Date", required=True)
    end_date = fields.Date(string="End Date", required=True)
    sale_orders = fields.Many2many('sale.order', string="Sale Orders")

    def action_confirm(self):
        if self.start_date > self.end_date:
            raise UserError("Start Date cannot be greater than End Date.")

        sale_orders = self.env['sale.order'].search([
            ('date_order', '>=', self.start_date),
            ('date_order', '<=', self.end_date)
        ])

        if not sale_orders:
            raise UserError("No sale orders found for the selected date range.")

        self.sale_orders = sale_orders

        return self.env.ref('school_management.action_wizard_sale_order_report').report_action(self)

    def action_generate_xlsx(self):

        if self.start_date > self.end_date:
            raise UserError("Start Date cannot be after End Date.")
 
        sale_orders = self.env['sale.order'].search([
            ('date_order', '>=', self.start_date),
            ('date_order', '<=', self.end_date)
        ])
 
        if not sale_orders:
            raise UserError("No sale orders found.")
 
        # Step 1: Generate XLSX in memory
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet('Sale Orders')
 
        # Header
        headers = ['Order Name', 'Customer', 'Order Date', 'Total']
        for col, header in enumerate(headers):
            worksheet.write(0, col, header) 

        # Data
        row = 1
        for order in sale_orders:
            worksheet.write(row, 0, order.name)
            worksheet.write(row, 1, order.partner_id.name)
            worksheet.write(row, 2, str(order.date_order))
            worksheet.write(row, 3, order.amount_total)
            row += 1
        workbook.close()
        output.seek(0)
 
        # Step 2: Create attachment
        file_data = output.read()
        filename = f"sale_order_report_{self.start_date}_{self.end_date}.xlsx"
        attachment = self.env['ir.attachment'].create({
            'name': filename,
            'type': 'binary',
            'datas': base64.b64encode(file_data),
            'store_fname': filename,
            'mimetype': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            'res_model': self._name,
            'res_id': self.id,
        })
 
        # Step 3: Return download URL
        return {
            'type': 'ir.actions.act_url',
            'url': f'/web/content/{attachment.id}?download=true',
            'target': 'self',
        }
 