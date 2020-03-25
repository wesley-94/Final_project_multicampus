from flickrapi import FlickrAPI
import urllib.request
from PIL import Image
import sys
import time

key = 'b88ca2b24d6576e7f599262d39ee7369'
secret = 'b59f9d28f3c5543d'

# city_name = '' # input

def get_images(city_name):
    flickr = FlickrAPI(key, secret)
    photos = flickr.walk(text=city_name, tag_mode='all', tags=city_name, 
                            extras='url_c', per_page=50, sort='relevance')
    urls = []

    t0 = time.time()

    for i, photo in enumerate(photos):

        if i % 500 == 0:
            print(i)
            t1 = time.time()
            crawling_time = t1-t0
            print('%.2f' % crawling_time)
            t0 = time.time()

        try:
            url = photo.get('url_c')
            urls.append(url)

            # Download image from the url and save
            File_name = city_name+'_'+str(i)+'.jpg'
            urllib.request.urlretrieve(urls[i], File_name)

            # # Resize the image and overwrite it
            # image = Image.open(File_name)
            # image = image.resize((256,256), Image.ANTIALIAS)
            # image.save(File_name)
        except:
            print("Url for image number {} could not be fetched.".format(i))

        if i > 13000:
            break

    print(len(urls))

def main():
    city = sys.argv[1]
    get_images(city)

if __name__== '__main__':
    main()