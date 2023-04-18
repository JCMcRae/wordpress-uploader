import json
import os
import shutil

from PIL import Image
import glob

from your_python_package import ERRORS, WP_UPLOAD_ERROR, wp

EXTERNAL_IMAGES_DIRECTORY = glob.glob("your/external/folder/here")
IMAGES_DIRECTORY = "your/internal/images/folder"


# TODO: Reformat Raw Data Class.
# This class is a lightweight class to keep the filename, caption, and `scheduler` data in one neat form.
class RawData:
    def __init__(self, filename, caption, schedule):
        self.filename = filename
        self.caption = caption
        self.schedule = schedule

# This is a lightweight class meant to handle response data.
class WordpressResponse:
    def __init__(self, response):
        self.json = response.json()
        self.media = self.json["media"][0]
        self.upload_id = self.media['ID']
        self.image_location = self.media['URL']

    def is_successful(self):
        if isinstance(self.upload_id, int) and self.upload_id > 0:
            print("Upload to WordPress successful: Upload ID#" + str(self.upload_id))
            return True
        else:
            print(ERRORS.get(WP_UPLOAD_ERROR))
            return False


def start_upload(multiple_files):
    filename_list = []

    for filename in EXTERNAL_IMAGES_DIRECTORY:
        base_name = os.path.basename(filename)
        print(f"{EXTERNAL_IMAGES_DIRECTORY.index(filename) + 1}: {base_name}")

        filename_list.append(filename)

    if multiple_files:
        print("You may select up to 10 media items.")
        print("Make your selections with a space apart. e.g. 0 1 2 3 4...")
        caption = str(input("Caption: "))
        image_indices = str(input("Select Image indices: ")).split(" ")
        minute = str(input("Minute (default 0): "))
        hour = str(input("Hour (default 0): "))
        day_of_the_week = str(input("Day Of The Week (default monday): "))
        schedule = get_schedule_data(minute, hour, day_of_the_week)
        collection = []

        print("Copying files from external folder...")
        for index in image_indices:
            shutil.copy(filename_list[int(index) - 1], IMAGES_DIRECTORY)
            collection.append(RawData(filename_list[int(index) - 1], caption, schedule))
        print("Copied file from external folder to project folder.")

        for image in collection:
            print(image.filename)
        upload_multiple_raw_data_to_wordpress(collection)
    else:
        image_index = int(input("Select Image: ")) - 1
        caption = str(input("Caption: "))

        print("Copying file from external folder...")
        shutil.copy(filename_list[image_index], IMAGES_DIRECTORY)
        print("Copied file from external folder to project folder.")

        minute = str(input("Minute (default 0): "))
        hour = str(input("Hour (default 0): "))
        day_of_the_week = str(input("Day Of The Week (default monday): "))
        schedule = get_schedule_data(minute, hour, day_of_the_week)

        upload_raw_data_to_wordpress(RawData(filename_list[image_index], caption, schedule))


def upload_raw_data_to_wordpress(raw_data):
    caption = raw_data.caption

    print("Uploading " + raw_data.filename + " to WordPress...")

    response = WordpressResponse(wp.upload_media_to_wordpress(raw_data))

    return response.is_successful()


def upload_multiple_raw_data_to_wordpress(collection):
    upload_data = wp.upload_multiple_media_to_wordpress(collection)
    successful_uploads = []
    upload_errors = []
    all_successful = True

    for upload in upload_data:
        response = WordpressResponse(upload)
        if response.is_successful():
            successful_uploads.append(response)
        else:
            upload_errors.append(response)
            all_successful = False

    if all_successful:
        return "All images successfully uploaded"
    else:
        return f"There was an error with the following upload(s): {upload_errors}"


def get_schedule_data(minute, hour, day):
    return [minute, hour, day]
