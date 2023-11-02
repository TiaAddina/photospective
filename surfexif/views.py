# Django-related imports from "Network" project's distribution code
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse

# My own Django-related imports
from django.contrib.auth.decorators import login_required
from .models import User, Image, Tag, Category
from .forms import ImageForm
from django.core.exceptions import ObjectDoesNotExist

# My own custom imports (for utility functions, helper functions, etc.)
from .helpers import get_exif_dict


# View function for rendering the images that satisfy a list of given tags
@login_required
def tags_intersection_view(request):

    # Start with the list of all of the user's uploads
    user_imgs = User.objects.get(id=request.user.id).images_uploaded.all()

    # Initialize an empty queryset to store results of intersection
    qs_reduced = Image.objects.none()

    # Iterate through given "t" GET parameters,
    for tag_id in request.GET.getlist('t'):

        # Test if the given "t" parameter is an integer
        try:

            # Check if tag exists in the database
            tag = get_object(Tag, int(tag_id))

            # If the tag exists in the database,
            if tag:

                # Create a queryset of all the user's images with that tag
                qset = user_imgs.filter(tags_with_image__id=tag.id)

                # If the intersection set is not empty,
                # intersect it with the new queryset
                if qs_reduced:
                    qs_reduced = qs_reduced.intersection(qset)

                # Else if intersection set is empty,
                # intialize its contents with the user's images for the
                # first valid tag
                else:
                    qs_reduced = qset

        # If "t" parameter is not an integer (and therefore not valid)
        # move on to the next parameter
        except:
            continue

    # Render a list of images that is the intersection of the tags passed
    return render_image_list(request, qs_reduced)


# View function for rendering the homepage and personal gallery
def index(request):

    # If the user is logged in, show them the homepage
    if request.user.is_authenticated:

        # Get the queryset for all of the user's uploaded images
        user_uploads = Image.objects.filter(uploader=f'{request.user.id}')

        # Render the images
        return render_image_list(request, user_uploads)

    # Else show them the login page
    else:
        return HttpResponseRedirect(reverse('login'))


# View function for rendering a single image with its full EXIF profile
@login_required
def single_image_view(request, image_id):

    # Try to get the requested image
    requested_img = get_object(Image, image_id)

    # If the image exists and the user is the one who uploaded it,
    if requested_img and (requested_img.uploader.id == request.user.id):
        # Wrap the image in a list
        # This is needed because our templates iterate through a list
        # of images, so this just creates a list of one image
        images = [requested_img]
    else:
        images = []

    # Render the full profile for the image
    return render_image_list(request, images)


# View function for uploading an image file and updating database
# records for tags and categories
# Loosely based on Django's documentation for file uploads via ModelForms:
# https://docs.djangoproject.com/en/3.1/topics/http/file-uploads/
@login_required
def upload_view(request):

    # If the user is trying to upload an image,
    if request.method == 'POST':

        # Capture the form from the request
        form = ImageForm(request.POST, request.FILES)

        # Check that the form contains an image
        if form.is_valid():

            # Pre-process image object before saving
            image = form.save(commit=False)

            # Add uploader id to image object
            image.uploader = User.objects.get(pk=request.user.id)

            # Save the image object to the database
            form.save()

            # Add the image's tags and categories to the database
            exif_dict = get_exif_dict(image.imagepath.path)
            db_add_tags(exif_dict, image)

            # Go back to the homepage once file has been saved
            return default_redirect()

    # If the user is not trying to upload a file,
    else:

        # then render a fresh image upload form for the page
        form = ImageForm()

    # When we visit the "upload" url, render the appropriate version
    # of the upload image form
    return render(request, 'surfexif/upload.html', {'form': form})


# JSON function for rendering the tags under a chosen category
@login_required
def tags_of_category_json(request, category_id):

    # Search for the category
    category = get_object(Category, category_id)

    # Check if the category exists and is a category the user can access
    if category and category in get_personal_categories(request):

        # https://stackoverflow.com/questions/15874233/output-django-queryset-as-json
        tags_dict = list(category.tags_with_category.filter(images__uploader=request.user.id).distinct().values())
        return JsonResponse(tags_dict, safe=False)

    # If category does not exist, redirect to default homepage
    else:
        return JsonResponse({'error': 'Category does not exist.'})


# View function for rendering the "all categories page"
def all_categories_view(request):

    # Fetch all of the categories that the user has access to
    categories = get_personal_categories(request)

    return render(request, 'surfexif/outline_tree.html', {
                # The category button needs an image id for JS selection,
                # so thats why we need to pass in a default id so that
                # the category buttons can be rendered in the same way it is
                # rendered everywhere else
                           'imageid': 1,
                           'categories': categories
                           })


# Login view function was taken from the "Network" project (Project 4) from
# CSCI E-33A Fall 2020 :
# https://cs50.harvard.edu/extension/web/2020/fall/projects/4/network/
def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "surfexif/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "surfexif/login.html")


# Logout view function was taken from the "Network" project (Project 4) from
# CSCI E-33A Fall 2020 :
# https://cs50.harvard.edu/extension/web/2020/fall/projects/4/network/
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


# Register view function was taken from the "Network" project (Project 4) from
# CSCI E-33A Fall 2020 :
# https://cs50.harvard.edu/extension/web/2020/fall/projects/4/network/
def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "surfexif/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "surfexif/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "surfexif/register.html")


# Helper function to add tags and tag categories to database
def db_add_tags(exif_data, image_obj):
    # Iterate through the tags and tag-categories for the image to add
    # non-duplicates to the database
    for key, value in exif_data.items():

        # Add the category to the database if it doesn't already exist,
        # else fetch the pre-existing matching category object
        cat = Category.objects.get_or_create(descriptor=key)

        # Add the tag to the database if it doesn't already exist,
        # else fetch the pre-existing tag
        # Note: This get_or_create will search for unique pairs of
        # descriptor and category, not just unique descriptors
        tag = Tag.objects.get_or_create(descriptor=value, category=cat[0])

        # Once tag object is saved/confirmed to exist, associate the image
        # with the tag
        tag[0].images.add(image_obj)


# Convenience function for redirecting to default homepage route
def default_redirect():
    return HttpResponseRedirect(reverse('index'))


# Convenience helper function to check if an item exists in the database
def get_object(obj_model, obj_id):
    try:
        return obj_model.objects.get(id=obj_id)
    except ObjectDoesNotExist:
        return None


# Convenience function for creating HTTPResponse object from a given
# list of images and rendering it with the default template
def render_image_list(request, images):

    return render(request, 'surfexif/index.html', {
            'images': images
    })


# Convenience function for getting the list of categories that
# are derived from images that are uploaded by the user
def get_personal_categories(request):

    # Use deep search to filter through the category model
    return Category.objects.filter(tags_with_category__images__uploader=request.user.id).distinct()
