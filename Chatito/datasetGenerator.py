# from core import rasaGenerator
# from random import randint
#
# def generate_data_set(workplace, size_per_class=10):
#     rasa_generatror = rasaGenerator
#     self._get_alias()
#     self._get_entities()
#     self._get_actions()
#     samples = []
#     for action in self.actions:
#         if action == '%[get_paylib]':
#             examples = self.actions[action]
#             nb_examples = len(examples)
#             while True:
#                 example_index = randint(0, nb_examples - 1)
#                 text = ''
#                 intent = re.findall(r'(?<=%\[).+(?=\])', action)[0]
#                 sample = {'intent': intent, 'entities': []}
#                 element_list = []
#                 index = 0
#                 for element_name in re.split('(%s|%s)' % (self.regex_alias_name, self.regex_entity_name),
#                                              examples[example_index]):
#                     if re.match(self.regex_alias_name, element_name):
#                         value = self.get_element(element_name)
#                         text += value
#                         index += len(value)
#                     elif re.match(self.regex_entity_name, element_name):
#                         value = self.get_element(element_name)
#                         entity = {'value': value, 'start': index, 'end': index + len(value) - 1,
#                                   'entity': re.findall(r'(?<=@\[).+(?=\])', element_name)[0]}
#                         sample['entities'].append(entity)
#
#                         text += value
#                         index += len(value)
#                         element_list.append(self.get_element(element_name))
#                     else:
#                         element_list.append(element_name)
#                         text += element_name
#                         index += len(element_name)
#                 sample['text'] = text
#                 samples.append(sample)
#                 if len(samples) >= size_per_class:
#                     break
#     return samples