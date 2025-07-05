import json
import urllib
from bs4 import BeautifulSoup as bs


def main():
    with open('all_cards.json', 'r') as f:
        cards_json = json.load(f)
        existing_cards = cards_json['cards']
        current_page = cards_json.get('next_page', '')
        if not current_page:
            current_page = 'https://yugipedia.com/wiki/Category:Rush_Duel_cards'
    all_cards = []
    soup = create_parser(current_page)
    eles = soup.find_all('a')
    card_urls = []
    for ele in eles:
        curr = ele
        if curr.parent.name == 'li':
            curr = ele.parent
        else:
            continue
        if curr.parent.name == 'ul':
            curr = curr.parent
        else:
            continue
        classes = curr.parent.attrs.get('class')
        class_to_compare = classes[0] if classes and len(classes) > 0 else ''
        if curr.parent.name == 'div' and class_to_compare == 'mw-category-group':
            path = ele.attrs['href']
            card_urls.append(f'https://yugipedia.com{path}')
    all_cards.extend(parse_cards(card_urls))
    next_page = ''
    for ele in eles:
        if ele.string == 'next page':
            path = ele.attrs['href']
            next_page = f'https://yugipedia.com{path}'
            break

    cards_dict = {}
    for card in existing_cards:
        cards_dict[card['card_name']] = card
    # Create or replace all new entries.
    for card in all_cards:
        cards_dict[card['card_name']] = card
    cards_to_write = [card for card in cards_dict.values()]
    with open('all_cards.json', 'w') as f:
        f.write(json.dumps({'cards': cards_to_write, 'next_page': next_page}))


def get_content(url):
    req = urllib.request.Request(url)
    req.add_header(
        'User-Agent',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:106.0) Gecko/20100101 Firefox/106.0',
    )
    req.add_header(
        'Accept',
        'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    )
    req.add_header('Accept-Language', 'en-US,en;q=0.5')

    return urllib.request.urlopen(req).read().decode('utf-8')


def create_parser(url):
    content = get_content(url)
    return bs(content, 'html.parser')


def parse_cards(card_urls):
    formatted_cards = []
    for card_url in card_urls:
        card_info = parse_card(card_url)
        if card_info is not None:
            formatted_cards.append(card_info)
    return formatted_cards


def parse_card(card_url):
    try:
        soup = create_parser(card_url)
        info = {'url': card_url}
        info['card_type'] = soup.find(
            'a', {'title': 'Card type'}
        ).parent.next_sibling.next_sibling.text.strip()
        if info['card_type'] == 'Monster':
            info['monster_types'] = (
                soup.find('a', {'title': 'Type'})
                .parent.next_sibling.next_sibling.text.strip()
                .split(' / ')
            )
            info['monster_attribute'] = (
                soup.find('a', {'title': 'Attribute'})
                .parent.next_sibling.next_sibling.contents[1]
                .text
            )
            info['monster_level'] = (
                soup.find('a', {'title': 'Level'})
                .parent.next_sibling.next_sibling.contents[1]
                .text
            )
            info['monster_attack'] = (
                soup.find('a', {'title': 'ATK'})
                .parent.next_sibling.next_sibling.contents[1]
                .text
            )
            info['monster_defense'] = (
                soup.find('a', {'title': 'DEF'})
                .parent.next_sibling.next_sibling.contents[3]
                .text
            )
        else:
            info['card_property'] = soup.find(
                'a', {'title': 'Property'}
            ).parent.next_sibling.next_sibling.text.strip()
        info['card_name'] = soup.find(class_='card-table').find('div').find('div').text
        info['japanese_name'] = (
            soup.find(class_='card-table')
            .contents[3]
            .contents[0]
            .contents[1]
            .contents[6]
            .text
        )
        info['card_status'] = (
            soup.find('a', {'title': 'Status'})
            .parent.next_sibling.next_sibling.contents[1]
            .text.split(' ')[0]
        )
        info['image_url'] = (
            soup.find(class_='cardtable-main_image-wrapper')
            .contents[0]
            .contents[0]
            .attrs['src']
        )
        info['card_text'] = soup.find(class_='lore').text.strip()
        if info['card_type'] != 'Monster' or 'Effect' in info['monster_types']:
            text_parts = info['card_text'].split('[REQUIREMENT]')
            effect_type = 'Effect'
            effect_separator = '[EFFECT]'
            if '[CONTINUOUS EFFECT]' in info['card_text']:
                effect_type = 'ContinuousEffect'
                effect_separator = '[CONTINUOUS EFFECT]'
            elif '[MULTI-CHOICE EFFECT]' in info['card_text']:
                effect_type = 'MultiChoiceEffect'
                effect_separator = '[MULTI-CHOICE EFFECT]'
            info['effect_type'] = effect_type
            info['additional_text'] = text_parts[0].strip()
            card_requirement, card_effect = text_parts[1].split(effect_separator)
            info['card_requirement'] = card_requirement.strip()
            info['card_effect'] = card_effect.strip()
    except Exception as e:
        print('FAILED (', e, ')', card_url)
        return None
    return info


if __name__ == '__main__':
    main()
