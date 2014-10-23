import logging
import datetime
from bson.son import SON
from functools import wraps
from pymongo.cursor import Cursor
from pymongo import ReplicaSetConnection, ReadPreference, Connection
from pymongo import DESCENDING, ASCENDING

logger = logging.getLogger('core')


def set_default_order(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'order' not in kwargs or kwargs['order'] is None:
            kwargs['order'] = args[0].DEFAULT_ORDER
        return func(*args, **kwargs)
    return wrapper


def cursor_to_list(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        retval = func(*args, **kwargs)
        if isinstance(retval, Cursor):
            retval = [x for x in retval]
        elif isinstance(retval, dict) and 'results' in retval and 'total' in retval:
            if isinstance(retval['results'], Cursor):
                retval['results'] = [x for x in retval['results']]
        return retval
    return wrapper


class IncrementalId(object):
    """implement incremental id for collection in mongodb
    """
    def __init__(self, db):
        self.db = db
        self.colls = {}

    def _ensure_next_id(self, coll_name):
        """ensure next_id item in collection ,if not, next_id method will throw exception rasie by pymongo"""
        cond = {'_id': coll_name}
        id_info = self.db.ids.find_one(cond)
        if not id_info:
            self.db.ids.insert({'_id': coll_name, 'seq': 1L})

    def next_id(self, coll):
        """get next increment id and increase it """
        if coll not in self.colls:
            self._ensure_next_id(coll)
        cond = {'_id': coll}
        update = {'$inc': {'seq': 1L}}
        son = SON([('findandmodify', 'ids'), ('query', cond), ('update', update), ('new', True)])
        seq = self.db.command(son)
        return seq['value']['seq']


class MongodbStorage(object):
    _db = None
    _conn = None
    ORDER_DESC = DESCENDING
    ORDER_ASC = ASCENDING
    DEFAULT_ORDER = [("order", ORDER_ASC)]

    def __init__(self, conn_str, db_name):
        try:
            if conn_str.find("replicaSet") == -1:
                _conn = Connection(
                    conn_str,
                    max_pool_size=30,
                    safe=True,
                    read_preference=ReadPreference.SECONDARY_ONLY)
            else:
                _conn = ReplicaSetConnection(
                    conn_str,
                    max_pool_size=30,
                    safe=True,
                    read_preference=ReadPreference.SECONDARY_ONLY)
            self._db = _conn[db_name]
            self._conn = _conn
        except Exception, e:
            logger.exception('Can not connect to mongodb: %s', e)
            raise e

    def delete_item(self, table, cond):
        eval('self._db.%s.remove(%s)' % (table, cond))

    def upsert_item(self, table, cond, item, upsert=False, multi=False):
        eval("self._db.%s.update(%s, {'$set': %s}, upsert=%s, multi=%s)" % (table, cond, item, upsert, multi))

EPOCH = datetime.datetime(1970, 1, 1)


def total_seconds(delta):
    """return total seconds of a time delta."""
    if not isinstance(delta, datetime.timedelta):
        raise TypeError('delta must be a datetime.timedelta.')
    return delta.days * 86400 + delta.seconds + delta.microseconds / 1000000.0


def datetime2timestamp(dt, convert_to_utc=False):
    '''
    Converts a datetime object to UNIX timestamp in milliseconds.
    '''
    if isinstance(dt, datetime.datetime):
        if convert_to_utc:
            dt = dt + datetime.timedelta(hours=-8)
        timestamp = total_seconds(dt - EPOCH)
        return long(timestamp)
    return dt


def timestamp2datetime(timestamp, convert_to_local=False):
    '''
    Converts UNIX timestamp to a datetime object.
    '''
    if isinstance(timestamp, (int, long, float)):
        dt = datetime.datetime.utcfromtimestamp(timestamp)
        if convert_to_local:
            dt = dt + datetime.timedelta(hours=8)
        return dt
    return timestamp


def timestamp_utc_now():
    return datetime2timestamp(datetime.datetime.utcnow())


def timestamp_now():
    return datetime2timestamp(datetime.datetime.now())
