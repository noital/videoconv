from flask import Flask, request, jsonify, redirect
from flask.logging import create_logger
from moviepy.editor import VideoFileClip
from faker import Faker
import logging
import boto3
import os


app = Flask(__name__)
LOG = create_logger(app)
LOG.setLevel(logging.INFO)
bucketName = os.environ['BUCKET']
#bucketUrl = boto3.client('s3').get_bucket(Bucket=bucketName)
LOG.info(f'bucketName: {bucketName}')
#LOG.info(f'bucketUrl: {bucketUrl}')
faker = Faker()

def create_html(filename):
    return """<html>
        <video width="320" height="240" controls>
            <source src="video/""" + filename + """" type="video/webm">
          Your browser does not support the video tag.
          </video> 
    </html>"""


@app.route("/convert", methods=['POST'])
def convert():
    uploaded_file = request.files['upload']
    fileName = ''.join(faker.words(3))
    LOG.info(f'original filename: {uploaded_file.filename}')
    LOG.info(f'random filename: {fileName}')
    uploaded_file.save('temp/'+fileName+'.src')
    
    html_file = open('temp/' + fileName + '.html', "w")  
    html_file.write(create_html(fileName+'.webm'))
    html_file.close()
    video = VideoFileClip('temp/' + fileName + '.src')
    video.write_videofile('temp/' + fileName + '.webm')
    
    boto3.resource('s3').Bucket(bucketName).upload_file(Filename='temp/' + fileName+'.webm', Key='video/'+fileName+'.webm')
    boto3.resource('s3').Bucket(bucketName).upload_file(Filename='temp/' + fileName+'.html', Key=fileName+'.html')
    return redirect(fileName+'.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True) # specify port=80
