#!/usr/bin/env python
import os, errno
import openai
import urllib.request
from datetime import datetime

from pprint import pprint

# Load your API key from an environment variable or secret management service
# Generate api key here: https://beta.openai.com/account/api-keys
openai.api_key = os.getenv("OPENAI_API_KEY")

out_dir = 'out'
out_sentences_requested = 'sentences.txt'

input_str = ''
image_size = '1024x1024'
image_sizes = ['256x256', '512x512', '1024x1024']

# Start a loop that will run until the user gives input
while True:
    input_str = input("Enter your request: ")

    if input_str:
      print("Sentence requested: {}".format(input_str))
      
      input_image_size = input("Enter your image size (available sizes: '256x256', '512x512', [default] '1024x1024'): ")
      if input_image_size and input_image_size in image_sizes:
        image_size = input_image_size
      
      print("Current image size: {}".format(image_size))

      try:
        response = openai.Image.create(
          prompt=input_str,
          n=1,
          size=image_size
        )

        image_url = response['data'][0]['url']
        print("Image url response: {}".format(image_url))

        try:
            os.makedirs(out_dir)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

        # current date and time
        now = datetime.now()
        now_str = now.strftime("%Y%m%d%H%M%S")

        output_str = "out/{}-{}_{}.png".format(input_str.replace(' ', '_'), image_size, now_str)

        urllib.request.urlretrieve(image_url, output_str)

        sentences_file = "{}/{}".format(out_dir, out_sentences_requested)
        with open(sentences_file,'a') as sf:
          sf.write('{}: {}\n'.format(now_str, input_str))

      except openai.error.InvalidRequestError as err:
        print("Invalid Request Error: {}".format(err))
      except:
        print("Something else went wrong")
        
      break
