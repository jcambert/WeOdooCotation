from odoo import models, fields, api,_
from . import models as _inner_models
from ast import literal_eval as _literal_eval
import logging
import re
import math
_logger = logging.getLogger(__name__)

def literal_eval(arg):
    if isinstance(arg,bool):
        return arg
    return _literal_eval(arg)

class Model(models.AbstractModel):
    """ Main super-class for regular database-persisted Odoo models.

    Odoo models are created by inheriting from this class::

        class user(Model):
            ...

    The system will later instantiate the class once per database (on
    which the class' module is installed).
    """
    _auto = True                # automatically create database backend
    _register = False           # not visible in ORM registry, meant to be python-inherited only
    _abstract = False           # not abstract
    _transient = False          # not transient

    _models=_inner_models
    def get_param(self,key):
        return literal_eval( self.env['ir.config_parameter'].get_param(key) or False)

    def __getattr__(self,key):
        # print(key)
        if isinstance(key,str) and key in self._models:
            return self.env[self._models[key]]
        res =super().__getattr__(key)
        return res

    def map(self,fn):
        return map(fn,self)

class BaseArchive(models.AbstractModel):
    _name='base.archive.mixin'
    _description='Archive Mixin'
    active = fields.Boolean('Active',default=True)

    def do_archive(self):
        for rec in self:
            rec.active = True
class BaseSequence(models.AbstractModel):
    _name='base.sequence.mixin'
    _description='Sequence Mixin'
    sequence = fields.Integer()