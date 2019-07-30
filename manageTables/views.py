from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.utils import timezone
from home.models import Item, Choice
from .models import Customer, ActiveTables, Server
from manageInventory.models import Inventory
from operationsResearch.models import BillHistory
#from django.template import loader
from django.http import Http404
from django.shortcuts import get_object_or_404, render
from .forms import NewTableForm
##======================================
from django.views.decorators.csrf import csrf_exempt
import queue
import json
from findIngredients import totalIngredientConsumption, getAllUniqueIngredients
# Create your views here.

wait_queue = {} #wait list as dict so we can update with dict.update()
                #queue.Queue(maxsize=10)


def index(request):
    table_list = ActiveTables.objects.order_by('id')
    form = NewTableForm()
    wait_list = []
    json_queue = json.loads(json.dumps(wait_queue))
    print(json_queue)
    for i in json_queue:
        wait_list.append(json_queue[i]["Username"])
    print(get_client_ip(request))
    context = {'table_list':table_list,'form':form,'queue':wait_list}
    return render(request, 'tableView.html', context)

def summary(request, table_id):
    table = get_object_or_404(ActiveTables, pk=table_id)
    ordered_items = []
    subtotal = 0.0
    customer_list=[]
    choice_list = []
    menu_list = Item.objects.order_by('item_id')
    print(table.choice_set.all())
    for c in table.customer_set.all():
        print(c.choice_set.all().values_list('id',flat=True).order_by('id'))
    for customer in table.customer_set.all():
        customer_list.append(customer)
        for choice in customer.choice_set.all():
            print(f'customer set: {choice}')
            ordered_items.append(choice.item)
            choice_list.append(choice)
   
    for choice in table.choice_set.all(): 
            if any(choice.id in c.choice_set.all().values_list('id',flat=True).order_by('id') 
                   for c in table.customer_set.all()):
                continue
            else:
                print(f'table set: {choice}')
                ordered_items.append(choice.item)
                choice_list.append(choice)
                
            
    for p in ordered_items:
        subtotal += p.price
        
    context = {'ordered_items':ordered_items,'subtotal':subtotal,'table_id':table_id,'customer_list':customer_list,
               'menu_list':menu_list,'c_list_index':len(customer_list),'choice_and_item':zip(ordered_items,choice_list)}
    return render(request, 'summary.html',context)

def updateCustomers(request):
    customer_list=[]
    increment = int(request.GET['append_index'])
    table_id = int(request.GET['table_id'])
    table = get_object_or_404(ActiveTables, pk=table_id)
    print("start")
    for customer in table.customer_set.all():#.order_by('id'):#[increment:]:
        #if increment < len(table.customer_set.all()):
        customer_list.append(customer)
        increment += 1
    print("end")
    context = {'table_id':table_id,'customer_list':customer_list,'index':increment}
    return render(request,'updateCustomerList.html',context)

def sendToMenu(request, table_id):
    item_list = Item.objects.order_by('item_id')
    table = get_object_or_404(ActiveTables, pk=table_id)
    context = {'item_list':item_list, 'table':table}
    return render(request, 'menu.html', context)

def addItemToBill(request, table_id, item_id):
    table = get_object_or_404(ActiveTables, pk=table_id)
    table.choice_set.create(item=Item.objects.get(pk=item_id), quantity=1, date=timezone.now())
    return HttpResponseRedirect(reverse('manageTables:summary', args=(table_id,)))

def createTable(request):
    if request.method =='POST':
        form = NewTableForm(request.POST)
        if form.is_valid():
            server_name = form.cleaned_data['server_name']
            table_number = form.cleaned_data['table_number']
            host_name = form.cleaned_data['host_name']
            wait_list_index = ""
            _id_ = ""
            #json_queue = json.loads(json.dumps(wait_queue))
            for i in wait_queue:
                if host_name == wait_queue[i]["Username"]:
                    wait_list_index = i
                    _id_ = wait_queue[i]["ID"]
            del wait_queue[wait_list_index]
            try:
                newTable = ActiveTables.objects.create(tableNumber=int(table_number),server=Server.objects.get(name=server_name),ACCESS=_id_,time=timezone.now())
                Customer.objects.create(table=newTable,name=host_name)
            except(KeyError, Server.DoesNotExist):
                return render(request, 'tableView.html',{'error_message':"Server Does not exist.",})     
            return HttpResponseRedirect(reverse('manageTables:index', args=()))

def closeoutTable(request,table_id):
    table = get_object_or_404(ActiveTables, pk=table_id)
    custom_str = ""
    item_list = []
    with open("bill_history.txt","a") as history:
        history.write(40 * "=" + "\n")
        for i in table.customer_set.all():
            custom_str += f' {i.name}'
        history.write("Customers: "+ custom_str + "\n")
        for j in table.choice_set.all():
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
    time_spent_seated = timezone.now() - table.time
    minutes = time_spent_seated.seconds / 60
    BillHistory.objects.create(server=table.server,customers=custom_str,items=str(item_list),date=table.time,time_seated = minutes)
    table.choice_set.all().delete()
    table.customer_set.all().delete()
    table.delete()
    
    return HttpResponseRedirect(reverse('manageTables:index', args=()))

def splitBills(request,table_id):
    table = get_object_or_404(ActiveTables, pk=table_id)
    customers = []
    for person in table.customer_set.all():
        customers.append(person)
    context = {"customers":customers,"table_id":table_id}
    return render(request,"splitBills.html",context)

@csrf_exempt
def assignChoices(request):
    if request.method == "POST":
        data = json.loads(request.body.decode('UTF-8'))
        access_code = data['Access_Code']
        userID = int(data['UserID'])
        table = ActiveTables.objects.get(ACCESS=access_code)
        person = table.customer_set.get(pk=userID)
        for i in data['Choices']:
            for j in table.choice_set.all():
                print(j.id)
                if j.item.item_name == i and j.customer is None:
                    person.choice_set.add(j)
                    print(f'added {j}')
                    break
                elif j.customer is not None:
                    continue
        for k in table.choice_set.all():
            if k.customer is not None:
                print(f'{k.customer.name} - {k.item.item_name}')
        return HttpResponse("Choices were assigned")
            

@csrf_exempt
def updateQueue(request):
    if request.method == "GET":
        return JsonResponse(json.loads(json.dumps(wait_queue)))#,safe=False)
    elif request.method == "POST":
        print(json.loads(request.body.decode('UTF-8')))
        wait_queue.update({(f'Customer{len(wait_queue)}'):dict(json.loads(request.body.decode('UTF-8')))})
        return HttpResponse("Data was input into Queue")

@csrf_exempt
def inputToTable(request,access_code):
    if request.method == "POST":
        data = json.loads(request.body.decode('UTF-8'))
        table = data['table']
        print(f'These cutomers were put into table {table}')
        cust = Customer.objects.create(table=ActiveTables.objects.get(ACCESS=access_code),name=customer["Username"])
        print(f'{customer["Username"]}\n')
        return JsonResponse({"UserID":cust.id})
    
def lobby(request,access_code):
    if request.method == "GET":
        people_at_table = []
        table = get_object_or_404(ActiveTables,ACCESS=access_code)
        for i in table.customer_set.all():
            person = {"Username":i.name}
            people_at_table.append(person)
        json_dict = {"Customers":people_at_table}
        return JsonResponse(json.loads(json.dumps(json_dict)))
    
def get_client_ip(request):
    ip = request.META.get('REMOTE_ADDR')
    return ip

def getAccessCode(request,customer_id):
    code = ""
    hosts = []
    for table in ActiveTables.objects.all():
            if  table.ACCESS == customer_id:
                code = table.ACCESS
                print(table.customer_set.all())
                for host in table.customer_set.all():
                    hosts.append(host.id)
                    print("we got customer id")
                return JsonResponse({"access_code":code,"UserID":hosts[0]})
    return JsonResponse({})

def getBill(request,access_code):
    table = get_object_or_404(ActiveTables,ACCESS=access_code)
    json_dict = {}
    items_at_table = []
    for choices in table.choice_set.all():
        item = {"Name":choices.item.item_name,"Price":choices.item.price}
        items_at_table.append(item)
    json_dict = {"Items":items_at_table}
    return JsonResponse(json.loads(json.dumps(json_dict)))

def showBill(request,userID):
    customer = Customer.objects.get(pk=userID)
    items_for_customer = []
    for choices in customer.choice_set.all():
        item = {"Name":choices.item.item_name,"Price":choices.item.price}
        items_for_customer.append(item)
    json_dict = {"Items":items_for_customer}
    return JsonResponse(json.loads(json.dumps(json_dict)))

@csrf_exempt
def personalizedMenu(request):
    if request.method == "POST":
        preferences = json.loads(request.body.decode('UTF-8'))
        price = float(preferences['Price'])
        calories = int(preferences['Calories'])
        ingredient = preferences['Ingredient']
        json_array = []
        for item in Item.objects.all():
            if price-2.0 <= item.price <= price+2.0:
                if calories-100 < item.calories < calories+100:
                    ingredients, amounts = getAllUniqueIngredients(item.ingredients)
                    for ingred in ingredients:
                        if ingred == ingredient:
                            json_array.append({"Name":item.item_name,"Calories":item.calories,
                                               "Price":item.price,"Ingredients":ingredients})
                
        return JsonResponse({"Preferences":json_array})
    
def getIngredients(request):
    if request.method == "GET":
        ingred_list = []
        ingreds = Inventory.objects.all()
        for inv in ingreds:
            name = {"Name":inv.name}
            ingred_list.append(name)
        json_dict = {"Ingredients":ingred_list}
        return JsonResponse(json.loads(json.dumps(json_dict)))