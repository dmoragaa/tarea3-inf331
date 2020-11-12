import boto3
import re
import argparse

def credentials():
  
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument('-i', '--awsid', type=str, required=True)
    parser.add_argument('-k', '--awskey', type=str, required=True)

    return parser.parse_args()

def detect_text(photo, bucket, credentials):

    client = boto3.client(
        'rekognition',
        aws_access_key_id=credentials.awsid,
        aws_secret_access_key=credentials.awskey
    )

    response=client.detect_text(Image={'S3Object':{'Bucket':bucket,'Name':photo}})
                        
    textDetections=response['TextDetections']

    return textDetections

def comparar(textDetect0, textDetect1):
    words0 = [] #palabras en la imagen de control
    words1 = [] #palabras en la imagen a comparar
    
    
    for text in textDetect0:
        if (" " in text['DetectedText']):
            aux = text['DetectedText'].split()
            for palabra in aux:
                words0.append(palabra.lower())
        else:
            words0.append((text['DetectedText']).lower()) #agregar palabra por palabra en minúscula

    for text in textDetect1:
        if (text['Confidence'] < 97.0): #verificar que cada confidence sea mayor al 97%
            print("La detección de la palabra " + text['DetectedText'] + " es menor a 97%")
            return False
        if (" " in text['DetectedText']):
            aux = text['DetectedText'].split()
            for palabra in aux:
                words1.append(palabra.lower())
        else:
            words1.append((text['DetectedText']).lower()) #agregamos palabra por palabra en minúscula

    for word in words1:
        new_word = re.sub(r'[!@#$%^&*()\./<>?|`_+]', '', word)
        if (word != new_word):
            i = words1.index(word)
            words1[i] = new_word

    #verificar si todas las palabras de words0 están en words1
    for word in words0:
        if (word not in words1):
            return False
    return True

def main():

    bucket=str(input("Ingrese nombre del bucket: "))
    photo0=str(input("Ingrese nombre de imagen de control: "))

    photo1=str(input("Ingrese nombre de imagen de prueba: "))

    cred = credentials()

    text_count0=detect_text(photo0, bucket, cred)
    text_count1=detect_text(photo1, bucket, cred)

    print (comparar(text_count0, text_count1))

if __name__ == "__main__":
    
    main()