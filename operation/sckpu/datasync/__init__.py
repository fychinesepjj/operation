from operation.core.datasync import register
#from repository.db.mongo import TestMongodbStorage
#from operation.testop.datasync.adapters import TestAdapter
#from operation.testop.cadmin.models import TestModel

models_register = {
    #TestModel: {'adapter': TestAdapter, 'db': TestMongodbStorage, 'table': 'public'},
}

def register_sync_model(model):
    if model in models_register:
        adapter = models_register[model]['adapter']
        register(model, adapter, models_register[model])
