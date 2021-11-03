from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.shortcuts import render, get_object_or_404
from .models import BronxMember, Transaction, StockItem
import requests


def main(request):
    # For the main view
    template = loader.get_template('index.html')
    response = requests.get('https://api.whatdoestrumpthink.com/api/v1/quotes/random').json()
    members = BronxMember.objects.order_by('-beer_outstanding').all()

    context = {"trump_quote": response["message"], "member_info": members,
               "member_ids": [member.id for member in members]}

    return HttpResponse(template.render(context, request))


def ledger_info(request):
    if request.is_ajax and request.method == "GET":  # In case of GET request: get number of beers outstanding
        member = get_object_or_404(BronxMember, pk=request.GET['member_id'])

        recent_transactions = list(Transaction.objects.filter(member=member).order_by("-stamp")[:5])
        data = {
            "beer_outstanding": member.beer_outstanding,
            "name": f"{member.firstName} {member.lastName}",
            "daily": member.daily,
            "weekly": member.weekly,
            "monthly": member.monthly,
            "recent": recent_transactions,
        }

    return JsonResponse(data)

def adjust_ledger(request):
    # Check whether this is the proper request
    if request.is_ajax and request.method == "POST":  # In case of POST request: change number of beers outstanding
        # Get the correct member from database
        member = get_object_or_404(BronxMember, pk=request.POST['member_id'])

        # Add/subtract the required number of beers
        transaction_amount = int(request.POST['amount'])
        if transaction_amount > 0:
            out = False
        else:
            out = True

        member.beer_outstanding += transaction_amount

        # Create new transaction
        Transaction.objects.create(member=member, item=StockItem.objects.get(name="Beer"),
                                   qty=abs(transaction_amount), out=out)

        # Save the database entry
        member.save()

        data = {
            "beer_outstanding": member.beer_outstanding
        }


    return JsonResponse(data)


