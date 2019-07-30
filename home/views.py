from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from .models import Item, Choice, Users
from manageTables.models import ActiveTables, Customer, Server
from manageInventory.models import Inventory
from operationsResearch.models import BillHistory
#from django.template import loader
from django.http import Http404
from django.shortcuts import get_object_or_404, render
from findIngredients import totalIngredientConsumption
from .forms import SearchUserForm
import csv
import random
#
#simpler way of doing index function with 'render', but really only saves one line of code
#it automatically sends an HttpResponse
#
#def index(request):
#   item_list = Item.objects.all()
#   context = {'item_list':item_list}
#   return render(request, 'home/index.html',context)

def index(request):
    item_list = Item.objects.order_by('item_id')
    context = {'item_list':item_list,}
    return render(request, 'home/index.html', context)

def menu(request):
    item_list = Item.objects.order_by('item_id')
    context = {'item_list':item_list,}
    return render(request, 'home/menu.html', context)

def detail(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    return render(request, 'home/detail.html', {'item':item})
    #return render(request, 'home/detail.html', {'item':item})

def results(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    choice_history = Choice.objects.all()
    return render(request, 'home/results.html', {'item':item,'choice_history':choice_history})

def purchase(request, item_id):
    if request.method == 'POST':
        item = get_object_or_404(Item, pk=item_id)
        try:
            quantity_text = request.POST['textfield']
            choice_quantity = int(quantity_text)
        except(KeyError, Choice.DoesNotExist):
            return render(request, 'home/detail.html',{'item':item,'error_message':"You didn't select a choice.",})
        else:
            item.choice_set.create(quantity=choice_quantity,date=timezone.now())
            return HttpResponseRedirect(reverse('home:results', args=(item.id,)))
    else:
        return HttpResponseRedirect(reverse('home:detail', args=(item.id,)))

# Create your views here.

def populateFoodElf(request):
    names = []
    servers = []

    with open("names.csv") as f:
        count = 0
        reader = csv.reader(f, delimiter=',', quotechar='"')
        for row in reader:
            if row:
                names.append(row[1])
                if len(names) > 1000:
                    break
    for i in Inventory.objects.all():   #add stock to all ingredients
        setattr(i,"units",10000)
        i.save()

    with open("bill_history.txt","a") as history:
        for count in range(100):
            print(f'day {count}')
            numTables = random.randint(5,15)
            days_ago = 100 - count
            for i in range(numTables):
                chars = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
                code = ""
                for i in range(8):
                    code += chars[random.randint(0,35)]
                #################################################################################
                _server_ = random.choice(list(Server.objects.all()))
                tableInst = ActiveTables(server=_server_,time=timezone.now(),ACCESS=code)
                tableInst.save()
                for j in range(random.randint(2,6)):
                    tableInst.customer_set.create(name=random.choice(names))
                for person in tableInst.customer_set.all():
                    for numChoices in range(random.randint(1,3)):
                        person.choice_set.create(item=random.choice(list(Item.objects.all())),
                                                 quantity=1, table=tableInst,date=timezone.now())
                ###################################################################################
                custom_str = ""
                item_list = []
                history.write(40 * "=" + "\n")
                for i in tableInst.customer_set.all():
                    custom_str += f' {i.name}'
                history.write("Customers: "+ custom_str + "\n")
                for j in tableInst.choice_set.all():
                    item_list.append(j.item.item_id)
                    history.write(f'{j.item.item_id} - {j.item.item_name} - ${j.item.price} - {j.customer.name}\n')
                    consumption_dict = totalIngredientConsumption(j.item.ingredients)
                    for ingredient_name in consumption_dict:
                        field_name = 'units'
                        obj = Inventory.objects.get(name=ingredient_name)
                        field_value = getattr(obj,field_name)
                        field_value = field_value - consumption_dict[ingredient_name]
                        setattr(obj,field_name,field_value)
                        obj.save()

                minutes = random.randint(35,75)
                date_of_bill = timezone.now() + timezone.timedelta(days=-days_ago, hours=random.randint(2,18))
                BillHistory.objects.create(server=tableInst.server,customers=custom_str,items=str(item_list),date=date_of_bill,time_seated = minutes)
                tableInst.choice_set.all().delete()
                tableInst.customer_set.all().delete()
                tableInst.delete()

    return HttpResponseRedirect(reverse('home:index', args=()))

#def sqlInjectionTutorial(request):
#    searchForm = SearchUserForm()
#    return render(request,'home/searchUsers.html',{'searchForm':searchForm})
#def showUser(request):
#    form = SearchUserForm(request.POST or None)
#    if request.method == "POST" and form.is_valid():
    #    email = form.cleaned_data['email']
    #    password = form.cleaned_data['password']
    #    user_list = Users.objects.raw("select * from home_users where email = '%s' and password = '%s'" % (email,password,))
    #    newForm = SearchUserForm()
    #    return render(request,'home/searchUsers.html',{'searchForm':newForm,'user_list':user_list})
