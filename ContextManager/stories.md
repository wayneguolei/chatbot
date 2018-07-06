## greet
* greeting
    - utter_greet

## happy
* thanks
    - utter_youarewelcome

## goodbye
* goodbye
    - utter_goodbye

## venue_search
* get_paylib
    - action_get_paylib
    - slot{"entity_month": "april", "entity_month_number": "04"}

## concert_search
* dayoff_create
    - action_dayoff_create
    - slot{"entity_day_number": "4", "entity_year_number": "2018", "entity_dayoff": "cp"}

## compare_reviews_venues
* ask_day
    - utter_ask_day

## compare_reviews_concerts
* ask_month
    - utter_ask_cp_type

## compare_reviews_concerts
* ask_cp_type
    - utter_ask_cp_type
    - action_dayoff_create
