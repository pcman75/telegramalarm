import os, json, requests

def getSensorName(friendlyName):
    name = friendlyName.replace(' ', '_').replace('.0', '').replace('-', '').replace('<','less').lower()
    return 'binary_sensor.' + name


def triggerSensor(name, state, message, logger):
    headers = {
        'Authorization': f'Bearer {os.environ["SUPERVISOR_TOKEN"]}',
        "content-type": "application/json"
    }

    entity = {
        "state": state,
        "attributes": {
            "friendly_name": name, #"Alarma M 6.0 - 7.0",
            "message": message
        }
    }
    response = requests.post(f'http://supervisor/core/api/states/{getSensorName(name)}', headers=headers, json = entity)
    logger.debug(response)
    return response.ok