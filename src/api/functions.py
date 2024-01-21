import json


def read_from_db_lol():
    """
    This is a simulated database
    """
    with open('some_data.json', 'r') as json_data:
        return json.load(json_data)


def write_to_db_lol(command, status):
    """
    This is a simulated database
    """
    with open('some_data.json', 'r') as json_data:
        data = json.load(json_data)
        data[command] = status

    with open('some_data.json', 'w') as new_data:
        return json.dump(data, new_data)

def change_all_commands(status):
    with open('some_data.json', 'r') as json_data:
        data = json.load(json_data)
        if status == 'on':
            data = {x: True for x in data}
        elif status == 'off':
            data = {x: False for x in data}
        else:
            return


    with open('some_data.json', 'w') as new_data:
            return json.dump(data, new_data)