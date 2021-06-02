def get_list_item(list, index, default):
    item = None

    try:
        item = list[index]
    except IndexError:
        print('returning empty string as index {} is out of bound of list {}'.format(index, list))
        item = default

    return item

def get_value_from_dict(dict, key, default):
    try:
        value = dict[key]
    except KeyError:
        print('value with {} is not found in {}'.format(key, dict))
        value = default

    return value