from django.urls import path
from . import views


urlpatterns = [

    # ... Path for the default homepage ... #
    path("", views.index, name="index"),


    # ... Paths for image management ... #
    path("img/upload", views.upload_view, name="upload"),
    path("img/all", views.tags_intersection_view, name="imgs_w_tags"),
    path("img/categories", views.all_categories_view, name="categories"),
    path("img/profile/<int:image_id>",
         views.single_image_view,
         name="img_profile"),


    # ... Paths for JSON resource management ... #
    path("json/tags4cat/<int:category_id>",
         views.tags_of_category_json,
         name="tags_categ_json"),


    # ... Paths for user account management ... #

    # These view functions below were taken from the "Network"
    # project (Project 4) from CSCI E-33A Fall 2020 :
    # https://cs50.harvard.edu/extension/web/2020/fall/projects/4/network/

    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register")
]
