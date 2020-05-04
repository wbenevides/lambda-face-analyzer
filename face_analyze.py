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


def compare_images(id_list):
    results = []
    for id in id_list:
        results.append(client.search_faces(
            CollectionId='faces',
            FaceId=id,
            MaxFaces=10,
            FaceMatchThreshold=80
        ))
    return results

def generate_data_json(compare_result):
    data_json = []
    for item in compare_result:
        face_matches = item.get('FaceMatches')
        if len(face_matches) >= 1:
            perfil = dict(name=face_matches[0]['Face']['ExternalImageId'],
                          faceId=face_matches[0]['Face']['FaceId'],
                          similarity=round(face_matches[0]['Similarity'], 2)
                          )
            data_json.append(perfil)
    return data_json


def deploy_data(data_json):
    file = s3.Object('wb-fa-site', 'data.json')
    file.put(Body=json.dumps(data_json))

detected_faces = detect_faces()
detected_id_list = create_detected_id_list(detected_faces)
compare_result = compare_images(detected_id_list)
data_json = generate_data_json(compare_result)
deploy_data(data_json)
print(json.dumps(data_json, indent=2))
