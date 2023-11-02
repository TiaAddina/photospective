from PIL import Image
from PIL.ExifTags import TAGS


#   purpose:    Converts a given image (specified by path) to a small jpeg
#   args:
#               1 - Path to image that you want to resize and convert
#               2 - Max height you'd like to specify for the image
#   return:     None
#   sources:    I had trouble with Pillow stripping EXIF data when the save
#               method was called, so I researched it and found the resource
#               below:
#               https://stackoverflow.com/questions/17042602/
#         preserve-exif-data-of-image-with-pil-when-resizecreate-thumbnail
#
def to_small_jpeg(imagepath, maxlen):

    # Other than the EXIF-preservation technique, all other techniques used
    # here are from Pillow's documentation for the Image module:
    # https://pillow.readthedocs.io/en/stable/reference/Image.html

    # Open the image in a form Pillow can use
    img = Image.open(f'{imagepath}')

    # Convert the image to JPEG
    img.convert('RGB')

    # Resize the image according to the length specified, preserving aspect
    # (maxlen is a cap for the longest side of the image)
    img.thumbnail((maxlen, maxlen))

    # Prevent the save method from stripping away any EXIF data the image has
    try:
        img.save(f'{imagepath}', exif=img.info['exif'])
    except KeyError:
        img.save(f'{imagepath}')


#   purpose:    Given a local image file, fetches the EXIF data in a
#             human-readable form
#   args:
#               1 - Path to the image we'd like to extract EXIF data from
#   return:     Dictionary of key+value pairs containing the EXIF data
#   method:     Uses Pillow, which gets downloaded together with Django
#   notes:      Pillow's TAG dictionary translates the EXIF standard's numeric
#               ID's into more descriptive names like Lens, Camera, Make, etc.
#
#   sources:    Documentation on how to use Pillow to get EXIF data was
#               gathered from the following resource:
#               https://www.thepythoncode.com/article/
#               extracting-image-metadata-in-python
#
def get_exif_dict(imagepath):

    # Convert the locally-stored image to jpeg and resize it
    to_small_jpeg(f'{imagepath}', 800)

    # Open the preprocessed image in a form that Pillow can work with
    img = Image.open(f'{imagepath}')

    # Fetch the EXIF data that is available from the image
    img_exif = img.getexif()

    # Translate the native EXIF tag id's into their human-readable equivalents

    # Fresh dictionary to store translated pairs
    translated = {}
    for key, value in img_exif.items():
        # If the EXIF value is not binary, save the pair in the translate set
        # Why: We don't need bytes/binary data for Photospective's purposes
        if not isinstance(value, bytes) and key != None and value != None:
            # Dictionary how has a human-readable key with a string value
            translated[str(TAGS.get(key))] = str(value)

    # Return the dictionary of human-readable EXIF pairs
    return translated
