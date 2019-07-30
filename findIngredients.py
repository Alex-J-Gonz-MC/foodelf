import csv

def shownames():
    with open("names.csv") as f:
     count = 0
     reader = csv.reader(f, delimiter=',', quotechar='"')
     for row in reader:
        if row:
            name=row[1]
            print(name)
            count+=1
            if count > 5000:
                break
        
def findIngredient(x):
    jasper = open('jdelinventory.csv')
    jasper_file = csv.reader(jasper)

    for row in jasper_file:
        ingredients = row[4].split("-")
        itemNameWithSpace = row[1].split("_")
        cheese_list = []
        if any(x in i for i in ingredients):
            cheese_list.append(itemNameWithSpace)
            print(cheese_list)
    print("done with finding ingredients... %s" % (x))

def getAllUniqueIngredients(ingred):
    ingredients_list = []
    amount = []
    ingredients = ingred.split(",")
    for unique in ingredients:
        food_str = ""
        num_str = ""
        for i in unique:
            if i.isdigit():
                num_str += i
            elif i != '\"' and i != ':':
                food_str += i
        ingredients_list.append(food_str)
        amount.append(int(num_str))
        #print(f'Ingredient: {food_str}\tAmount: {num_str}')
    return ingredients_list, amount

def totalIngredientConsumption(ingred):
    ingredient, amount = getAllUniqueIngredients(ingred)
    consumption_dict = {}
    used_ingredients = []
    #print(ingredient)
    #print(amount)
    for i in range(len(ingredient)):
        #print(ingredient[i],amount[i])
        #if any(ingredient[i] in j for j in used_ingredients):
        #    consumption_dict[ingredient[i]] += amount[i]
        #else:
            consumption_dict.update({ingredient[i]:amount[i]})
        #    used_ingredients.append(ingredient[i])
    #print(consumption_dict)
    return consumption_dict

#ingredients_dict = {}
#getAllUniqueIngredients()
#print(totalIngredientConsumption("Shrimp:6,Rice Noodles:4,Spicy Cabbage Slaw:3,Cucumber:5,Shallots:6,Romaine:12,Cabbage:6,Cilantro:5"))
#shownames()
