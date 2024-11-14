from django.shortcuts import render
from django.http import HttpResponseNotFound, HttpResponseRedirect, JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import *
from django.views.decorators.csrf import csrf_exempt


@login_required
def admin_panel(request):
	if request.user.role.access_to_admin_panel:

		return render(request, 'admin_panel/home.html')

	else:
		return HttpResponseNotFound(request)


@login_required
def admin_panel_roles(request):
	if request.user.role.access_to_admin_panel:

		roles = Role.objects.all()

		return render(request, 'admin_panel/roles.html', {
			'roles': roles
		})

	else:
		return HttpResponseNotFound(request)


@login_required
def admin_panel_product_categories(request):
	if request.user.role.access_to_admin_panel:

		categories = Category.objects.all()

		return render(request, 'admin_panel/product_categories.html', {
			'categories': categories
		})

	else:
		return HttpResponseNotFound(request)


@login_required
def admin_panel_tags(request):
	if request.user.role.access_to_admin_panel:

		tags = Tag.objects.all()

		return render(request, 'admin_panel/tags.html', {
			'tags': tags
		})

	else:
		return HttpResponseNotFound(request)


@login_required
def admin_panel_products(request):
	if request.user.role.access_to_admin_panel:

		products = Product.objects.all()

		return render(request, 'admin_panel/products.html', {
			'products': products
		})

	else:
		return HttpResponseNotFound(request)


@login_required
def admin_panel_products_add(request):
	if request.user.role.access_to_admin_panel:
		form = ProductForm()
		if request.method == 'GET':
			return render(request, 'admin_panel/product_add.html', {
				'form': form
				})
		else:
			form = ProductForm(request.POST, request.FILES)
			if form.is_valid:
				form.save()
				return HttpResponseRedirect('/admin_panel/products')
	else:
		return HttpResponseNotFound(request)


@login_required
def admin_panel_add_tag(request):
	if request.user.role.access_to_admin_panel:
		form = TagForm()
		if request.method == 'GET':
			return render(request, 'admin_panel/tag_add.html', {
					'form': form
				})
		else:
			form = TagForm(request.POST)
			if form.is_valid:
				form.save()
				return HttpResponseRedirect('/admin_panel/tags')
	else:
		return HttpResponseNotFound(request)


@login_required
def admin_panel_add_category(request):
	if request.user.role.access_to_admin_panel:
		form = CategoryForm()
		if request.method == 'GET':
			return render(request, 'admin_panel/category_add.html', {
				'form': form
			})
		else:
			form = CategoryForm(request.POST)
			if form.is_valid:
				form.save()
				return HttpResponseRedirect('/admin_panel/categories')
	else:
		return HttpResponseNotFound(request)


@login_required
def admin_panel_edit_product(request, pid):
	if request.user.role.access_to_admin_panel:

		product = Product.objects.get(id=pid)
		form = ProductForm(instance=product)

		if request.method == 'GET':

			p_tags = [x.tag for x in ProductTag.objects.filter(product=product)]
			ptids = [x.id for x in p_tags]
			all_tags = [x for x in Tag.objects.all() if x.id not in ptids]

			p_cats = [x.category for x in ProductCategory.objects.filter(product=product)]
			pcids = [x.id for x in p_cats]
			all_cats = [x for x in Category.objects.all() if x.id not in pcids]

			if product.photo:
				photo_url = product.photo.url
			else:
				photo_url = False

			return render(request, 'admin_panel/product_edit.html', {
				'form': form,
				'photo_url': photo_url,
				'product_tags': p_tags,
				'product_categories': p_cats,
				'all_tags': all_tags,
				'all_categories': all_cats,
				'pid': product.id
			})
		elif request.method == 'POST':
			form = ProductForm(request.POST, request.FILES, instance=product)

			if form.is_valid:
				form.save()
				return HttpResponseRedirect('/admin_panel/products')
	else:
		return HttpResponseNotFound(request)


@csrf_exempt
@login_required
def admin_panel_remove_product_tag(request):
	if request.user.role.access_to_admin_panel:
		if request.method == 'POST':

			product = Product.objects.get(id=int(request.POST.get('pid')))
			tag = Tag.objects.get(id=int(request.POST.get('tid')))

			ProductTag.objects.filter(product=product, tag=tag).delete()

			return JsonResponse({}, status=200)

	else:
		return HttpResponseNotFound(request)


@csrf_exempt
@login_required
def admin_panel_add_product_tag(request):
	if request.user.role.access_to_admin_panel:
		if request.method == 'POST':

			product = Product.objects.get(id=int(request.POST.get('pid')))
			tag = Tag.objects.get(id=int(request.POST.get('tid')))

			if ProductTag.objects.filter(product=product, tag=tag).count() == 0:
				ProductTag.objects.create(product=product, tag=tag)

				return JsonResponse({}, status=200)

	else:
		return HttpResponseNotFound(request)


@csrf_exempt
@login_required
def admin_panel_remove_product_cat(request):
	if request.user.role.access_to_admin_panel:
		if request.method == 'POST':

			product = Product.objects.get(id=int(request.POST.get('pid')))
			cat = Category.objects.get(id=int(request.POST.get('cid')))

			ProductCategory.objects.filter(product=product, category=cat).delete()

			return JsonResponse({}, status=200)

	else:
		return HttpResponseNotFound(request)


@csrf_exempt
@login_required
def admin_panel_add_product_cat(request):
	if request.user.role.access_to_admin_panel:
		if request.method == 'POST':

			product = Product.objects.get(id=int(request.POST.get('pid')))
			cat = Category.objects.get(id=int(request.POST.get('cid')))

			if ProductCategory.objects.filter(product=product, category=cat).count() == 0:
				ProductCategory.objects.create(product=product, category=cat)

				return JsonResponse({}, status=200)

	else:
		return HttpResponseNotFound(request)


@csrf_exempt
@login_required
def delete_product(request):
	if request.user.role.access_to_admin_panel:
		if request.method == 'POST':

			Product.objects.filter(id=int(request.POST.get('pid'))).delete()
			return JsonResponse({}, status=200)

	else:
		return HttpResponseNotFound(request)


@csrf_exempt
@login_required
def admin_panel_delete_category(request):
	if request.user.role.access_to_admin_panel:
		if request.method == 'POST':

			cid = int(request.POST.get('cid'))

			Category.objects.filter(id=cid).delete()
			return JsonResponse({}, status=200)

	else:
		return HttpResponseNotFound(request)


@csrf_exempt
@login_required
def admin_panel_delete_tag(request):
	if request.user.role.access_to_admin_panel:
		if request.method == 'POST':

			cid = int(request.POST.get('tid'))

			Tag.objects.filter(id=cid).delete()
			return JsonResponse({}, status=200)

	else:
		return HttpResponseNotFound(request)


@csrf_exempt
@login_required
def delete_order(request):
	if request.user.role.access_to_admin_panel:
		if request.method == 'POST':

			Order.objects.filter(id=int(request.POST.get('oid'))).delete()
			return JsonResponse({}, status=200)

	else:
		return HttpResponseNotFound(request)


@login_required
def admin_panel_orders(request):
	if request.user.role.access_to_admin_panel:
		orders = Order.objects.all().order_by('-create_at')
		return render(request, 'admin_panel/orders.html', {'orders': orders})


@login_required
def admin_panel_order(request, oid):
	if request.user.role.access_to_admin_panel:
		order = Order.objects.get(id=oid)
		order_products = OrderElement.objects.filter(order=order)
		for prod in order_products:
			prod.total_price = prod.product.price * prod.pcount
			print(prod.product.price, prod.pcount, prod.total_price, order.total_price)
		return render(request, 'admin_panel/order_detail.html', {'order': order, 'order_products': order_products})
	else:
		return HttpResponseNotFound(request)


@csrf_exempt
@login_required
def admin_delete_role(request, rid):
	if request.user.role.access_to_admin_panel:
		role = Role.objects.get(id=rid)
		role.delete()
		return HttpResponse(status=200)
	else:
		return HttpResponseNotFound(request)


@login_required
def admin_edit_role(request, rid):
	if request.user.role.access_to_admin_panel:

		role = Role.objects.get(id=rid)
		form = RoleForm(instance=role)

		if request.method == 'GET':

			return render(request, 'admin_panel/edit_role.html', {
				'form': form
			})
		elif request.method == 'POST':
			form = RoleForm(request.POST, instance=role)

			if form.is_valid:
				form.save()
				return HttpResponseRedirect('/admin_panel/roles')
	else:
		return HttpResponseNotFound(request)


@login_required
def admin_add_role(request):
	if request.user.role.access_to_admin_panel:

		form = RoleForm()

		if request.method == 'GET':

			return render(request, 'admin_panel/add_role.html', {
				'form': form
			})
		elif request.method == 'POST':
			form = RoleForm(request.POST)

			if form.is_valid:
				form.save()
				return HttpResponseRedirect('/admin_panel/roles')
	else:
		return HttpResponseNotFound(request)


@login_required
def admin_edit_order(request, id):
	if request.user.role.access_to_admin_panel:

		order = Order.objects.get(id=id)
		form = OrderForm(instance=order)
		total_price = 0

		if request.method == 'GET':
			order_products = OrderElement.objects.filter(order=order)
			for prod in order_products:
				prod.total_price = prod.product.price * prod.pcount
				prod.save()
				total_price += prod.total_price


			return render(request, 'admin_panel/order_edit.html', {
				'form': form,
				'order_products': order_products,
				'total_price': total_price
			})
		elif request.method == 'POST':
			form = OrderForm(request.POST, instance=order)


			if form.is_valid:
				form.save()
				return HttpResponseRedirect('/admin_panel/orders')
	else:
		return HttpResponseNotFound(request)


@csrf_exempt
def order_upcount(request):
	if request.POST:
		id = int(request.POST.get('id'))
		order_el = OrderElement.objects.get(id=id)
		order_el.pcount += 1
		order = order_el.order
		order.total_price += order_el.product.price
		order.save()
		order_el.save()

		return JsonResponse({'price': order_el.product.price}, status=200)


@csrf_exempt
def order_downcount(request):
	if request.POST:
		id = int(request.POST.get('id'))
		order_el = OrderElement.objects.get(id=id)
		if order_el.pcount > 0:
			order_el.pcount -= 1
			order = order_el.order
			order.total_price -= order_el.product.price
			order.save()
			order_el.save()
			return JsonResponse({'price': order_el.product.price}, status=200)
		else:
			return HttpResponse(status=203)
