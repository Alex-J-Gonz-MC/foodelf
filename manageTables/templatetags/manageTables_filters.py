from django.template.library import Library
from home.models import Choice
from manageTables.models import Customer

register = Library()

@register.filter
def getChoices(customer):
    choice_list = []
    for choice in customer.choice_set.all():
        choice_list.append(choice)
    return choice_list

@register.filter
def calculateTotal(customer):
    total = 0.0
    for choice in customer.choice_set.all():
        total += choice.item.price
    return total