from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
#from django.template import loader
from django.http import Http404, JsonResponse, HttpResponseServerError
from django.shortcuts import get_object_or_404, render
# Create your views here.
from .models import Inventory
from .forms import PreferenceForm,EditInventoryForm, AddStockForm
from home.models import Item
###############################################################
from django.views.decorators.csrf import csrf_exempt
from keras import models
import numpy as np
from keras.utils import to_categorical
import os
import random
import json
###############################################################

def inventoryMain(request):
    inventory = Inventory.objects.all()
    formList = []
    editForm = EditInventoryForm()
    stockForm = AddStockForm()
    context = {"inventory":inventory,"editForm":editForm,"stockForm":stockForm}
    return render(request,"mainInventory.html",context)

def preferencesForm(request):
    form = PreferenceForm()
    context = {"form":form}
    return render(request,"detail.html",context)

def prefOut(request):
    if request.method =='POST':
        form = PreferenceForm(request.POST)
        if form.is_valid():
            price = form.cleaned_data['highPrice']
            cal = form.cleaned_data['highCal']
            ing = form.cleaned_data['ingredient']
            ##################LOAD MODEL AND WEIGHTS#####################
            #load json and create model
            json_file_dir = os.path.dirname(__file__)  # get current directory
            file_path = os.path.join(json_file_dir, 'model.json')
            
            json_file = open(file_path,'r')
            loaded_model_json = json_file.read()
            json_file.close()
            loaded_model = models.model_from_json(loaded_model_json)
            
            #load weights into new model
            weights_path = os.path.join(json_file_dir, 'weights.h5')
            loaded_model.load_weights(weights_path)
            
            
            ####################EVALUATE MODEL###########################
            #Evaluate model on test data
            loaded_model.compile(loss='categorical_crossentropy', # Cross-entropy
                            optimizer='rmsprop', # Root Mean Square Propagation
                            metrics=['accuracy']) # Accuracy performance metric
            
            x = []
            y = []
            y_items = []
            
            for i in range(-1,2):
                for j in range(-50,100,50):
                    x.append([(float(price)+(i*1.0))/8.00,(int(cal)+ j)/1500,int(ing)])
            x = np.array(x)
            output = loaded_model.predict(x)
            
            for out in output:
                max_output = -1.00
                output_itemID = -1                
                for i in range(len(out)):
                    if out[i] > max_output:
                        max_output = out[i]
                        output_itemID = i
                output_itemID+=1
                y.append(output_itemID)
            y = set(y)  #turns into a set of only unique elements
            y = list(y) #turn back into a list
            
            for id_of_item in y:
                y_items.append(Item.objects.get(pk=id_of_item))
            
            context = {"output":y_items}
            return render(request,"netOutput.html",context)
        
def testComms(request):
    if request.method == "GET":
        num = random.randint(100,500)
        num = str(num)
        char = random.choice(["A","B","C","D","E","F"])
        code = char + num
        return HttpResponse(code,content_type="text/plain")
    
def testJSON(request):
    if request.method == "GET":
        json_dict = {}
        for item in list(Item.objects.all()):
            json_dict.update({(f'Item {item.id}'):{
                              "Item Name":item.item_name,
                              "Price":item.price,
                              "Ingredients":item.ingredients}})
               
        return JsonResponse(json_dict)

@csrf_exempt
def testPOST(request):
    #if request.is_ajax():
        #if request.method == "POST":
            #print(f'Raw Data: {request.body}')
    if request.method == "POST":
        #json_data = json.loads(request.body) # request.raw_post_data w/ Django < 1.4
        try:
            #data = json_data['data']
            print(json.loads(request.body.decode('UTF-8')))
        except KeyError:
            return HttpResponseServerError("Malformed data!")   
    return JsonResponse({"Hey Cutie!":"I got your data"})

def populateForm(request):
    if request.method == "GET":
        ingred_id = int(request.GET['ingred_id'])
        print(ingred_id)
        item = Inventory.objects.get(pk=ingred_id)
        data = {'name':item.name,'units':str(item.units),
                'price_per_unit':str(item.price_per_unit),
                'safety_stock':str(item.safety_stock),
                'date_purchased':str(item.date_purchased)}
        editForm = EditInventoryForm(data,initial=data)
        return render(request,'prepopulatedForm.html',{'editForm':editForm,'ingred_id':ingred_id})

def editInventory(request,ingred_id):
    form = EditInventoryForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
            name = form.cleaned_data['name']
            price_per_unit = float(form.cleaned_data['price_per_unit'])
            safety_stock = int(form.cleaned_data['safety_stock'])
            obj = Inventory.objects.get(pk=ingred_id)
            setattr(obj,'name',name)
            setattr(obj,'price_per_unit',price_per_unit)
            setattr(obj,'safety_stock',safety_stock)
            obj.save()
            print(f'{obj.name} {obj.price_per_unit} {obj.safety_stock}')
    return HttpResponseRedirect(reverse('manageInventory:inventoryMain',args=()))


def getAddStockForm(request):
    if request.method == "GET":
        ingred_id = int(request.GET['ingred_id'])
        obj = Inventory.objects.get(pk=ingred_id)
        stockForm = AddStockForm()
        return render(request,'getAddStockForm.html',{'stockForm':stockForm,'ingred_id':ingred_id,"ingred_name":obj.name})

def addStock(request,ingred_id):
    form = AddStockForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        total_units = 0
        ingredient = Inventory.objects.get(pk=ingred_id)
        units = int(form.cleaned_data['units'])
        total_units += ingredient.units
        total_units += units
        setattr(ingredient,'units',total_units)
        ingredient.save()
    return HttpResponseRedirect(reverse('manageInventory:inventoryMain',args=()))
    