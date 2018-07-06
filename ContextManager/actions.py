from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from rasa_core.actions.action import Action


class ActionCreateDayOff(Action):
    def name(self):
        return 'action_dayoff_create'

    def run(self, dispatcher, tracker, domain):
        type_dayoff = tracker.get_slot("entity_dayoff")
        entity_year_number = tracker.get_slot("entity_year_number")
        if not entity_year_number:
            entity_year_number = "2018"
        entity_day_number = tracker.get_slot("entity_day_number")
        entity_month_number = tracker.get_slot("entity_month_number")
        if not entity_month_number:
            entity_month = tracker.get_slot("entity_month")
            dispatcher.utter_message("vos congés du type %s le %s %s %s a été créés" % (type_dayoff, entity_day_number,
                                                                                        entity_month,entity_year_number))
        else:
            dispatcher.utter_message("vos congés du type %s de %s-%s-%s a été créés" % (type_dayoff, entity_day_number,
                                                                                        entity_month_number,
                                                                                        entity_year_number))
        return []


class ActionGetPaylib(Action):
    def name(self):
        return 'action_get_paylib'

    def run(self, dispatcher, tracker, domain):
        entity_month_number = tracker.get_slot("entity_month_number")
        dispatcher.utter_message("Ci-joint votre bulletin de salire du mois %s" % entity_month_number)
        return []
