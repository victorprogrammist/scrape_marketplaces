
import coms.coms
import sys
import json
import os

def read_params_from_file(file_parameters = None):

    def get_arg(idx, default = None):
        if idx < len(sys.argv):
            return sys.argv[idx]
        return default

    #*******************************************************************

    if not file_parameters:
        file_parameters = get_arg(1, 'parameters.json')

    file_parameters = coms.coms.get_filename_for_read(file_parameters)

    if not os.path.isfile(file_parameters):
        coms.coms.logmsg(f'file not found: {file_parameters}')
        parameters = {}
    else:
        try:
            with open(file_parameters, 'r', encoding='utf-8-sig') as f:
                parameters = json.load(f)
        except:
            coms.coms.logmsg(f'error in json: {file_parameters}')
            return None

    #*******************************************************************

    dest_filename = parameters.get('dest_filename', None)
    if dest_filename is None:
        dest_filename = f"result-{coms.coms.date_time_str()}.json"

    parameters['dest_filename'] = coms.coms.get_filename_for_store(dest_filename)

    #*******************************************************************

    expected_count_items = parameters.get('expected_count_items', 3)
    expected_count_items = coms.coms.only_numbers(expected_count_items)
    if not expected_count_items:
        expected_count_items = 10

    parameters['expected_count_items'] = expected_count_items

    #*******************************************************************

    valid_parameters = [
        'dest_filename',
        'search_string',
        'url_category',
        'min_price',
        'max_price',
        'sorting',
        'expected_count_items'
        ]

    for k,v in parameters.items():
        coms.coms.logmsg(f'parameter {k}: {v}')
        if not k in valid_parameters:
            coms.coms.logmsg(f'WRONG PARAMETER: {k}')

    #*******************************************************************

    return parameters




