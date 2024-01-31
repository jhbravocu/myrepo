# -*- coding: utf-8 -*-

# from odoo import models, fields, api


def pago_guardar(self, vals):
    voucher_obj = self.env['account.payment']
    invoices_input = []
    op = vals['op'] or False
    ctx = dict(self._context)
    ctx.update({'op': op})
    # if self.env['account.move'].browse(vals['active_ids']).filtered(lambda x: x.pending_available_op_amount == 0):
    #     raise exceptions.ValidationError(_('Existen línea(s) seleccionada(s) pagada(s) totalmente.'))
    for invoice in self.env['account.move'].browse(vals['active_ids']):
        if not False:
            invoice.write({'pago_aprobado': True, 'cuenta_bancaria_id': self.cuenta_bancaria_id.id,
                           'fecha_aprobacion': self.fecha_aprobacion})
            fund_origin_journal = invoice.get_fund_origin_journal()
            fund_origin_journal = fund_origin_journal.id if fund_origin_journal else 'None'
            invoices_input.append(('%s-%s-%s' %
                                   (invoice.currency_id.id, invoice.partner_id.id, fund_origin_journal),
                                   invoice.id))

            voucher_id = voucher_obj.search([('invoice_id', '=', invoice.id)])
            for vh in voucher_id:
                if vh.state not in ('cancel', 'confirm'):
                    vh.sudo().with_context(ctx).proforma_voucher_auxiliary()
                    vh.write({'fecha_aprobacion_pago': self.fecha_aprobacion})

                vh.move_ids.write({'operating_unit_id': vh.operating_unit_id.id})

            # for voucher in voucher_id:
            #     for move in voucher.move_ids:
            #         move.write({'operating_unit_id': voucher.operating_unit_id.id})

            # voucher_id.sudo().with_context(ctx).proforma_voucher_auxiliary()
            # voucher_id.write({'fecha_aprobacion_pago': self.fecha_aprobacion})

            is_configure_parameter = self.env['ir.config_parameter'].sudo().get_param('grp.visulizar_documentos_para_OP_otras_uo')
            operating_unit_id = False
            for voucher in voucher_id:
                default_operating_unit_id = voucher.operating_unit_id.id
                if is_configure_parameter == '1':
                    if voucher.solicitud_viatico_id:
                        operating_unit_id = voucher.solicitud_viatico_id.department_service_id.operating_unit_id.id
                    if voucher.rendicion_viaticos_id:
                        operating_unit_id = voucher.rendicion_viaticos_id.department_service_id.operating_unit_id.id
                    if voucher.solicitud_anticipos_id:
                        operating_unit_id = voucher.solicitud_anticipos_id.uo_id_presta_servicio.operating_unit_id.id
                    if voucher.rendicion_anticipos_id:
                        operating_unit_id = voucher.rendicion_anticipos_id.uo_id_presta_servicio.operating_unit_id.id
                voucher.move_ids.write({'operating_unit_id': default_operating_unit_id if not operating_unit_id else operating_unit_id})
        # elif invoice.pago_aprobado:
        #     raise exceptions.ValidationError(_('Ya existen línea/s con aprobación de pago.'))
    invoice_grouped = voucher_obj.group_docs_to_pay(invoices_input, 0)
    # self.generate_orden_pago(invoice_grouped)
    ctx = dict(self._context)
    ctx.update({'cuenta_bancaria_id': self.cuenta_bancaria_id})
    voucher_obj.with_context(ctx).generate_orden_pago(invoice_grouped)
    return {'type': 'ir.actions.act_window_close'}
