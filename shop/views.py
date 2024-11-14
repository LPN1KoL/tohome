from random import choice
from django.core.paginator import Paginator
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseNotFound
from django.contrib.auth import authenticate, login as user_login, logout as user_logout, update_session_auth_hash
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import check_password
from .forms import *
from .models import *
from .utils import *
from django.http import JsonResponse
from random import choice
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm

# Create your views here.
def home(request):
	ps = Product.objects.all()

	if len(ps) > 0:

		while True:
			p = choice(ps)
			if p.photo:
				break

		return render(request, 'new_ui/home.html', {
			'name_1': p.name, 'price_1': p.price, 'image_1': p.photo.url,
			'name_2': p.name, 'price_2': p.price, 'image_2': p.photo.url,
			'name_3': p.name, 'price_3': p.price, 'image_3': p.photo.url,
			'name_4': p.name, 'price_4': p.price, 'image_4': p.photo.url,
			'name_5': p.name, 'price_5': p.price, 'image_5': p.photo.url,
			'name_6': p.name, 'price_6': p.price, 'image_6': p.photo.url
		})
	else:
		return render(request, 'new_ui/home.html', {
		})


def login_view(request):
	if request.method == 'GET':
		return render(request, 'new_ui/login.html', {
			'form': LoginForm()
		})

	elif request.method == 'POST':
		login_ = request.POST.get('login')
		password_ = request.POST.get('password')

		usr = authenticate(request, username=login_, password=password_)

		if usr is not None:
			user_login(request, usr)
			return HttpResponseRedirect('/')
		else:
			return render(request, 'new_ui/login.html', {
				'form': LoginForm(request.POST)
			})


def reg_view(request):
	if request.method == 'GET':
		return render(request, 'new_ui/register.html', {
			'form': RegForm()
		})
	else:
		form = RegForm(request.POST)
		error = ''

		login = request.POST.get('login')
		password = request.POST.get('password')
		password2 = request.POST.get('password2')
		email = request.POST.get('email')

		if form.is_valid():
			if password != password2:
				error = 'Введённые пароли не совпадают!\n'
			if CustomUser.objects.filter(email=email).exists():
				error = 'Введённый адрес электронной почты занят!\n'
			if CustomUser.objects.filter(username=login).exists():
				error = 'Пользователь с таким логином уже существует!\n'

			if error:
				return render(request, 'new_ui/register.html', {
					'form': form,
					'error': error
				})

			else:
				new_user = CustomUser.objects.create(
					username=login,
					email=email
				)

				new_user.set_password(password)
				new_user.save()

				return HttpResponseRedirect('/login')


def logout(request):
	user_logout(request)
	return HttpResponseRedirect('/')


def catalog(request):

	products = []
	if request.method == 'GET':
		products = Product.objects.order_by('?')[:50]

	if request.method == 'POST':
		products = search_by_filters(request, Product.objects.all())


	return render(request, 'new_ui/catalog.html', {
		'products': products
	})


def categories(request):

	class Cat:
		def __init__(self, cat):
			self.cat = cat
			self.p = ProductCategory.objects.filter(category=cat)
			if len(self.p) > 0:
				a = True
				for product in self.p:
					if product.product.photo:
						self.p = product.product
						a = False
						break
				if a:
					self.p = self.p[0].product

			else:
				self.p = None

	cats = [Cat(x) for x in Category.objects.all()]
	cats = [x for x in cats if x.p]



	return render(request, 'new_ui/categories.html', {
		'categories': cats
	})


def detail_category(request, cat_id):
	cat = Category.objects.filter(id=cat_id)
	if len(cat) > 0:

		if request.method == 'GET':
			cat = cat[0]
			products = [x.product for x in ProductCategory.objects.filter(category=cat)]

			return render(request, 'new_ui/detail_category.html', {
				'category': cat,
				'products': products
			})

		if request.method == 'POST':
			cat = cat[0]
			products = search_by_filters(request, [x.product for x in ProductCategory.objects.filter(category=cat)])

			return render(request, 'new_ui/detail_category.html', {
				'category': cat,
				'products': products
			})

	else:
		return HttpResponseRedirect('/')


def detail_product(request, pid):
	product = Product.objects.filter(id=pid)

	if len(product) > 0:
		product = product[0]
		on_trash = False

		if UserTrash.objects.filter(user=request.user, product=product).exists():
			on_trash = True

		return render(request, 'new_ui/detail_product.html', {
			'product': product,
			'on_trash': on_trash
		})

	else:
		return HttpResponseRedirect('/')


def buy_product(request, pid):
	if request.user.is_authenticated:

		prod = Product.objects.filter(id=pid)
		if len(prod) > 0:

			prod = prod[0]

			ut = UserTrash.objects.filter(user=request.user, product=prod)

			if ut.exists():

				return HttpResponseRedirect(f'/trash')

			else:
				UserTrash.objects.create(user=request.user, product=prod, pcount=1)

			return HttpResponseRedirect(f'/product/{pid}')

		else:
			return HttpResponseRedirect('/login')

	else:
		return HttpResponseRedirect('/login')


def trash(request):
	if request.user.is_authenticated:

		products = UserTrash.objects.filter(user=request.user)
		total_sum = sum([x.product.price * x.pcount for x in products])

		return render(request, 'new_ui/trash.html', {
			'products': products,
			'total_sum': total_sum
		})

	return HttpResponseRedirect('/login')


def up_count(request, pid):
	prd = UserTrash.objects.filter(user=request.user, product=Product.objects.get(id=pid))
	if prd.exists():
		prd = prd[0]
		prd.pcount += 1
		prd.save()

	return HttpResponse(200)


def down_count(request, pid):
	prod = UserTrash.objects.filter(user=request.user, product=Product.objects.get(id=pid))
	if prod.exists():
		prod = prod[0]
		prod.pcount -= 1
		pcount = prod.pcount
		if prod.pcount > 0:
			prod.save()
		else:
			prod.delete()

		return JsonResponse({'count': pcount}, status=200)
	return HttpResponse(status=404)


def create_order(request):
	products = UserTrash.objects.filter(user=request.user)
	tprice = sum([x.product.price * x.pcount for x in products])
	cont = f'{request.user.email}'

	if request.user.phone_number:
		cont += f', {request.user.phone_number}'

	order = Order.objects.create(
		user=request.user,
		contacts=cont,
		total_price=tprice
	)

	for prod in products:
		OrderElement.objects.create(
			order=order,
			product=prod.product,
			pcount=prod.pcount
		)
		prod.delete()

	return HttpResponseRedirect('/trash')



@login_required
def order_detail(request, oid):
	order = Order.objects.get(id=oid)
	order_products = OrderElement.objects.filter(order=order)
	for prod in order_products:
		prod.total_price = prod.product.price * prod.pcount
		prod.save()
	return render(request, 'new_ui/order_detail.html', {'order': order, 'order_products': order_products})



@login_required
def my_orders(request):
	orders = Order.objects.filter(user=request.user).order_by('-create_at')
	return render(request, 'new_ui/my_orders.html', {'orders': orders})


@login_required
def order_edit(request, id):
	order = Order.objects.get(id=id)
	if order.user == request.user:
		form = OrderContactsForm(instance=order)

		if request.method == 'GET':


			return render(request, 'new_ui/order_edit.html', {
				'form': form
			})
		elif request.method == 'POST':
			form = OrderContactsForm(request.POST, instance=order)


			if form.is_valid:
				form.save()
				return HttpResponseRedirect('/my_orders')

	else:
		return HttpResponseNotFound(request)



@login_required
def lichniy_kabinet(request, id):
	user = CustomUser.objects.get(id=id)
	if request.user.id == user.id:

		form = UserRedForm(instance=user)

		if request.method == 'GET':

			return render(request, 'new_ui/lichniy_kabinet.html', {
				'form': form,
				'orders': Order.objects.filter(user=user)
			})
		elif request.method == 'POST':
			form = UserRedForm(request.POST, instance=user)

			if form.is_valid():
				usr = form.save(commit=False)
				for order in Order.objects.filter(user=user):
					contacts = '' + usr.email
					if usr.phone_number:
						contacts += f', {usr.phone_number}'
					order.contacts = contacts
					order.save()
				form.save()
				return HttpResponseRedirect(f'/user/{id}')
			else:
				return render(request, 'new_ui/lichniy_kabinet.html', {
				'form': form,
				'orders': Order.objects.filter(user=user),
				'errors': UserRedForm.errors
			})

	else:
		HttpResponseNotFound(request)


@login_required
def change_password(request, id):
	user = CustomUser.objects.get(id=id)
	if request.user.id == user.id:

		form = PasswordChangeForm(user=request.user)

		if request.method == 'GET':

			return render(request, 'new_ui/password_change.html', {
				'form': form
			})
		elif request.method == 'POST':
			form = PasswordChangeForm(user=request.user, data=request.POST)

			if form.is_valid():
				old_password = request.POST.get("old_password")
				if user.check_password(old_password):
					user = form.save()
					update_session_auth_hash(request, user)
					return HttpResponseRedirect(f'/user/{id}')
			else:
				return render(request, 'new_ui/password_change.html', {
				'form': form,
				'errors': PasswordChangeForm.errors
			})

	else:
		HttpResponseNotFound(request)


def examples(request):
	return render(request, 'new_ui/examples.html')


def about(request):
	return render(request, 'new_ui/about.html')
