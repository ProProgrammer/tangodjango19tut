from datetime import datetime

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render

from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm
from rango.models import Category, Page


def index(request):
    # Query the database for a list of All categories currently stored
    # Order the categories by number of likes in descending order.
    # Retrieve the top 5 categories only - or all if less than or equal to 5.
    # Place the list in our context_dict dictionary that will be passed to the template engine

    category_list = Category.objects.order_by('-likes')[:5]
    # The expression above queries the Category model to retrieve top five categories.
    # It uses order_by() method to sort by the number of likes in descending order.
    # The - in `-likes` denotes that we would like them in descending order
    # If we removed the `-` and kept it just `likes` it would return it in ascending order
    # The [:5] is to return the first five items only (index 0 through 4)

    pages_list = Page.objects.order_by('-views')[:5]

    context_dict = {'categories': category_list,
                    'pages': pages_list}

    # Call function to handle the site counter related cookies
    visitor_cookie_handler(request)
    context_dict['visits'] = request.session['visits']

    # Obtain the response object early so we can add cookie information
    response = render(request, 'rango/index.html', context_dict)

    # Render response back to the user, udpating any cookies that need changed
    return response


def about(request):
    visitor_cookie_handler(request)
    context_dict = dict()

    context_dict['boldmessage'] = 'This tutorial has been put together by Deep Sukhwani'

    context_dict['visits'] = request.session['visits']

    return render(request, 'rango/about.html', context=context_dict)


def show_category(request, category_name_slug):
    # Create a context dictionary which we can pass to the template rendering engine
    context_dict = {}

    try:
        # Can we find a category name slug with the given name?
        # If we can't, the .get() method raises a DoesNotExist exception.
        # So the .get() method returns on method instance or raises an exception
        category = Category.objects.get(slug=category_name_slug)

        # Retrieve all associated pages
        # Note that filter() will return a list of page objects or an empty list
        pages = Page.objects.filter(category=category)

        # Add our results list to the template context dictionary under name pages
        context_dict['pages'] = pages

        # We also add category object from the database to the context dictionary.
        # We will use this in the template to verify the category exists
        context_dict['category'] = category

    except Category.DoesNotExist:
        # We get here if we didn't find the specified category (i.e. - the category name slug requested was invalid)
        # Don't do anything - the template will display "no category" message for us

        context_dict['category'] = None
        context_dict['pages'] = None

    # Go render the response and return it to the client
    return render(request, 'rango/category.html', context=context_dict)


"""
All view functions defined as part of a Django application must take at least one parameter. This is typically called
request and provides access to information related to the given HTTP request made by the user.
When parameterizing URLs, you supply additional named parameters to the signature for the given view.
That is why our show_category() view was defined as def show_category(request, category_name_slug).
"""


@login_required
def add_category(request):
    form = CategoryForm()

    # A HTTP POST?
    if request.method == 'POST':
        form = CategoryForm(request.POST)

        # Have we been provided with a valid form?

        if form.is_valid():
            # Save the new category to the database
            form.save(commit=True)

            # Now that the category is saved, we could give a confirmation message
            # But since the most recent category added is on the index page
            # Then we can direct the user back to the index page
            return index(request)

        else:
            # The supplied form contained errors
            # Just print them to the terminal.
            print form.errors

    # Will handle the bad form, new form or no form supplied cases.
    # Render the form with error messages (if any)
    return render(request, 'rango/add_category.html', {'form': form})


@login_required
def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None

    form = PageForm()

    # Is this a HTTP Post request?
    if request.method == 'POST':
        form = PageForm(request.POST)

        # Is the form valid?
        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()
            return show_category(request, category_name_slug)
        else:
            print form.errors

    context_dict = {'form': form, 'category': category}

    # This will handle the bad form, new form or no form supplied cases.
    # Render the form with error messages (if any)
    return render(request, 'rango/add_page.html', context=context_dict)


def register(request):
    # A boolean value "registered" for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when the registration succeeds.
    registered = False

    # If it's a HTTP POST, we're interested in processing the form data
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        # If the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid():
            # Save the user's form data to the database
            user = user_form.save()

            # Now we hash the password with the set_password method.
            user.set_password(user.password)
            user.save()

            # Now sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves, we set commit=False. This delays saving the model
            # until we're ready to avoid integrity problems
            profile = profile_form.save(commit=False)
            profile.user = user

            # Did the user provide a profile picutre?
            # If so, we need to get it from the input form and put it in the UserProfile model
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            # Now we save the UserProfile model instance
            profile.save()

            # Update our variable to indicate that the template registration was successful
            registered = True

        else:
            # Invalid form or forms - mistakes or something else?
            # Print problem to the terminal
            print user_form.errors, profile_form.errors

    else:
        # Not a HTTP POST, so we render our form using two ModelForm instances
        # These forms will be blank, ready for user input
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request,
                  'rango/register.html',
                  {'user_form': user_form,
                   'profile_form': profile_form,
                   'registered': registered})


def user_login(request):
    """
    This view will handle the processing of data from subsequent login form, and attempt to log a user in with the
    given details.
    """

    # if the request is a HTTP POST, try to pull out the relevant information
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
        # We use request.POST.get('<variable>') as opposed to request.POST['<variable>'] because the .get method on a
        #  dictionary like object returns None if the value does not exist, while request.POST['<variable>'] with
        # raise a KeyError exception.

        username = request.POST.get('username')
        password = request.POST.get('password')

        # Use Django's machinery to attempt to see if the username/password combination is valid - a User object is
        # returned if it is.
        user = authenticate(username=username, password=password)

        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user with matching credentials was found.
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                return HttpResponseRedirect(reverse('rango:index'))
            else:
                error = "Your rango account is disabled"
                # An inactive account was used - no logging in!
                return render(request, 'rango/login.html', {'error': error})
        else:
            # Bad login details were provided. So we can't log the user in.
            error = "Invalid Login details"
            return render(request, 'rango/login.html', {'error': error})
            # return HttpResponse("Invalid login details supplied.")

    # This request is not a HTTP POST, so display the login form.
    # This scenario most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the blank dictionary object
        return render(request, 'rango/login.html', {})


@login_required
def restricted(request):
    return render(request, 'rango/restricted.html')


"""
Methods to check if a user is authenticated:

-- In the template --
use {% if user.authenticated %}

-- In the view --
Directly examine the request object & check if user is authenticated

-- Use a decorator function --
Django provides @login_required decorator that checks if the user is authenticated

---------------------

The direct approach checks to see whether a user is logged in via user.is_authenticated() method.
The user object is available via the request object passed into a view.

Eg:

def some_view(request):
    if not request.user.is_authenticated():
        return HttpResponse("You are not logged in")
    else:
        return HttpResponse("You are logged in")

---------------------

The third approach uses Python decorators.
Django provides a decorator called login_required(), which we can attach to any view where we require the user to be
logged in. If a user is not logged in and attempts to access a view decorated with login_required(), they are then
redirected to another page (that we can set) - typically the login page.

Eg usage:

from django.contrib.auth.decorators import login_required

@login_required
def restricted(request):
    return HttpResponse("Since you are logged in, you can see this text!")
"""


@login_required()
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out
    logout(request)
    return HttpResponseRedirect(reverse('rango:index'))


# A helper method
def get_server_side_cookie(request, cookie, default_val=None):
    val = request.session.get(cookie)

    if not val:
        val = default_val
    return val


# Update function definition to use server side storage of user information
def visitor_cookie_handler(request):
    """
    This is not a view since it doesn't return a response.
    This is simply a helper function that will be called inside index() view

    # Get the number of visits to the site.
    # We use the COOKIES.get() function to obtain the visits cookie.
    # If the cookie exists, the value returned is casted to an integer.
    # If the cookie doesn't exist, then the default value of 1 is used.
    # We than use last_visit cookie value to see the last visit datetime, if it doesn't exist we return current
    datetime to current datetime hence set last_visit as current datetime
    # We use last_visit_time to store last visit time
    """

    # Cookie values are returned as strings, hence casting it to an integer
    visits = int(get_server_side_cookie(request, 'visits', '1'))

    # if datetime.now() is datetime.datetime(2017, 1, 26, 8, 23, 12, 849111)
    # str(datetime.now()) will be 2017-01-26 08:23:12.849111
    # last_visit_time will be datetime.datetime(2017, 1, 26, 8, 23, 12)
    last_visit_cookie = get_server_side_cookie(request, 'last_visit', str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7], '%Y-%m-%d %H:%M:%S')

    # If it's been more than a day since the last visit...
    # For testing purpose, change days to seconds in next line so that the counter updates after every second and you
    #  do not have to wait for a day to see incrementing value of visits cookie.
    if (datetime.now() - last_visit_time).days > 0:
        visits += 1

        # Update the last visit cookie now that we have updated the count
        request.session['last_visit'] = str(datetime.now())
    else:
        visits = 1

        # Set the last visit cookie
        request.session['last_visit'] = last_visit_cookie

    # Update / set the visits cookie
    request.session['visits'] = visits
