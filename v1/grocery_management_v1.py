# Grocery Management System 
Store=[
    {"item":"milk","price":25,"amount":150},
    {"item":"cereal","price":10,"amount":115},
    {"item":"chips","price":50,"amount":120},
    {"item":"water","price":20,"amount":185},
    {"item":"coffee","price":45,"amount":120},
    {"item":"egg","price":7,"amount":970},
    {"item":"bread","price":30,"amount":230}
]
# Function to view all the available items in the store
def show_store():
    print("Store : ")
    for product in Store:
        print(product['item'],'-',product['price'])
        # To check the amount of the products in the store
    a=input("Do you want to check the stock of these item?(yes/no) ")
    if a.lower()=='yes':
        look_store()
    
# Function to view about a specific item in the store (used chat gpt)
def if_instore():
    item = input("Enter the item you want to check : ")
    found=False
    for product in Store:
        if product['item'] == item:
            found=True       # used because we want to print the item details only if the item is available in the store
            print("Item is available in the store")
            print(product["item"], "available in store = ",product["amount"])
    if not found:
        print("Item is not available in the store")        
# A function to add a new item to the store
def add_store():
    item_=input("Enter item name : ")
    price_=int(input("Enter the price of item : "))
    amount_=int(input("Enter the amount of item : "))
    new_item={"item":item_,"price":price_,"amount":amount_}
    Store.append(new_item)       # append the new item to the store list
    print('Product is added in Store')
    show_store()
# A function to update the amount of an item in the store
def update_store():
    l=[]
    show_store()
    name=input("Enter the name of item to be updated")
    for product in Store:
        a=product['item']
        if a==name:       # if the item is found in the store
            new_amount=int(input("Enter the new amount of product added"))
            product['amount']+=new_amount       # adds to the existing amount
            print("Amount has been updated")
            show_store()
        else:
            print("Item is not available in store")
# To change the price of already available item in the store
def change_price():
    name=input("Enter the name of item to be updated")
    for product in Store:
        if product['item'] == name:
            new_prize = int(input("Enter the new prize of the item in store"))
            product['price'] = new_prize       #price is changed in the store list
            print("price updated")   
            show_store()
        else:
            print("Item not found in store")         
# Function for billing 
def cart_buy():
    cart = []
    total_price = 0.0
    while True:
        show_store()       # to show the available items in the store
        name = input("Enter the item name to add to the cart (or 'done' to end the cart): ")
        if name == 'Done':
            break
        found = False
        for product in Store:
            if name == product['item']:
                found = True
                quantity = int(input("Enter the quantity for " + name + ": "))
                if quantity <= product['amount']:
                    product['amount'] -= quantity
                    cart.append({'item': name, 'quantity': quantity})
                    total_price += quantity * product["price"]
                    print(str(quantity) + " units of " + name + " added to the cart.")
                else:
                    print("Sorry, only " + str(product['amount']) + " units available.")
                break  
        if not found:
            print(name + " is not in the store.")
    if total_price>=1000:
        print("You have a discount of 10%")
        total_price=total_price*0.9
    discount=input("Do you have a discount coupoun?")
    if discount== 'yes':
        print("You have a discount of 10%")
        total_price=total_price*0.9        
    print("\nFinal Cart:")
    for item in cart:
        print(str(item['quantity']) + " units of " + item['item'])
    print("Total Price: ₹" + str(total_price))
# Deleting an item from the store
def delete_item():
    name = input("Enter the item name to delete from the store: ")
    for product in Store:
        if product['item']==name:
            Store.remove(product)
            print("Item deleted")
            show_store()
            break
        else:
            print("Item not found in store")
            break
# Tracking the amount of items in the store
def tracking_stock():
    for product in Store:
        if product['amount'] <= 10:
            print(product['item'] + " is running low. Please restock.")
        elif product['amount'] <= 50:
            print(f"Reminder to check stock {product['item']} require checking.")

# Additional Functions
def look_store():
    stocks = input("Do you want to check the stock of these items? (yes/no) ")

    if stocks.lower() == 'yes':
        print("Store :")
        for product in Store:
            print(product['item'], '-', product["amount"])
    else:
        print("Not required")
        
# Main function
while True:
    print("Grocery Store Management:")
    print("1. View Store")
    print("2. Add item in Store")
    print("3. Update Store")
    print("4. Change the price of available stock")
    print("5. Form Cart and Calculate the Bill")
    print("6. Delete/Remove item from Store")
    print("7. To Check the stock of a particular item in the store")
    print("8. Exit the Store")
    choice=int(input("Enter the Function to be performed "))
    if choice==1:
        show_store()
    elif choice==2:
        add_store()
    elif choice==3:
        update_store()
    elif choice==4:
        change_price()
    elif choice==5:
        cart_buy()
    elif choice==6:
            delete_item()
    elif choice==7:
        if_instore()
    elif choice==8:
        break
    else:
        print("Invalid Function. Please choose a valid function.")
