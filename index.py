import boto3

s3 = boto3.resource('s3')

def list_images():
    images = []
    bucket = s3.Bucket('wb-fa-images')
    for image in bucket.objects.all():
        images.append(image.key)
    return images

images = list_images()