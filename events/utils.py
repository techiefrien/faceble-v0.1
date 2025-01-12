from datetime import datetime, date

def date_difference(start_date: str, n: int):
    # Get the current date
    current_date = date.today()  # Returns a datetime.date object
    
    # Ensure start_date is a string before parsing
    if isinstance(start_date, date):
        start_date = start_date.strftime("%Y-%m-%d")  # Convert to string
    
    # Convert the start_date string to a datetime.date object
    start_date_obj = datetime.strptime(start_date, "%Y-%m-%d").date()
    
    # Calculate the difference in days
    diff = (current_date - start_date_obj).days
    
    # Check if the difference is greater than or equal to n
    if diff >= n:
        return False
    else:
        return diff




from io import BytesIO
from PIL import Image
from django.core.files.base import File

def compress_image(image):
    # Create a BytesIO object
    im_io = BytesIO()

    # Open the image
    img = Image.open(image)

    # Convert to RGB (if not already in RGB mode)
    img = img.convert('RGB')

    # Save the image to BytesIO, removing metadata
    img.save(im_io, format='JPEG', optimize=True, quality=30)

    # Create a Django File object
    comp_img = File(im_io, name=image.name)

    return comp_img
