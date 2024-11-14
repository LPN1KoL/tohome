from django.urls import path
from .admin_panel_views import *
from .views import *



admin_panel_urlpatterns = [
	path('admin_panel', admin_panel),
	path('admin_panel/roles', admin_panel_roles),
	path('admin_panel/categories', admin_panel_product_categories),
	path('admin_panel/categories/delete', admin_panel_delete_category),
	path('admin_panel/tags', admin_panel_tags),
	path('admin_panel/tags/delete', admin_panel_delete_tag),
	path('admin_panel/tags/add', admin_panel_add_tag),
	path('admin_panel/products', admin_panel_products),
	path('admin_panel/products/add', admin_panel_products_add),
	path('admin_panel/products/edit/<int:pid>', admin_panel_edit_product),
	path('admin_panel/remove_tag', admin_panel_remove_product_tag),
	path('admin_panel/add_tag', admin_panel_add_product_tag),
	path('admin_panel/categories/add', admin_panel_add_category),
	path('admin_panel/remove_cat', admin_panel_remove_product_cat),
	path('admin_panel/add_cat', admin_panel_add_product_cat),
	path('admin_panel/delete_product', delete_product),
	path('admin_panel/orders', admin_panel_orders),
	path('admin_panel/delete_order', delete_order),
	path('admin_panel/order/<int:oid>', admin_panel_order),
	path('admin_panel/delete_role/<int:rid>', admin_delete_role),
	path('admin_panel/edit_role/<int:rid>', admin_edit_role),
	path('admin_panel/roles/add', admin_add_role),
	path('admin_panel/orders/edit/<int:id>', admin_edit_order),
	path('admin_panel/upcount', order_upcount),
	path('admin_panel/downcount', order_downcount)
]

urlpatterns = [
	path('', home),
	path('login', login_view),
	path('register', reg_view),
	path('logout', logout),
	path('catalog', catalog),
	path('categories', categories),
	path('categories/<int:cat_id>', detail_category),
	path('product/<int:pid>', detail_product),
	path('product/<int:pid>/buy', buy_product),
	path('trash', trash),
	path('up_count/<int:pid>', up_count),
	path('down_count/<int:pid>', down_count),
	path('confirm_order', create_order),
	path('my_orders', my_orders),
	path('order_detail/<int:oid>', order_detail),
	path('order_edit/<int:id>', order_edit),
	path('user/<int:id>', lichniy_kabinet),
	path('change_password/<int:id>', change_password),
	path('examples', examples),
	path('about', about)
] + admin_panel_urlpatterns
