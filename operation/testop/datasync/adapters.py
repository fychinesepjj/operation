#! -*- coding:utf-8 -*-
import logging
from operation.core.datasync import ModelAdapter
logger = logging.getLogger('operation')


class PushMessageAdapter(ModelAdapter):
    def convert_to(self, from_model):
        result_dict = []
        app_infos = {
            'id': from_model.id,
            'name': from_model.name,
            'content': from_model.content,
        }
        result_dict.append(app_infos)
        return result_dict
