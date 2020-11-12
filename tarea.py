import boto3
import re
import argparse
from datetime import datetime

confidence = 90.0

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

def comparar(textDetect0, textDetect1, log):
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
        if (text['Confidence'] < confidence): #verificar que cada confidence sea mayor al parámetro
            print("La detección de la palabra " + text['DetectedText'] + " es menor a "+ str(confidence) +"% \n")
            log.write("La detección de la palabra " + text['DetectedText'] + " en la imagen de prueba es menor a "+ str(confidence) +"% \n")
            log.write("--------------------------------------------------------------------------------------------- \n")
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
    flag = True
    for word in words0:
        if (word not in words1):
            return flag
    log.write("Resultado: "+ str(flag) +"\n")
    log.write("-----------------------------------------------------------------------------------------\n")
    return flag

def main():
    log = open("logs.txt","a")
    now = datetime.now()
    now = str(now)

    bucket=str(input("Ingrese nombre del bucket: "))
    photo0=str(input("Ingrese nombre de imagen de control: "))

    photo1=str(input("Ingrese nombre de imagen de prueba: "))

    log.write(now + ",   IMG control: "+ photo0 + ",  IMG prueba: "+ photo1+"\n")

    cred = credentials()

    text_count0=detect_text(photo0, bucket, cred)
    text_count1=detect_text(photo1, bucket, cred)

    print (comparar(text_count0, text_count1, log))
    log.close()

if __name__ == "__main__":
    
    main()