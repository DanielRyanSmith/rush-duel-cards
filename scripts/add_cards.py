import json
from cardsearch.models import Card

# python manage.py runscript add_cards
def run():
    with open('all_cards.json', 'r') as f:
        cards_file = json.load(f)
        for card_info in cards_file['cards']:
            # Skip cards that have unknown (unreleased) info.
            if card_info.get('monster_level') == '???':
                continue
            attack = (int(card_info['monster_attack'])
                      if 'monster_attack' in card_info else None)
            defense = (int(card_info['monster_defense'])
                       if 'monster_defense' in card_info else None)
            level = (int(card_info['monster_level'])
                       if 'monster_level' in card_info else None)
            card = Card(
                name=card_info['card_name'],
                card_type=card_info['card_type'],
                card_property=card_info.get('card_property'),
                status=card_info['card_status'],
                image_url=card_info['image_url'],
                japanese_name=card_info['japanese_name'],
                text=card_info['card_text'],
                effect_type=card_info.get('effect_type'),
                effect=card_info.get('card_effect'),
                additional_text=card_info.get('additional_text'),
                requirement=card_info.get('card_requirement'),

                monster_attribute=card_info.get('monster_attribute'),
                monster_attack=attack,
                monster_defense=defense,
                monster_level=level,
            )
            card.save()
            if 'monster_types' in card_info:
                for monster_type in card_info['monster_types']:
                    card.monstertype_set.create(name=monster_type)
            card.save()
