# Photospective
### by Tia Addina Binti Mohd Razif 
#### for CSCI E-33A's Final Project

## Brief
Photospective provides a web-based interface for exploring the EXIF metadata available in uploaded JPEG images. It is intended to be a constrained, specific tool to help photographers explore how they take pictures so that they can iteratively improve their skills and techniques.

In brief, the process of EXIF-tag exploration comes in the following two forms:
1. By clicking on hyperlinked EXIF values to see all the images that conform to that setting as well. 
   1. For example, clicking on the "55mm" value for the "FocalLength" EXIF tag/category will render all of the images taken with that focal length.
   2. All EXIF values that appear on the site can be clicked to filter through the user's uploads in this manner.
2. By specifying a collection of tags to filter the images through using "AND" logic.
   1. For example, you can combined "FocalLength: 55mm" and "Model: NIKON D7000" to get all uploaded images that were taken with a Nikon D7000 camera using a 50mm lens.
   2. This feature is supported on the frontend using a simple, session-persistent "staging" area that appears in at the top of the page.
      1. Users can go from image to image or jump between images and the category page to curate a list of tags to filter their images by, then they can execute the search. As long as the user stays in the same browser tab and does not log out, the list will be available until the user is ready to execute the search.

## Features

1. User Account Creation
   1. Users can create their own accounts where they can manage and explore their own image galleries
      1. Users cannot view the tags, categories, and images of other registered users
   2. Citation Note: All account-creation and authentication features are based on the distribution code for the "Network" project from Fall 2020 of CSCI E-26: https://cs50.harvard.edu/extension/web/2020/fall/projects/4/network/. These parts are cited throughout the source files.

2. File Uploads
   1. Users can upload images of any type, but the EXIF parser works most reliably with JPEG images.
      1. When images are uploaded, they are resized and converted to JPEG before any EXIF parsing is done.
      2. When images are uploaded and the EXIF dictionary is fetched, the EXIF tags and values will be added to the database.
         1. NOTE: See model design information under "Files Added" for details on how redundancy has been minimized.
   
3. EXIF Exploration
   1. There are two types of data with which users filter images:
      1. EXIF Tags, also referred to as Categories (these include "FocalLength", "Model", "Make", etc.)
      2. EXIF Values (these include "55mm", "NIKON D7000", "Nikon Corporation")
   2. Throughout the website...
      1. <b>EXIF tags/categories</b> are rendered as <b>buttons</b> that can be clicked to reveal a drop-down-like container containing all of the values available for that tag/category
      2. <b>EXIF values</b> are rendered as two parts:
         1. Their text are hyperlinks that, when clicked, renders all of the images that satisfy that given value
         2. However, to the left of the text, wherever the EXIF values appear in tables or under categories, there will be a small "➕" sign that can be clicked to add that tag to the "query staging area". This is a box at the top where users can collect their filters before executing them.
   3. The main exploration tool is the query staging area:
      1. This list persists even if the user clicks on a tag value link, on an image, or navigates to another page on the site. This makes it easier for the user to select what they want to explore.
      2. Once the user is ready to filter their images, they can click the "Execute Query" button to find the images forming the intersection set of all the selected tag values.
      3. The list will only be cleared in the following situations:
         1. Once the execute query button is clicked
         2. Once the user logs out, logs in, or registers
         3. Once the browser tab is closed
   4. The homepage renders all of the user's uploads
4. Mobile-responsiveness:
   1. Simple mobile-responsiveness has been added via Bootstrap and CSS media queries

## Files Added
1. In the SurfExif app:
   1. forms.py
      1. Included a ModelForm for uploading images, Django documentation sources cited in file
   2. helpers.py
      1. Two functions to facilitate parsing EXIF data from image files
         1. One function handles file pre-processing like EXIF-extraction, JPEG conversion, and resizing.
         2. The other function translates a numerical dictionary to a human-readable dictionary
   3. models.py
      1. User
         1. No changes to the base AbstractUser class
      2. Image
         1. Stores the filepath, uploader, and time uploaded
      3. Tag
         1. Stores the EXIF value of a given EXIF tag/category
         2. Since there will always be more tag values than categories, the categories are stored in another table/model
         3. Each tag is associated with one category via a ForeignKey 
      4. Category
         1. Stores the name of a category and nothing else
   4. urls.py
   5. views.py
      1. Other than the view functions used to update Models, render pages, and return JSON data, views.py also includes the "add_db_tags" helper function for adding EXIF tags/categories and EXIF values to the database.
         1. The "add_db_tags" function is slightly sophisticated as it needs to make decisions about whether to make new Tag or Category objects based on the EXIF data of an image: Most of the time, I would be creating new Tag objects since tag values often vary a lot, but sometimes I've already saved the Tag (e.g. the "MeteringMode" category can only have so much variation in its values). I would have to take care to handle these updates properly so that the database only holds as much information as it actually needs to make the website work, and no more. 
   6. "surfexif/media/uploads/" directory
      1. This is where all uploaded and resized images are stored in the form of media/uploads/user_id, e.g. the user with the ID of 3 would have all their images stored in media/uploads/user_3
   

## Files Changed
1. Global settings.py and urls.py for the Django project had to be tweaked slightly to specify how and where uploaded media gets saved. Django documentation sources cited in file.

## Future Enhancements :)
1. It would be awesome to use FormSets in the upload file phase so that multiple images can be uploaded at once
2. Being able to delete uploaded images (from both the static storage and from the database) would also be a good feature
3. Being able to remove tags from the query staging area after they have been added but before the query is executed would be very useful
   

## Security Issues
1. The use of SessionStorage over LocalStorage mitigates some security leaks by ensuring that user data isn't kept for very long, but it's fairly easy to tweak the Javascript so that SessionStorage is not cleared when user logs out. This can then allow for other users to have access to at least the category and tag IDs of other users' images, even if Django explicitly disallows access to Media files unless directly passed through a view context.
