from django import forms
from manageInventory.models import Inventory
from django.utils.safestring import mark_safe
unique_ingredients = {'bacon': 1, 'egg': 2, 'cheese': 3, 'roll': 4, 'sausage': 5, 'ham': 6, 'steak': 7, 'hashbrown': 8, 'hero': 9, 
                      'homefries': 10, 'toast': 11, 'roastbeef': 12, 'onion': 13, 'pepper': 14, 'tomato': 15, 'mushroom': 16, 'eggwhite': 17, 'turkeybacon': 18, 
                      'avocado': 19, 'spinach': 20, 'pancake': 21, 'frenchtoast': 22, 'waffles': 23, 'bagel': 24, 'creamcheese': 25, 'jelly': 26, 'butter': 27}
prices = [2.00, 3.00, 4.00, 5.00, 6.00, 7.00, 8.00]

    
class PreferenceForm(forms.Form):
    highPrice = forms.CharField(label="Price Range", max_length = 4)
    highCal = forms.CharField(label="Calorie Range", max_length=3)
    ingredient = forms.CharField(label="Preffered Ingredient", max_length = 20)
    
class EditInventoryForm(forms.Form):
    name = forms.CharField(label="Name", max_length = 50)
    units = forms.CharField(label="Units", max_length = 10,required=False, disabled=True)
    price_per_unit = forms.CharField(label="Price Per Unit", max_length = 50)
    safety_stock = forms.CharField(label="Safety Stock", max_length = 10)
    date_purchased = forms.CharField(label="Date Purchased",required=False,  disabled=True)
    
    #def __init__(self):
        #self.cleaned_data["name"] = ""
        #self.cleaned_data["units"] = ""
        #self.cleaned_data["price_per_unit"] = ""
        #self.cleaned_data["safety_stock"] = ""
        #self.cleaned_data["date_purchased"] = ""        
        
    def prefill(self, ingred_id):
        ingred = Inventory.objects.get(pk=ingred_id)
        
        self.cleaned_data["name"] = ingred.name
        self.cleaned_data["units"] = str(ingred.units)
        self.cleaned_data["price_per_unit"] = str(ingred.price_per_unit)
        self.cleaned_data["safety_stock"] = str(ingred.safety_stock)
        self.cleaned_data["date_purchased"] = str(ingred.date_purchased)

class AddStockForm(forms.Form):
    units = forms.CharField(label="Number of Units to Add to Inventory", max_length=10)
        
