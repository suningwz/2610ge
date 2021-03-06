# -*- coding: utf-8 -*-
from datetime import date, timedelta

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

class MaintenenceRims(models.Model):
    _name = 'maintenance.rims'
    _inherit = ['mail.thread']

    date = fields.Date('Fecha de Revisión', tracking=True)
    equipment_id = fields.Many2one('maintenance.equipment',string='Equipo', tracking=True)
    revision_frequency = fields.Date('Frecuencia de Revisión', tracking=True)
    marca = fields.Char('Marca', tracking=True)
    name = fields.Char(tracking=True)
    modelo = fields.Char('Modelo', tracking=True)
    no_serie = fields.Char('No Serie', tracking=True)
    medida = fields.Char('Medida', tracking=True)
    tipo_renovado = fields.Char('Tipo Renovado', tracking=True)
    mil_orig = fields.Char('Milimetros Orig', tracking=True)
    mil_act = fields.Char('Milimetros Act', tracking=True)
    presion = fields.Char('Presion', tracking=True)
    km_acum = fields.Float('Kms Acumulados', tracking=True)
    user_id = fields.Many2one('res.users', string='Responsable', default=lambda self: self.env.uid, tracking=True)
    current_state = fields.Selection([('n', 'Nueva'),('r', 'Renovada')], string='Estado actual', tracking=True)
    company_id = fields.Many2one('res.company', string='Compañia', default=lambda self: self.env.company)
    position = fields.Integer(string="Posición", tracking=True)

    @api.model
    def find_and_execute_alerts(self):
        records = self.env['maintenance.rims'].search()
        for record in records:
            if record.date == date.today() - timedelta(days=1):
                # send Today Alert
                record.action_send_email()
                msg = """ Fecha de revisión próxima: Mañana """
                record.message_post(body=msg)

    def action_send_email_alert_rims(self):
        self.ensure_one()
        template_id = self.env.ref("rims_maintenance.email_alert_template")
        ctx = {
            'email_to': self.user_id.email,
            'email_from': self.env.user.company_id.email,
            'send_email': True,
            'attendee': self.user_id.name
        }
        template_id.with_context(ctx).send_mail(self.id, force_send=True, raise_exeption=False)

    

class MaintenanceEquipment(models.Model):
    _inherit = 'maintenance.equipment'


    maintenance_rims_count = fields.Integer(compute='_compute_maintenance_rims_count', string="Maintenance Count Rims", store=True)
    maintenance_rims_ids = fields.One2many('maintenance.rims','equipment_id', copy=False)
    
    tu_list = [
        ('tracto', 'Tractocamion'),
        ('gon2', 'Gondola 2 ejes'),
        ('gon3', 'Gondola 3 ejes'),
        ('tan2', 'Tanque 2 ejes'),
        ('tan3', 'Tanque 3 ejes'),
        ('lowboy', 'Low boy'),
        ('volteo', 'Volteo'),
        ('pipa', 'Pipa'),
        ('platf', 'Plataforma'),
        ('dolly2', 'Dolly 2 ejes'),
    ]
    tipo_unidad = fields.Selection(tu_list, string='Tipo de unidad')

    aseguradora = fields.Char('Aseguradora')
    no_poliza = fields.Char('No. Póliza')
    periodo = fields.Char('Periodo')
    
    marca = fields.Char('Marca')
    placas = fields.Char('Placas')
    color = fields.Char('Color')
    linea_tipo = fields.Char('Tipo / Línea')
    cilindros = fields.Integer('No. Cilindros')
    no_eco = fields.Char('No. Económico')
    no_motor = fields.Char('No. Motor')
    
    @api.depends('maintenance_rims_ids')
    def _compute_maintenance_rims_count(self):
        lista = []
        for item in self.maintenance_rims_ids:
            lista.append(item)
        self.maintenance_rims_count = len(lista)

    def action_view_rims(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "res_model": "maintenance.rims",
            "views": [
                [self.env.ref("rims_maintenance.maintenance_rims_tree").id, "tree"],
                [self.env.ref("rims_maintenance.maintenance_rims_form").id, "form"]
            ],
            "domain": [('equipment_id', '=', self.id)],
        }
