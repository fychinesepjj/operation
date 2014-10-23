from repository.db.mongo.base import MongodbStorage, IncrementalId


class PushMongodbStorage(MongodbStorage):

    db_name = "test"

    def __init__(self, conn_str):
        super(PushMongodbStorage, self).__init__(conn_str, self.db_name)
        self._ids = IncrementalId(self._db)
