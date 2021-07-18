from flask import Flask
import json
from lxml import etree

app = Flask(__name__)

config_values = []

@app.route("/")
def hello_world():
    GetConfigValues()
    return "<p>Hello, {}</p>".format(config_values[0]['description'])

@app.route("/change/<int:config_id>")
def change_value(config_id):
    GetConfigValues()
    current_config = next((item for item in config_values if item['id'] == config_id), None)

    if current_config['value'] == 'true':
        new_value = 'false'
    else:
        new_value = 'true'
    

    element = etree.parse(current_config['filepath'])
    root = element.getroot()
    e = root.find(current_config['xpath'])
    e.attrib[current_config['value_attribute']] = new_value
    with open(current_config['filepath'], 'wb') as f:
        write_value = etree.tostring(root, pretty_print=True)
        f.write(str.encode('<?xml version="1.0" encoding="UTF-8" ?>'))
        f.write(write_value)

    return new_value


def GetConfigValues():
    config_values.clear()
    with open('webapi.config') as f:
        config_file = json.load(f)
    
    for config in config_file:
        value = {}
        value['description'] = config['description']
        value['value'] = GetConfigValue(config['filepath'], config['xpath'], config['value_attribute'])
        value['id'] = config['id']
        value['xpath'] = config['xpath']
        value['filepath'] = config['filepath']
        value['value_attribute'] = config['value_attribute']
        config_values.append(value)

def GetConfigValue(filepath, xpath, attribute):
    element = etree.parse(filepath)
    root = element.getroot()
    e = root.find(xpath)
    return e.attrib[attribute]