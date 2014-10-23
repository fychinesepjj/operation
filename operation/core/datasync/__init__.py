import logging

logger = logging.getLogger('core')
_ADAPTERS = {}


class AlreadyRegistered(Exception):
    pass


class NotRegistered(Exception):
    pass


def register(model, adapter_class, conn_options):    # only register non-proxy model
    try:
        if model in _ADAPTERS:
            return False

        _ADAPTERS[model] = adapter_class(conn_options)
    except AlreadyRegistered:
        logger.exception('register adapter FAILED, model: %s, adapter_class: %s' % (model, adapter_class))
        return False
    finally:
        return True


def get_adapter(model):
    if model._meta.proxy:     # only support one level proxy class
        model = model.__bases__[0]    # only get first parent class, ignore multi-inherited
    if model not in _ADAPTERS:
        raise NotRegistered('The model %s is not registered' % model.__name__)
    return _ADAPTERS[model]


class ModelAdapter(object):
    _in_testing = False

    def __init__(self, conn_ops):
        self.conn_ops = conn_ops

    def set_testing(self, status):
        self._in_testing = status

    def convert_to(self, from_model):
        pass

    def convert_from(self, to_model, data):
        pass
