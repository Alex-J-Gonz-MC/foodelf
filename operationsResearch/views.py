from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.utils import timezone
from home.models import Item, Choice
from manageTables.models import Customer, ActiveTables, Server
from manageInventory.models import Inventory
from .models import BillHistory
from findIngredients import totalIngredientConsumption
import ast

def index(request):
    bills = list(BillHistory.objects.all().order_by('date'))
    profit = []
    item_count = {}
    dates = []
    item_sales = {}
    bill_count = 0
    ingredient_count = {}
    for item in Item.objects.all():
        item_count.update({item.item_name:0})
    for inv in Inventory.objects.all():
        ingredient_count.update({inv.name:0})        
    
    for bill in bills:
        if bill_count > 100:
            break
        for item_id in ast.literal_eval(bill.items):
            item_production_cost = 0.0
            item_gross_revenue = 0.0
            item = Item.objects.get(pk=item_id)
            item_count[item.item_name] += 1
            consumption_dict = totalIngredientConsumption(item.ingredients)
            item_gross_revenue += item.price
            for ingred in consumption_dict:
                ingredient = Inventory.objects.get(name=ingred)
                ingredient_count[ingred] += consumption_dict[ingred]
                item_production_cost += ingredient.price_per_unit * consumption_dict[ingred]
                
        dates.append(str(bill.date))
        profit.append(abs(item_gross_revenue - item_production_cost))
        bill_count += 1
        
    
    tablesID = []
    cost = []
    for table in ActiveTables.objects.all():
        tablesID.append(table.id)
        cost_for_table = 0.0
        for choice in table.choice_set.all():
            cost_for_table += choice.item.price
        cost.append(cost_for_table)
    
    date_prof = zip(dates,profit)
    data_list = []    
    for i,j in date_prof:
        data_list.append({'x':i,'y':j})
 
    context = {"items":list(item_count.keys()),"counts":list(item_count.values()),
               "dates":dates,"profits":profit,"tables":tablesID,"costs":cost,
               "data_list":data_list,"date_prof":date_prof,"ingreds":list(ingredient_count.keys()),
               "ingred_counts":list(ingredient_count.values())}
    return render(request,'index.html',context)

def billHistory(request):
    bills = list(BillHistory.objects.all())
    return render(request,'billHistory.html',{"bills":bills})
