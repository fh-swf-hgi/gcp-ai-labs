from google.cloud import vision
from PIL import Image, ImageDraw, ImageFont
from urllib import request
from urllib.request import Request, urlopen
import requests

client = vision.ImageAnnotatorClient()

def detect_face(face_file, max_results=4):
    """Uses the Vision API to detect faces in the given file.

    Args:
        face_file: A file-like object containing an image with faces.

    Returns:
        An array of Face objects with information about the picture.
    """
    client = vision.ImageAnnotatorClient()

    content = face_file.read()
    image = vision.Image(content=content)

    return client.face_detection(
        image=image, max_results=max_results).face_annotations

def highlight_faces(image, faces, output_filename):
    """Draws a polygon around the faces, then saves to output_filename.

    Args:
      image: a file containing the image with the faces.
      faces: a list of faces found in the file. This should be in the format
          returned by the Vision API.
      output_filename: the name of the image file to be created, where the
          faces have polygons drawn around them.
    """
    im = Image.open(image)
    draw = ImageDraw.Draw(im)
    for face in faces:
        box = [(vertex.x, vertex.y)
               for vertex in face.bounding_poly.vertices]
        draw.line(box + [box[0]], width=5, fill='#00ff00')
        # Place the confidence value/score of the detected faces above the
        # detection box in the output image
        #font = ImageFont.truetype("Arial.ttf",56)
        font = ImageFont.truetype("DejaVuSans.ttf",56)
        draw.text(((face.bounding_poly.vertices)[0].x + 10,
                   (face.bounding_poly.vertices)[0].y + 40),
                  str(format(face.detection_confidence, '.3f')) + '%',
                  font=font,
                  fill='#FF0000')
    im.save(output_filename)

def main(max_results):
    url = "https://images.pexels.com/photos/1037989/pexels-photo-1037989.jpeg"

    input_filename = 'image.jpeg'
    output_filename = 'image_annotated.jpeg'
    data = requests.get(url).content
    with open(input_filename,'wb') as f:
        f.write(data)

    with open(input_filename, 'rb') as image:
        faces = detect_face(image, max_results)
        print('Found {} face{}'.format(
            len(faces), '' if len(faces) == 1 else 's'))

        print(f'Writing to file {output_filename}')
        # Reset the file pointer, so we can read the file again
        image.seek(0)
        highlight_faces(image, faces, output_filename)


if __name__ == "__main__":
    main(8)
