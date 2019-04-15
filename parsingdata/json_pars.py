import json
import sys
import json
from collections import namedtuple
import time


class Json_Pars():
    def __init__(self):
        self.commands = namedtuple('commands', 'channel_name, ts_number, invers, ts_val, ts_name, cmd')

    def main(self, json_tu):
        for i_script in range(len(json_tu['scripts'])):
            scripts = json_tu['scripts'][i_script]
            if len(scripts['steps']):
                for i_step in range(len(scripts['steps'])):
                    steps = scripts['steps'][i_step]
                    for i_cmd in range(len(steps['commands'])):
                        parsing_ts_full = steps['commands'][i_cmd]

                        # time.sleep(steps['wait'] / 100)
                        list_ts_full = parsing_ts_full['ts_full'].split(':')
                        list_ts_full.append(parsing_ts_full['cmd'])
                        tuple_commands = self.commands._make(list_ts_full)

                        yield tuple_commands


if __name__ == "__main__":
    path = sys.argv[1]
    with open(path, encoding='cp1251') as f:
        json_tu = json.load(f)
    for i_script in range(len(json_tu['scripts'])):
        scripts(json_tu['scripts'][i_script])
