import os
import openai
import urllib.request
import errno
from datetime import datetime

# Load your API key from an environment variable or secret management service
# Generate api key here: https://beta.openai.com/account/api-keys

openai.api_key = ('Your API Key Here')

# Constants for the output directory and output file for sentences
OUT_DIR = 'out'
OUT_SENTENCES_FILE = 'sentences.txt'

# List of available image sizes
IMAGE_SIZES = ['256x256', '512x512', '1024x1024']

def generate_image(prompt, size):
    """Generates an image using the OpenAI API based on the given prompt and size.
    
    Returns the URL of the generated image.
    """
    response = openai.Image.create(
        prompt=prompt,
        n=1,
        size=size
    )
    return response['data'][0]['url']

def save_image(url, filename):
    """Saves the image at the given URL to the specified filename.
    """
    with open(filename, "wb") as f:
        f.write(urllib.request.urlopen(url).read())

def save_sentence(sentence):
    """Saves the given sentence to the output file for sentences.
    """
    # Create the output directory if it does not exist
    try:
        os.makedirs(OUT_DIR)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

    # Append the sentence to the output file
    with open(f"{OUT_DIR}/{OUT_SENTENCES_FILE}", 'a', encoding="utf-8") as sf:
        sf.write(f"{datetime.now().strftime('%Y%m%d%H%M%S')}: {sentence}\n")

def main():
    while True:
        prompt = input("Enter your request: ")
        if prompt:
            print(f"Sentence requested: {prompt}")

            # Prompt the user for an image size
            size = input("Enter your image size (available sizes: '256x256', '512x512', [default] '1024x1024'): ")
            if size and size in IMAGE_SIZES:
                image_size = size
            else:
                # Default to 1024x1024 if no size is provided or if the provided size is invalid
                image_size = '1024x1024'
            print(f"Current image size: {image_size}")

            try:
                # Generate the image
                image_url = generate_image(prompt, image_size)
                print(f"Image url response: {image_url}")

                # Save the image and the sentence to the output directory
                filename = f"{OUT_DIR}/{prompt.replace(' ', '_')}-{image_size}_{datetime.now().strftime('%Y%m%d%H%M%S')}.png"
                save_image(image_url, filename)
                save_sentence(prompt)
            except openai.error.InvalidRequestError as err:
                print(f"Invalid Request Error: {err}")
            except Exception as e:
                print(f"Something else went wrong: {e}")

            break


if __name__ == "__main__":
    main()