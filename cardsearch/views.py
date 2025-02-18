from django.shortcuts import render
from django.http import HttpResponse

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
    name = request.POST.get('name', None)
    level = request.POST.get('level', None)
    attack = request.POST.get('attack', None)
    defense = request.POST.get('defense', None)
    attribute = request.POST.get('attribute', None)
    card_type = request.POST.get('card-type', None)
    card_status = request.POST.get('card-status', None)
    monster_types = request.POST.get('monster-types', None)

    card_text = request.POST.get('card-text', None)
    requirement = request.POST.get('requirement', None)
    effect = request.POST.get('effect', None)

    if name:
        cards = cards.filter(name__contains=name)
    if card_text:
        cards = cards.filter(text__contains=card_text)
    if requirement:
        cards = cards.filter(text__contains=requirement)
    if effect:
        cards = cards.filter(text__contains=effect)
    if level:
        cards = cards.filter(monster_level=int(level))
    if attack:
        cards = cards.filter(monster_attack=int(attack))
    if defense:
        cards = cards.filter(monster_defense=int(defense))
    if attribute:
        cards = cards.filter(monster_attribute__iexact=attribute)
    if monster_types:
        formatted_monster_types = monster_types.split(',')
        for mtype in formatted_monster_types:
            cards = cards.filter(monster_types__name__contains=mtype.strip())
    if card_type:
        cards = cards.filter(card_type__iexact=card_type)
    if card_status:
        cards = cards.filter(status__iexact=card_status)
    return cards

def search(request):
    if request.method == 'GET':
        return render(request, 'cardsearch/form.html', {})
    if request.method == 'POST':
        cards = Card.objects.all().prefetch_related('monster_types')
        cards = _filter_cards(request, cards)
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
        html = render(request, "cardsearch/results.html", context)
        return HttpResponse(html)

def search_results(request):
    return render(request, 'form.html')

def advanced(request):
    return render(request, 'cardsearch/advanced.html')