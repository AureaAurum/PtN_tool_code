import yaml
import re

with open(r'./translate.yaml', encoding='utf-8') as readYaml:
    yaml = yaml.load(readYaml, Loader=yaml.Loader)

with open(r'./characters.json',"rt", encoding='utf-8') as readParameter:
    parameter = readParameter.read()

with open(r'./characters.json',"wt", encoding='utf-8') as writeParameter:
    print(parameter.encode('utf-8'))

    for item in yaml['replace']:
        print(f"index:{item['index']} before:{item['before']} after:{item['after']}")
        #parameter = parameter.replace(str(item['before']),str(item['after']))
        parameter = re.sub(str(item['before']),str(item['after']),parameter)
    print(parameter.encode('utf-8'))
    writeParameter.write(parameter)