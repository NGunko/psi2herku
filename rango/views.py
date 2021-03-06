from django.http import HttpResponse
from django.shortcuts import render
# Import the Category model
from rango.models import Category
from rango.models import Page
#Add this import at the top of the file
from rango.forms import CategoryForm
from rango.forms import PageForm




def index(request):
  	category_list = Category.objects.order_by('-likes')[:5]
	page_list = Page.objects.order_by('-views')[:5]
	context_dict = {'categories': category_list, 'pages': page_list}
	return render(request, 'rango/index.html', context_dict)

def about(request):
	# Construct a dictionary to pass to the template engine as its context.
	# Note the key boldmessage is the same as {{ boldmessage }} in the template!
	context_dict = {'boldmessage': "this tutorial has been put together by pelayo and aurora!"}
	# Return a rendered response to send to the client.
	# We make use of the shortcut function to make our lives easier.
	# Note that the first parameter is the template we wish to use.
	return render(request, 'rango/about.html', context=context_dict)


def show_category(request, category_name_slug):
	# Create a context dictionary which we can pass
	# to the template rendering engine.
	context_dict = {}
	try:
		# Can we find a category name slug with the given name?
		# If we can't, the .get() method raises a DoesNotExist exception.
		# So the .get() method returns one model instance or raises an exception.
		category = Category.objects.get(slug = category_name_slug)
		# Retrieve all of the associated pages.
		# Note that filter() will return a list of page objects or an empty list
		pages=Page.objects.filter(category=category)
		# Adds our results list to the template context under name pages.
		context_dict['pages']=pages
		# We also add the category object from
		# the database to the context dictionary.
		# We'll use this in the template to verify that the category exists.
		context_dict['category']=category
	except Category.DoesNotExist:
		context_dict['category']=None
		context_dict['pages']=None
	return render(request, 'rango/category.html', context_dict)

def add_category(request):
	form=CategoryForm()

	if request.method == 'POST':
		form = CategoryForm(request.POST)
		if form.is_valid():
			cat = form.save(commit=True)
			# Now that the category is saved
			# We could give a confirmation message
			# But since the most recent category added is on the index page
			# Then we can direct the user back to the index page.
			return index(request)
		else:
			print(form.errors)
	# Will handle the bad form, new form, or no form supplied cases.
	# Render the form with error messages (if any)

	return render(request, 'rango/add_category.html', {'form': form})


def add_page(request, category_name_slug):
	try:
		category = Category.objects.get(slug=category_name_slug)
	except Category.DoesNotExist:
		category= None
	form = PageForm()
	if request.method == 'POST':
		form = PageForm(request.POST)
		if form.is_valid():
			if category:
				page = form.save(commit = False)
				page.category = category
				page.views = 0
				page.save()
				return show_category(request, category_name_slug)
			else:
				print(form.errors)
	context_dict = {'form': form, 'category': category}
	return render(request, 'rango/add_page.html', context_dict)
