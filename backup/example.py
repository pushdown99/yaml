# -*- coding: utf-8 -*-
import yaml
import io

# Define data
data = {
    'a list': [
        1, 
        42, 
        3.141, 
        1337, 
        'help', 
        u'€'
    ],
    'a string': 'bla',
    'another dict': {
        'foo': 'bar',
        'key': 'value',
        'the answer': 42
    }
}

with io.open('command.yaml', 'w', encoding='utf8') as istream:
    yaml.dump(data, istream, default_flow_style=False, allow_unicode=True)

with open("command.yaml", 'r') as ostream:
    try:
        dict = yaml.safe_load(ostream) 
        print(dict)
    except yaml.YAMLError as exc:
        print(exc)
