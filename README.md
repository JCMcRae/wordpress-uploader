# wordpress-uploader
Lightweight Code for Wordpress Image Uploading

The code in these files are some of the lines used in CYSTech `PLNR`, the proprietary content upload and management tool I built to schedule and automate content for the Clean Your Shoes blog (on WordPress) and Instagram.

#### THIS IS NOT A WORKING PROGRAM/APP. This is open-source code from a proprietary app.

Currently, the tool is built to only support the uploading of images (`application/octet-stream`), but you can use this code to upload other forms of media as well.


### How it works
`imaging.start_upload` is the main starting point for the content planning application. In my app, it takes a boolean from the CLI menu (powered by `Typer`), `multiple_files`. Either way, it will prompt you to select the images from an external images folder to be copied into the program's internal images folder. It will also prompt you to create a caption, and to schedule a time to post the content on IG. (The schedule part here is irrelevant, as this is only the code that uploads the images to Wordpress.)

If you've opted to upload a single image, then `start_upload` will call `upload_raw_data_to_wordpress`, which takes in the `RawData` object built by the `start_upload` method to send the image and relevant image data to WordPress, via `upload_media_to_wordpress`. A `WordPressResponse` object will then be returned with the response returned by Wordpress.

For multiple images, `start_upload` will create a "collection" (read: array) of `RawData` objects containing the relevant image data from the multiple images you've selected to uplaod. For some reason, the new WordPress API does not handle uploading multiple files at once as advertised in their API documentation, so `upload_multiple_raw_data_to_wordpress` calls `upload_media_to_wordpress` as many times as necessary to upload all the selected photos. This will return an array of data, which `upload_multiple_raw_data_to_wordpress` will take and turn into `WordPressResponse` objects and return whether or not all images were successfully uploaded.

`get_wordpress_media` will simply return all a list of the 20 most recent images/media files you have uploaded to your WordPress.

This code is free and open-source. I simply ask that you give proper credits when using this code.
