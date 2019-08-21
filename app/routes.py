#Libraries that are needed in order for this application 

from flask import render_template, flash
from app import app
from app.search import ProductSearch
from app.postalcode import AddressForm
import pandas as pd
import re as re
import json
import requests
import math
from app.geocoding import postal_geocode, createMap


#This helps us know when to hide certain images and search bars at appropriate times 
toshow = False
#Product information that we wil display 
product_name = ''
product_brand = ''

#Sample data made for this application 
product_data = pd.read_csv('/Users/KIMJI/Desktop/Product-App/app/sample.csv')
product_data = product_data.drop(['Unnamed: 0'], axis=1)


@app.route('/', methods = ['GET', 'POST'])
# Main index route
def index():

	#Initalize web forms
	form = ProductSearch()
	address= AddressForm()
	toshow = False
	product_name = []
	product_category = []
	product_brand = []
	top_result_num = 0

	# CONCAT FUNCTION FOR COLUMNS (removed, now done in csv file seperately)
	# product_data["Concat"] = [row[1].map(str).str.cat(sep=" ") for row in product_data.iterrows()]

	# Create a database for the given items
	data_new = pd.DataFrame()

	#If the user submits a item
	if form.validate_on_submit():

		form.item.data = str(form.item.data)
		form.item.data = form.item.data.upper()
		
		if (type(form.item.data)== str):
			data_new = product_data[product_data['CONCAT'].astype(str).str.contains(form.item.data, na = False)]

 

			if not data_new.empty:
				if len(data_new) >= 5: 
					top_result_num = 5
				else:
					top_result_num = len(data_new)

 

				for i in range(0, top_result_num):
					top_data = data_new.head(top_result_num)
					product_name = top_data['MATERIAL_DESCRIPTION'].tolist()
					product_brand = top_data['BRAND'].tolist()
					product_category = top_data['CATEGORY'].tolist()
					product_id = top_data['PRODUCT_NUM'].tolist()
					product_image = top_data['AD_IMAGE_ID'].tolist()


 
			else:
				product_name = ['Unavailable']
				product_brand = ['Unavailable']
				product_category = ['Unavailable']
				product_id = ['Unavailable']
				product_image = ['Unavailable']
		else:
			product_name = ['Unavailable']
			product_brand = ['Unavailable']
			product_category = ['Unavailable']
			product_id = ['Unavailable']
			product_image = ['Unavailable']


	return render_template('index.html', form=form, address=address, toshow = toshow, len_num = top_result_num, product_list=zip(product_name, product_category, product_brand))




# Product form: this will redirect to index when the product form is validated
@app.route('/product', methods = ['GET', 'POST'])
def product():

	#Initalize webforms
	form = ProductSearch()
	address= AddressForm()
	toshow = False
	product_name = []
	product_category = []
	product_brand = []
	product_id = []
	product_list = []
	top_result_num = 0
	# Create a database for the given items
	data_new = pd.DataFrame()

	#If the user submits a item
	if form.validate_on_submit():

 		form.item.data = str(form.item.data)
 		form.item.data = form.item.data.upper()

 		if (type(form.item.data)== str):
 			print("Enter")
 			print(form.item.data)
 			data_new = product_data[product_data['CONCAT'].astype(str).str.contains(form.item.data, na = False)]

 			print(data_new)
 			if not data_new.empty:

 				if len(data_new) >= 5: 
 					top_result_num = 5
 				else:
 					top_result_num = len(data_new)


 				top_data = data_new.head(top_result_num)
 				product_name = top_data['MATERIAL_DESCRIPTION'].tolist()
 				product_brand = top_data['BRAND'].tolist()
 				product_category = top_data['CATEGORY'].tolist()
 				product_id = top_data['PRODUCT_NUM'].tolist()
 				product_image = top_data['AD_IMAGE_ID'].tolist()

 			else:
 				product_name = ['Unavailable']
 				product_brand = ['Unavailable']
 				product_category = ['Unavailable']
 				product_id = ['Unavailable']
 				product_image = ['Unavailable']

 		else:
 			product_name = ['Unavailable']
 			product_brand = ['Unavailable']
 			product_category = ['Unavailable']
 			product_id = ['Unavailable']
 			product_image = ['Unavailable']

 		toshow = False
 		product_list = zip(product_name, product_category, product_brand, product_id, product_image)

	return render_template('index.html', form=form, len_num = top_result_num, address=address, toshow=toshow, product_list= product_list)


@app.route('/product/<product_id>', methods = ['GET', 'POST'])
@app.route("/product/<product_id>")
def product_details(product_id):
	address= AddressForm()
	the_id = int(product_id)
	if product_data[product_data['PRODUCT_NUM']==the_id].empty:
		flash("This does not exist")
	else:
		product_name = product_data['MATERIAL_DESCRIPTION'][product_data['PRODUCT_NUM']==the_id].iloc[0]
		product_brand = product_data['BRAND'][product_data['PRODUCT_NUM']==the_id].iloc[0]
		product_category = product_data['CATEGORY'][product_data['PRODUCT_NUM']==the_id].iloc[0]
		product_image = product_data['AD_IMAGE_ID'][product_data['PRODUCT_NUM']==the_id].iloc[0]

	return render_template("single.html", address=address, product_name = product_name, product_brand = product_brand, product_category = product_category, product_image =  product_image)



# Postal form: this will redirect to index when the postal form is validated
@app.route('/postal', methods = ['GET', 'POST'])
def postal():

	#Initalize webforms
	form = ProductSearch()
	address= AddressForm()
	top_result_num = 0
	store_name = []
	store_address = []
	store_postalcode = []
	toshow = False
	Map = None

	# Get product data and then drop unnamed column, and then concat for search algorithm purposes

	# Create a database for the given items
	data_new = pd.DataFrame()

	if address.validate_on_submit():

		toshow = False

		display_data = postal_geocode(address.item.data)
		print(display_data)
		display_data = display_data.drop(['Unnamed: 0'], axis=1)


		if display_data.empty:
			flash("WE COULD NOT FIND ANY STORES NEAR YOU. TRY SEARCHING FOR ANOTHER PRODUCT ABOVE")
		else:
			top_result_num = len(display_data)
			flash("Here are the closest stores: ")
			store_list = display_data['STORE_ID'].tolist()
			Map = createMap(display_data, store_list) 
			print(top_result_num)
			print(store_list)
			print(display_data)
			for i in range(0, top_result_num):
				top_data = display_data.head(top_result_num)
				store_name = top_data['BANNER'].tolist()
				store_address = top_data['ADDRESS'].tolist()
				store_postalcode = top_data['POSTAL_CODE'].tolist()


	return render_template('stores.html', form=form, address=address, toshow = toshow, mapURL = Map, store_list = zip(store_name, store_address, store_postalcode))