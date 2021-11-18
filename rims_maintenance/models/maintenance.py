# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError

class MaintenenceRims(models.Model):
    _name = 'maintenance.rims'

    date = fields.Date('Fecha de Revisión')
    equipment_id = fields.Many2one('maintenance.equipment',string='Equipo')
    revision_frequency = fields.Date('Frecuencia de Revisión')
    marca = fields.Char('Marca')
    name = fields.Char()
    modelo = fields.Char('Modelo')
    no_serie = fields.Char('No Serie')
    medida = fields.Char('Medida')
    tipo_renovado = fields.Char('Tipo Renovado')
    mil_orig = fields.Char('Milimetros Orig')
    mil_act = fields.Char('Milimetros Act')
    presion = fields.Char('Presion')
    km_acum = fields.Float('Kms Acumulados')
    user_id = fields.Many2one('res.users', string='Responsable',tracking=True, default=lambda self: self.env.uid)
    current_state = fields.Selection([('n', 'Nueva'),('r', 'Renovada')], string='Estado actual')
    company_id = fields.Many2one('res.company', string='Compañia', default=lambda self: self.env.company)
    position = fields.Integer(string="Posición")

    

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
