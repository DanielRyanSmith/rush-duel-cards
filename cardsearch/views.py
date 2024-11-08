from django.shortcuts import render
from django.http import HttpResponse

from cardsearch.models import Card

def index(request):
    q = request.GET.get('q') 
    name = request.GET.get('name')
    level = request.GET.get('level')
    attack = request.GET.get('attack')
    defense = request.GET.get('defense')
    attribute = request.GET.get('attribute')
    monter_type = request.GET.get('mtype')
    card_type = request.GET.get('ctype')
    card_status = request.GET.get('status')

    cards = Card.objects.all().prefetch_related('monster_types')
    if q:
        cards = cards.filter(
            text__contains=q)
    if name:
        cards = cards.filter(name__iexact=name)
    if level:
        cards = cards.filter(monster_level=int(level))
    if attack:
        cards = cards.filter(monster_attack=int(attack))
    if defense:
        cards = cards.filter(monster_defense=int(defense))
    if attribute:
        cards = cards.filter(monster_attribute__iexact=attribute)
    if monter_type:
        cards = cards.filter(monster_types__name__contains=monter_type)
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
    return render(request, "cardsearch/index.html", context)

def search(request):
    return HttpResponse("search results.")

def advanced(request):
    return HttpResponse("advanced search.")