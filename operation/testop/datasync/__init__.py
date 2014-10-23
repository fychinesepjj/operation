from operation.core.datasync import register
from repository.db.mongo import PushMongodbStorage
from operation.testop.datasync.adapters import PushMessageAdapter
from operation.testop.cadmin.models import PushMessage

models_register = {
    PushMessage: {'adapter': PushMessageAdapter, 'db': PushMongodbStorage, 'table': 'public'},
}


def register_sync_model(model):
    if model in models_register:
        adapter = models_register[model]['adapter']
        register(model, adapter, models_register[model])
