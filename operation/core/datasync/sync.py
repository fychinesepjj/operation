import sys
import traceback
from django.conf import settings
from operation.core.datasync import get_adapter


def sync_obj(obj, cls, up=True, testing=False):
    table_name = 'test_table' if testing else 'table'
    adapter = get_adapter(cls)
    if table_name not in adapter.conn_ops:
        return False
    adapter.set_testing(testing)
    db_conn = adapter.conn_ops['db'](settings.MONGODB_CONF)
    update_table = adapter.conn_ops[table_name]

    #pre callback
    if hasattr(obj, 'pre_sync_callback') and callable(obj.pre_sync_callback):
        obj.pre_sync_callback(up, testing)

    to_objs = adapter.convert_to(obj)
    error_list = []
    for to_obj in to_objs:
        cond = {'pk': to_obj['pk']} if 'pk' in to_obj else {'id': to_obj['id']}
        if up and obj.published:
            try:
                db_conn.upsert_item(update_table, cond, to_obj, upsert=True)
            except:
                trace_stack = '\n'.join(traceback.format_exception(*sys.exc_info()))
                error = 'cond: %s, obj:%s, e: %s' % (cond, to_obj, trace_stack)
                error_list.append(error)
        else:
            try:
                db_conn.delete_item(update_table, cond)
            except:
                trace_stack = '\n'.join(traceback.format_exception(*sys.exc_info()))
                print 'cond: %s, e: %s' % (cond, trace_stack)
                error_list.append(error)

    has_error = bool(error_list)
    if not up or has_error or not obj.published:
        obj.sync_status = False
    else:
        obj.sync_status = True

    #post callback
    if hasattr(obj, 'post_sync_callback') and callable(obj.post_sync_callback):
        obj.post_sync_callback(up, testing)

    obj.save()
    return (not has_error, ','.join(error_list))
