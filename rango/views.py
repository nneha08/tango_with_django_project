"""Put Package Comments here..."""
#################################
# Default Django imports
#################################
from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponse

#################################
# Internal Project Dependecies
#################################
from rango.models import Category
from rango.models import Page
from rango.forms import CategoryForm
from rango.forms import PageForm
from rango.forms import UserForm, UserProfileForm
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from datetime import datetime

# Remember to use .gitignore in your code so that files like `.idea` will
# not be commited in the code
# Sample Gitignore can be found at
# `https://github.com/django/django/blob/master/.gitignore`

# Try and implement class based Views instead of method based Views.
# Method based views have been deprecated and should not be used.
# Also read about *args and **kwargs. Its a gread thing in Python


def index(request, *args, **kwargs):
    """Put method docstring here.."""
    request.session.set_test_cookie()
    try:
        category_list = Category.objects.order_by('-likes')[:6]
        page_list = Page.objects.order_by('-views')[:5]
    except Exception as exc:
        print exc
        # Try and implement Try-Except wherever you think you should.
    context_dict = {'categories': category_list, 'pages': page_list}

    # Return a rendered response to send to the client.
    # We make use of the shortcut function to make our lives easier.
    # Note that the first parameter is the template we wish to use.

    # Whenever use a method from predefined libray like `render` try and
    # and put in the argument name before it. Like done in below method call
    # of render. Its a good paradigm to follow this in Python
    # Use Ipython for testing install it using pip install ipython
    # Do All the work in a virtualenv.
    # Also see I have crreated a new file called requirements.txt. So put
    # all the packages that will be used by your project in that
    # requirements.txt.
    # sudo pip install --upgrade /path/to/requirements.txt will install all
    # packages. Once you install all the packages and are about to push the
    # code remeber to do pip freeze > /path/to/requirements.txt

    # The mistake in your code is path of the templates file
    # Also, you might need to implement TEMPLATES in settings.py file of your
    # project
    #return render(request, 'rango/index.html', context_dict)
    # return render(request=request,
    #               template_name='rango/index.html',
    #               context=context_dict,
    #               status=200,
    #               content_type='Appliation/JSON')

    visits = request.session.get('visits')
    if not visits:
        visits = 1
    reset_last_visit_time = False

    last_visit = request.session.get('last_visit')
    if last_visit:
        last_visit_time = datetime.strptime(last_visit[:-7], "%Y-%m-%d %H:%M:%S")

        if (datetime.now() - last_visit_time).days > 0:
            # ...reassign the value of the cookie to +1 of what it was before...
            visits = visits + 1
            # ...and update the last visit cookie, too.
            reset_last_visit_time = True
    else:
        # Cookie last_visit doesn't exist, so create it to the current date/time.
        reset_last_visit_time = True

    if reset_last_visit_time:
        request.session['last_visit'] = str(datetime.now())
        request.session['visits'] = visits
    context_dict['visits'] = visits

    response = render(request, 'rango/index.html', context_dict)

    return response


def about(request):
    """Put Comments....."""
    context_dict = {'boldmessage': 'it will tell u about RANGO :)'}
    if request.session.get('visits'):
        count = request.session.get('visits')
    else:
        count = 0

    context_dict['visits'] = count

    # You can see, I have implemented JsonResponse instead of render
    # `JsonResponse` will return a dictioanry to the browser instead of HTML
    # In mobile-apps JsonResponse|HttpRespoinse is used and not render.
    # I understand that you are following a tutorial that is fine for now.
    # `render` is obviously used when you need to run the front-end of a
    # website using Django.
    # return JsonResponse(data=context_dict, status=200)
    return render(request, 'rango/about.html', context_dict)


def category(request, category_name_slug):
    """.."""
    context_dict = {}

    try:
        category = Category.objects.get(slug=category_name_slug)
        context_dict['category_name'] = category.name
        pages = Page.objects.filter(category=category)
        context_dict['pages'] = pages
        context_dict['category'] = category
    except Category.DoesNotExist:
        pass

    return render(request, 'rango/category.html', context_dict)


@login_required
def add_category(request):

    # A HTTP POST?
    if request.method == 'POST':
        form = CategoryForm(request.POST)

        # Have we been provided with a valid form?
        if form.is_valid():
            # Save the new category to the database.
            form.save(commit=True)

            # Now call the index() view.
            # The user will be shown the homepage.
            return index(request)
        else:
            # The supplied form contained errors - just print them to the terminal.
            print form.errors
    else:
        # If the request was not a POST, display the form to enter details.
        form = CategoryForm()

    # Bad form (or form details), no form supplied...
    # Render the form with error messages (if any).
    return render(request, 'rango/add_category.html', {'form': form})


@login_required
def add_page(request, category_name_slug):

    try:
        cat = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
                cat = None

    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            if cat:
                page = form.save(commit=False)
                page.category = cat
                page.views = 0
                page.save()
                # probably better to use a redirect here.
                return category(request, category_name_slug)
        else:
            print form.errors
    else:
        form = PageForm()

    context_dict = {'form': form, 'category': cat}
    return render(request, 'rango/add_page.html', context_dict)


# def register(request):
#
#     if request.session.test_cookie_worked():
#         print ">>>> TEST COOKIE WORKED!"
#         request.session.delete_test_cookie()
#     # A boolean value for telling the template whether the registration was successful.
#     # Set to False initially. Code changes value to True when registration succeeds.
#     registered = False
#
#     # If it's a HTTP POST, we're interested in processing form data.
#     if request.method == 'POST':
#         # Attempt to grab information from the raw form information.
#         # Note that we make use of both UserForm and UserProfileForm.
#         user_form = UserForm(data=request.POST)
#         profile_form = UserProfileForm(data=request.POST)
#
#         # If the two forms are valid...
#         if user_form.is_valid() and profile_form.is_valid():
#             # Save the user's form data to the database.
#             user = user_form.save()
#
#             # Now we hash the password with the set_password method.
#             # Once hashed, we can update the user object.
#             user.set_password(user.password)
#             user.save()
#
#             # Now sort out the UserProfile instance.
#             # Since we need to set the user attribute ourselves, we set commit=False.
#             # This delays saving the model until we're ready to avoid integrity problems.
#             profile = profile_form.save(commit=False)
#             profile.user = user
#
#             # Did the user provide a profile picture?
#             # If so, we need to get it from the input form and put it in the UserProfile model.
#             if 'picture' in request.FILES:
#                 profile.picture = request.FILES['picture']
#
#             # Now we save the UserProfile model instance.
#             profile.save()
#
#             # Update our variable to tell the template registration was successful.
#             registered = True
#
#         # Invalid form or forms - mistakes or something else?
#         # Print problems to the terminal.
#         # They'll also be shown to the user.
#         else:
#             print user_form.errors, profile_form.errors
#
#     # Not a HTTP POST, so we render our form using two ModelForm instances.
#     # These forms will be blank, ready for user input.
#     else:
#         user_form = UserForm()
#         profile_form = UserProfileForm()
#
#     # Render the template depending on the context.
#     return render(request,
#                     'rango/register.html',
#                     {'user_form': user_form, 'profile_form': profile_form, 'registered': registered})


# def user_login(request):
#
#     # If the request is a HTTP POST, try to pull out the relevant information.
#     if request.method == 'POST':
#         # Gather the username and password provided by the user.
#         # This information is obtained from the login form.
#                 # We use request.POST.get('<variable>') as opposed to request.POST['<variable>'],
#                 # because the request.POST.get('<variable>') returns None, if the value does not exist,
#                 # while the request.POST['<variable>'] will raise key error exception
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#
#         # Use Django's machinery to attempt to see if the username/password
#         # combination is valid - a User object is returned if it is.
#         user = authenticate(username=username, password=password)
#
#         # If we have a User object, the details are correct.
#         # If None (Python's way of representing the absence of a value), no user
#         # with matching credentials was found.
#         if user:
#             # Is the account active? It could have been disabled.
#             if user.is_active:
#                 # If the account is valid and active, we can log the user in.
#                 # We'll send the user back to the homepage.
#                 login(request, user)
#                 return HttpResponseRedirect('/rango/')
#             else:
#                 # An inactive account was used - no logging in!
#                 return HttpResponse("Your Rango account is disabled.")
#         else:
#             # Bad login details were provided. So we can't log the user in.
#             print "Invalid login details: {0}, {1}".format(username, password)
#             return HttpResponse("Invalid login details supplied.")
#
#     # The request is not a HTTP POST, so display the login form.
#     # This scenario would most likely be a HTTP GET.
#     else:
#         # No context variables to pass to the template system, hence the
#         # blank dictionary object...
#         return render(request, 'rango/login.html', {})


@login_required
def restricted(request):
    return render(request, 'rango/restricted.html', {})


# @login_required
# def user_logout(request):
#     # Since we know the user is logged in, we can now just log them out.
#     logout(request)
#
#     # Take the user back to the homepage.
#     return HttpResponseRedirect('/rango/')