import boto3

s3 = boto3.resource('s3')
client = boto3.client('rekognition')


def list_images():
    images = []
    bucket = s3.Bucket('wb-fa-images')
    for image in bucket.objects.all():
        images.append(image.key)
    return images


def index_images(images):
    for i in images:
        response = client.index_faces(
            CollectionId='faces',
            Image={
                'S3Object': {
                    'Bucket': 'wb-fa-images',
                    'Name': i
                }
            },
            ExternalImageId=i[:-4],
            DetectionAttributes=[]
        )

images = list_images()
index_images(images)
