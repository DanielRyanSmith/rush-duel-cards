from django.shortcuts import render
from functools import reduce
from operator import and_

from django.db.models import Q
from django.shortcuts import render

from cardsearch.models import Card

def index(request):
    if not request.GET.urlencode():
        return advanced(request)
    q = request.GET.get('q')
    name = request.GET.get('name')
    level = request.GET.get('level')
    attack = request.GET.get('attack')
    defense = request.GET.get('defense')
    attribute = request.GET.get('attribute')
    monster_type = request.GET.get('mtype')
    card_type = request.GET.get('ctype')
    card_status = request.GET.get('status')

    cards = Card.objects.all().prefetch_related('monster_types')
    if q:
        cards = cards.filter(text__contains=q)
    if name:
        cards = cards.filter(name__contains=name)
    if level:
        cards = cards.filter(monster_level=int(level))
    if attack:
        cards = cards.filter(monster_attack=int(attack))
    if defense:
        cards = cards.filter(monster_defense=int(defense))
    if attribute:
        cards = cards.filter(monster_attribute__iexact=attribute)
    if monster_type:
        cards = cards.filter(monster_types__name__contains=monster_type)
    if card_type:
        cards = cards.filter(card_type__iexact=card_type)
    if card_status:
        cards = cards.filter(status__iexact=card_status)

    # cards = Card.objects.filter(card_type='Monster', effect=None).order_by('monster_attack').prefetch_related('monster_types')
    cards_info = []
    for card in cards:
        cards_info.append({
            'card': card,
            'monster_types': ' / '.join(
                [str(mt) for mt in card.monster_types.all()])
        })
    context = {
        "cards_info": cards_info,
    }
    return render(request, "cardsearch/results.html", context)

def _filter_cards(request, cards):
    """
    Applies filters to the Card queryset based on POST data.
    """
    # A mapping from POST keys to their corresponding ORM lookup.
    # This approach is scalable and avoids repetitive if-statements.
    filter_map = {
        'name': 'name__icontains',
        'level': 'monster_level',
        'attack': 'monster_attack',
        'defense': 'monster_defense',
        'attribute': 'monster_attribute__iexact',
        'card-type': 'card_type__iexact',
        'card-status': 'status__iexact',
    }
    
    # Dynamically build a dictionary of filters.
    filters = {}
    for key, lookup in filter_map.items():
        value = request.POST.get(key)
        if value:
            # Safely handle integer conversions
            if key in ['level', 'attack', 'defense']:
                if value.isdigit():
                    filters[lookup] = int(value)
            else:
                filters[lookup] = value

    # Apply all collected simple filters at once.
    if filters:
        cards = cards.filter(**filters)

    # --- Handle complex text searches ---
    # Combine text searches using Q objects for clarity.
    # This finds cards where the text contains all provided snippets.
    text_searches = [
        Q(text__icontains=request.POST.get(key))
        for key in ['card-text', 'requirement', 'effect'] if request.POST.get(key)
    ]
    if text_searches:
        # Use reduce with the 'and_' operator to chain the filters.
        cards = cards.filter(reduce(and_, text_searches))

    # --- Handle Many-to-Many relationship for monster types ---
    monster_types = request.POST.get('monster-types')
    if monster_types:
        # Create a Q object for each monster type to chain them with AND.
        # This ensures the card has all the specified monster types.
        type_queries = [
            Q(monster_types__name__icontains=mtype.strip())
            for mtype in monster_types.split(',')
        ]
        if type_queries:
            # The '*' unpacks the list of Q objects into individual arguments.
            cards = cards.filter(*type_queries)
            
    # Using .distinct() to avoid duplicate results when filtering on
    # many-to-many relationships.
    return cards.distinct()


def search(request):
    """
    Handles the search form submission and displays results.
    """
    if request.method == 'GET':
        return render(request, 'cardsearch/form.html')

    # For POST requests, filter and display the results.
    # prefetch_related is great for optimizing access to related objects.
    cards = Card.objects.prefetch_related('monster_types')
    filtered_cards = _filter_cards(request, cards)

    context = {
        "cards_info": filtered_cards,
    }
    
    return render(request, "cardsearch/results.html", context)

def search_results(request):
    return render(request, 'form.html')

def advanced(request):
    return render(request, 'cardsearch/advanced.html')