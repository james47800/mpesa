from __future__ import unicode_literals
from django_daraja.mpesa import utils
from django.http import HttpResponse,JsonResponse
from django.views.generic import View
from django_daraja.mpesa.core import MpesaClient
from decouple import config
from datetime import datetime
#end of mpesa related imports


from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Myproduct
from .forms import UserRegistrationForm
from django.contrib.auth.decorators import login_required

#start of mpesa instances and variables
cl=MpesaClient()
stk_push_callback_url ="https://api.darajambili.com/express-payment"
b2c_callback_url = ""
#end of mpesa instance and variables

def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'account created successfully')
            return redirect('users-registration')
        else:
            messages.error(request, 'account not successfully created')
            return redirect('users-registration')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})


@login_required()
def home(request):
    return render(request, 'home.html')


@login_required()
def addproduct(request):
    if request.method == "POST":
        p_name = request.POST.get("jina")
        p_quantity = request.POST.get("kiasi")
        p_price = request.POST.get("bei")
        product = Myproduct(prod_name=p_name, prod_quantity=p_quantity, prod_price=p_price)
        product.save()
        messages.success(request, 'Product saved successfully')
        return redirect('add-products')
    return render(request,
                  'addproduct.html')
@login_required()
def view_products(request):
    #Select all the products from the database
    products= Myproduct.objects.all()
    #Render the template with the products
    return render(request, 'products.html', {'products':products})

@login_required()
def delete_product(request, id):
    #select the product you want to delete
    product=Myproduct.objects.get(id=id)
    #finally delete the product
    product.delete()
    #redirect back to the products page with a success message
    messages.success(request,'product deleted successfully')
    return redirect('products')

@login_required
def updateproduct(request,id):
    #select the product to be updated
    product=Myproduct.objects.get(id=id)
    #check if the form has any submitted records to receive them
    if request.method=="POST":
        updated_field=request.POST.get("jina")
        updated_price= request.POST.get("bei")
        updated_quantity = request.POST.get("kiasi")

        #update the selected product above with the received data
        product.prod_name= updated_field
        product.prod_quantity=updated_quantity
        product.prod_price=updated_price


        #return the updated data back to the database
        product.save()

        #redirect back to the products page with a success message
        messages.success(request,'Product updated successfully')
        return redirect('products')

    return render(request,"updateproduct.html",{'product':product})

def auth_success(request):
    token= cl.access_token()
    return JsonResponse(token,safe=False)

@login_required
def payment(request,id):
    #select the product being paid
    product=Myproduct.objects.get(id=id)
    #check if the form being submitted has a post method
    if request.method=="POST":
        phone_number = request.POST.get('nambari')
        amount= request.POST.get('bei')
        amount = int(amount)
        #proceed with the payment by launching mpesa sim toolkit
        account_ref = "TRNSACT001"
        transaction_description= "Payment for a product"
        callback_url = 'https://api.darajambili.com/express-payment'
        stk = cl.stk_push(phone_number,amount,account_ref,transaction_description,stk_push_callback_url)
        mpesa_response = stk.response_description
        messages.success(request,mpesa_response)
        return JsonResponse(mpesa_response,safe=False)
    return render(request,'payment.html',{'product':product})