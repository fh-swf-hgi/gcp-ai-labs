from google.cloud import vision
from PIL import Image, ImageDraw, ImageFont
from urllib import request
from urllib.request import Request, urlopen
import requests

client = vision.ImageAnnotatorClient()

def detect_objects(file, max_results=4):
    """Uses the Vision API to detect faces in the given file.

    Args:
        face: A file-like object containing an image.

    Returns:
        An array of objects.
    """
    client = vision.ImageAnnotatorClient()

    content = file.read()
    image = vision.Image(content=content)

    return client.object_localization(
        image=image, max_results=max_results).localized_object_annotations

def highlight_objects(image, objs, output_filename):
    """Draws a polygon around the objects, then saves to output_filename.

    Args:
      image: a file containing the image with the faces.
      faces: a list of faces found in the file. This should be in the format
          returned by the Vision API.
      output_filename: the name of the image file to be created, where the
          faces have polygons drawn around them.
    """
    im = Image.open(image)
    w,h = im.size
    draw = ImageDraw.Draw(im)
    for obj in objs:
        box = [(vertex.x*w, vertex.y*h)
               for vertex in obj.bounding_poly.normalized_vertices]
        draw.line(box + [box[0]], width=5, fill='#00ff00')
        # Place the confidence value/score of the detected faces above the
        # detection box in the output image
        #font = ImageFont.truetype("Arial.ttf",18)
        font = ImageFont.truetype("DejaVuSans.ttf",18)
        draw.text(((obj.bounding_poly.normalized_vertices)[0].x*w + 10,
                   (obj.bounding_poly.normalized_vertices)[0].y*h - 30),
                  str(format(obj.score, '.3f')) + '%',
                  font=font,
                  fill='#FF0000')
    im.save(output_filename)

def main(max_results):
    url = "https://images.pexels.com/photos/3932930/pexels-photo-3932930.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2"

    input_filename = 'image.jpeg'
    output_filename = 'image_annotated.jpeg'
    data = requests.get(url).content
    with open(input_filename,'wb') as f:
        f.write(data)

    with open(input_filename, 'rb') as image:
        objs = detect_objects(image, max_results)
        print('Found {} Object{}'.format(
            len(objs), '' if len(objs) == 1 else 's'))

        print(f'Writing to file {output_filename}')
        # Reset the file pointer, so we can read the file again
        image.seek(0)
        highlight_objects(image, objs, output_filename)


if __name__ == "__main__":
    main(8)
