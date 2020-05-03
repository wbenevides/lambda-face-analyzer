import boto3
import json

s3 = boto3.resource('s3')
client = boto3.client('rekognition')

def detect_faces():
    detected_faces = client.index_faces(
        CollectionId='faces',
        Image={
            'S3Object': {
                'Bucket': 'wb-fa-images',
                'Name': '_analyze.png'
            }
        },
        ExternalImageId='TEMP',
        DetectionAttributes=['DEFAULT']
    )
    return detected_faces

def create_detected_id_list(detected_faces):
    id_list = []
    for face in detected_faces['FaceRecords']:
        id_list.append(face['Face']['FaceId'])

    return id_list


detected_faces = detect_faces()
detected_id_list = create_detected_id_list(detected_faces)
print(detected_id_list)