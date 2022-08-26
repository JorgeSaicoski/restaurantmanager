# Restaurant Manager.
## Saas to manage restaurants.

### You can use it to sell the service for the restaurants in your city/region.
### Please, help us with updates.

## Usage
```bash
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```
### If you will use it in production, fix the settings.py in the folder restaurantmanager.
### You should to put your database and your domain.
### All image (logo and product) must to be create for you. So you can controll the server disk usage. 

# Preview
## https://micarta.jorgeadriano.info/
### To create a restaurant go to https://micarta.jorgeadriano.info/admin
### Login: Creator
### Password: pQG4BzhnafP0

### Dont forgot to put you as a owner.

## /restaurant/{you_restaurant_name}/ 
### Will show your restaurant's store.
## /staff/{you_restaurant_name}/
### Will show your staff's page
### Here you can saw the kitchen (all items to do)
### You can saw the orders oponed in weiter/delivery.
### You can "pay" the bill in cashier.
### And you can add new products.

# Contributing
## Please, if you are using it (to sell or to manage your restaurant), try to contribut.
### You can merge you version or contact jorge@sarkis.dev
