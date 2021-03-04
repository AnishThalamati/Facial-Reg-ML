import boto3
from tkinter import messagebox
from ImageMatcher.awsutils import *

rek_client = boto3.client('rekognition')

photo = "basedataset/download-1.jpg"

def compare_face(new_image, old_image):
    response = rek_client.compare_faces(
        SourceImage={
            'S3Object': {
                'Bucket': 'anishimages1',
                'Name': new_image # user input
            }
        },
        TargetImage={
            'S3Object': {
                'Bucket': 'anishimages1',
                'Name': old_image # existing image
            }
        },
    )
    return response


def compare_faces(image_list, user_image):
    for target_image in image_list:
        print("Matching with:", target_image)
        response = compare_face(user_image, target_image)
        face_matches = response['FaceMatches']
        if face_matches:
            print("MATCHED WITH:", target_image)
            messagebox.showinfo("Matched with:", target_image)
            return target_image
    print("NO MATCH")
    return ""
