#! -*- coding:utf-8 -*-
import logging
logger = logging.getLogger('operation')

'''
from operation.core.datasync import ModelAdapter
class TestAdapter(ModelAdapter):
    def convert_to(self, from_model):
        result_dict = []
        app_infos = {
            'id': from_model.id,
            'name': from_model.name,
            'content': from_model.content,
        }
        result_dict.append(app_infos)
        return result_dict
'''