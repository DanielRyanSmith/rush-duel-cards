from django.shortcuts import render
from functools import reduce
from operator import and_

from django.db.models import Q
from django.shortcuts import render

from cardsearch.models import Card

def index(request):
    return search(request)

def _filter_cards(request, cards):
    """
    Applies filters to the Card queryset based on POST data.
    """
    # A mapping for simple, direct filters.
    filter_map = {
        'name': 'name__icontains',
        'attribute': 'monster_attribute__iexact',
        'card-type': 'card_type__iexact',
        'card-status': 'status__iexact',
    }

    filters = {}
    for key, lookup in filter_map.items():
        value = request.POST.get(key)
        if value:
            filters[lookup] = value
    
    if filters:
        cards = cards.filter(**filters)

    # --- Handle numeric comparisons ---
    # These fields can have operators like 'gt', 'gte', 'lt', 'lte'.
    comparison_fields = ['level', 'attack', 'defense']
    for field in comparison_fields:
        value = request.POST.get(field)
        operator = request.POST.get(f'{field}-op', 'exact') # Default to exact match
        if value and value.isdigit():
            lookup = f'monster_{field}__{operator}'
            cards = cards.filter(**{lookup: int(value)})

    # --- Handle complex text searches ---
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
            Q(monster_types__name__contains=mtype.strip())
            for mtype in monster_types.split(',')
        ]
        for tq in type_queries:
            cards = cards.filter(tq)
            
    # Using .distinct() to avoid duplicate results when filtering on
    # many-to-many relationships.
    return cards.distinct()


def search(request):
    """
    Handles the search form submission and displays results.
    """
    if request.method == 'GET':
        # If the form is submitted via GET, or on initial load, show the form.
        return render(request, 'cardsearch/landing.html')

    # For POST requests, filter and display the results.
    # Get the sorting parameter from the URL, default to 'name'
    sort_by = request.GET.get('sort', 'name')

    # Apply filtering from your _filter_cards function
    cards = Card.objects.prefetch_related('monster_types')
    filtered_cards = _filter_cards(request, cards)

    # Apply sorting to the filtered queryset
    sorted_cards = filtered_cards.order_by(sort_by)

    context = {
        "cards": sorted_cards,
        "current_sort": sort_by,
        "sort_options": {
            "name": "Name",
            "card_type": "Card Type",
            "monster_level": "Level",
            "monster_attack": "Attack",
            "monster_defense": "Defense",
        },
    }
    
    return render(request, "cardsearch/results.html", context)

def search_results(request):
    return render(request, 'landing.html')

def advanced(request):
    return render(request, 'cardsearch/advanced.html')