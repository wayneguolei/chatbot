from utils import DataSetConfiguration
from os import listdir
from os.path import isfile, join
from random import randint
import re
import json
import datetime


def generate_data_set(workplace, rule_file, size_per_class=5000):
    rasa_generatror = DataSetConfiguration(workplace)
    conf_files = [join(workplace, f) for f in listdir(workplace) if isfile(join(workplace, f)) and join(workplace, f) != rule_file and '.json' not in f]
    for f in conf_files:
        rasa_generatror.get_alias(f)
        rasa_generatror.get_entities(f)
        rasa_generatror.get_actions(f)
        rasa_generatror.get_entity_synonyms(f)
    rasa_generatror.get_actions(rule_file)
    rasa_generatror.get_alias(rule_file)
    rasa_generatror.get_entities(rule_file)
    rasa_generatror.get_entity_synonyms(rule_file)
    samples = []
    for action in rasa_generatror.actions:
        nb_sample = 0
        rules = rasa_generatror.actions[action]
        nb_rules = len(rules)
        while True:
            rule_index = randint(0, nb_rules - 1)
            text = ''
            intent = re.findall(r'(?<=%\[).+(?=\])', action)[0]
            sample = {'intent': intent, 'entities': []}
            element_list = []
            index = 0
            for element_name in re.split('(%s|%s)' % (rasa_generatror.regex_alias_name,
                                                      rasa_generatror.regex_entity_name),
                                         rules[rule_index]):
                if re.match(rasa_generatror.regex_alias_name, element_name):
                    value = rasa_generatror.get_element(element_name)
                    text += value
                    index += len(value)
                elif re.match(rasa_generatror.regex_entity_name, element_name):
                    value = rasa_generatror.get_element(element_name)
                    entity = {'value': value, 'start': index, 'end': index + len(value),
                              'entity': re.findall(r'(?<=@\[).+(?=\])', element_name)[0]}
                    sample['entities'].append(entity)
                    text += value
                    index += len(value)
                    element_list.append(rasa_generatror.get_element(element_name))
                else:
                    element_list.append(element_name)
                    text += element_name
                    index += len(element_name)
            sample['text'] = text
            samples.append(sample)
            nb_sample += 1
            if nb_sample >= size_per_class:
                break
    training_data = {'rasa_nlu_data': {'regex_features': [], 'entity_synonyms': rasa_generatror.entity_synonyms, 'common_examples': samples}}
    dt_now = datetime.datetime.now()
    with open('%s/rasa_training_%s.json' % (workplace, dt_now.strftime("%Y%m%d%H%M%S")), 'w') as fp:
        json.dump(training_data, fp, indent=2, ensure_ascii=False)


if __name__ == '__main__':
    work_place = 'data'
    generate_data_set(workplace=work_place, rule_file='%s/example_data_generator.txt' % work_place)
