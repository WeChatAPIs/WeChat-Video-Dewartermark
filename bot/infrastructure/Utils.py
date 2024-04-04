from __future__ import annotations

import json
import os

def is_direct_result(response: any) -> bool:
    """
    Checks if the dict contains a direct result that can be sent directly to the user
    :param response: The response value
    :return: Boolean indicating if the result is a direct result
    """
    if type(response) is not dict:
        try:
            return response.choices[0].finish_reason == 'stop'
        except:
            return False
    else:
        return response.get('direct_result', False)

def cleanup_intermediate_files(response: any):
    """
    Deletes intermediate files created by plugins
    """
    if type(response) is not dict:
        response = json.loads(response)

    result = response['direct_result']
    format = result['format']
    value = result['value']

    if format == 'path':
        if os.path.exists(value):
            os.remove(value)
