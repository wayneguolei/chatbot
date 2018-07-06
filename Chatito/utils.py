import re
import random
from codecs import open


class DataSetConfiguration(object):

    def __init__(self, filename):
        self.filename = filename
        self.regex_alias_name = r'~\[.+?\]'
        self.regex_entity_name = r'@\[.+?\]'
        self.regex_action_name = r'%\[.+?\]'
        self.regex_text = r'(?!= +)[^\s-]+.*(?=\r)'
        self.actions = {}
        self.entities = {}
        self.alias = {}
        self.entity_synonyms = []

    def get_alias(self, filename):
        with open(filename, 'r', 'utf8') as f:
            alias_name = ''
            for l in f:
                if re.match(r'^'+self.regex_alias_name+r'(?=\r\n)', l):
                    alias_name = re.findall(self.regex_alias_name, l)[0]
                    if alias_name not in self.alias:
                        self.alias[alias_name] = []
                elif l == '\r\n':
                    alias_name = ''
                elif alias_name != '':
                    text = re.findall(self.regex_text, l)[0]
                    self.alias[alias_name].append(text)

    def get_entities(self, filename):
        with open(filename, 'r', 'utf8') as f:
            entity_name = ''
            for l in f:
                if re.match(r'^'+self.regex_entity_name+r'(?=\r\n)', l):
                    entity_name = re.findall(self.regex_entity_name, l)[0]
                    if entity_name not in self.entities:
                        self.entities[entity_name] = []
                elif l == '\r\n':
                    entity_name = ''
                elif entity_name != '':
                    text = re.findall(self.regex_text, l)[0]
                    if text in self.alias:
                        for alias in self.alias[text]:
                            self.entities[entity_name].append(alias)
                    else:
                        self.entities[entity_name].append(text)

    def get_entity_synonyms(self, filename):
        with open(filename, 'r', 'utf8') as f:
            entity_synonyms = {}
            entity_name = ''
            for l in f:
                if re.match(r'^' + self.regex_entity_name + r'(?=\r\n)', l):
                    entity_name = re.findall(r'(?<=@\[).+(?=\])', l)[0]
                elif l == '\r\n':
                    entity_name = ''
                elif entity_name != '':
                    text = re.findall(self.regex_text, l)[0]
                    if text in self.alias:
                        entity_value = re.findall(r'(?<=~\[).+(?=\])', l)[0]
                        entity_synonyms[entity_value] = []
                        for alias in self.alias[text]:
                            entity_synonyms[entity_value].append(alias)
            self.entity_synonyms.extend([{'value': entity, 'synonyms': entity_synonyms[entity]}
                                         for entity in entity_synonyms])

    def get_actions(self, filename):
        with open(filename, 'r', 'utf8') as f:
            action_name = ''
            for l in f:
                if re.match(r'^'+self.regex_action_name+r'(?=\r\n)', l):
                    action_name = re.findall(self.regex_action_name, l)[0]
                    if action_name not in self.actions:
                        self.actions[action_name] = []
                elif l == '\r\n':
                    action_name = ''
                elif action_name != '':
                    text = re.findall(self.regex_text, l)[0]
                    self.actions[action_name].append(text)

    def get_element(self, element_name):
        if element_name == '@[entity_integer]':
            return str(random.randint(0, 255))
        elif element_name == '@[entity_number]':
            i = random.randint(0, 30)
            if random.randint(0, 100) <= 30:
                i += 0.5
                if random.randint(0, 100) <= 90:
                    i = str(i).replace('.', ',')
            return str(i)
        elif element_name == '@[entity_month_number]':
            month_number = str(random.randint(1, 12))
            if len(month_number) < 2:
                if random.randint(1, 100) <= 50:
                    return month_number.zfill(2)
            return month_number
        elif element_name == '@[entity_day_number]':
            day_number = str(random.randint(1, 31))
            if len(day_number) < 2:
                if random.randint(1, 100) <= 50:
                    return day_number.zfill(2)
            return day_number
        elif element_name == '@[entity_year_number]':
            return str(random.randint(1990, 2025))
        else:
            if element_name[0] == '~':
                values = self.alias[element_name]
            elif element_name[0] == '@':
                values = self.entities[element_name]
            else:
                raise ValueError
            return random.choice(values)

