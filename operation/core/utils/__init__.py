try:
    from django.contrib.auth.models import User
    username_field = 'username'
    from operation.core.customs.site import custom_site as site
except Exception as e:
    import traceback
    import sys
    traceback.print_exc(file=sys.stdout)
    from django.contrib.admin import site


def semicolon_spliter(full_str, delimiter='\n'):
    splited_dict = {}
    if not full_str:
        return splited_dict
    full_str_list = full_str.split(delimiter)
    for line in full_str_list:
        splited_key_value = line.split(':')
        if len(splited_key_value) == 2:
            key, value = splited_key_value
            key = key.strip()
            value = value.strip()
            splited_dict[key] = value
    return splited_dict


def semicolon_join(str_dict, delimiter='\n'):
    temp_list = []
    for k, v in str_dict.iteritems():
        org_line = '%s:%s' % (k, v)
        temp_list.append(org_line)
    return '\n'.join(temp_list)


def str_to_list(string, delimiter=','):
    return_list = []
    if not string:
        return return_list
    splited_list = string.split(delimiter)
    for item in splited_list:
        item = item.strip()
        if item:
            return_list.append(item)
    return return_list
