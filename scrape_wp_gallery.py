import argparse
import os
import time

import requests
import urllib3


class WpGalleryScraper:
  def __init__(self, site, images_directory=None, scrape_pause_seconds=3):
    self.site = site
    self.scrape_pause_seconds = scrape_pause_seconds
    if not images_directory:
      self.images_directory = os.path.expanduser('~/Documents/img/scraped_images')
    else:
      self.images_directory = images_directory

  def download_image(self, image_url):
    file_basename = os.path.basename(image_url)
    file_path = os.path.join(self.images_directory, file_basename)
    response = requests.get(image_url)

    if response.status_code == 200:
      with open(file_path, 'wb') as f:
        f.write(response.content)
      print(f'Downloaded {file_path}')

  def pull_image_records(self, image_ids):
    image_api = f'https://{self.site}/wp-json/wp/v2/media/'

    for image_id in image_ids:
      image_record_url = f'{image_api}{image_id}'
      print(f'Fetching {image_record_url}')

      response = requests.get(image_record_url)

      if response.status_code == 200:
        image_data = response.json()
        image_url = image_data['source_url']
        print(f'Image URL: {image_url}')

        # Download the image
        self.download_image(image_url)
      else:
        print(f'Failed to fetch image with ID {image_id}: {response.status_code}')

      time.sleep(self.scrape_pause_seconds)


if __name__ == '__main__':
  arparser = argparse.ArgumentParser()
  arparser.add_argument('site', help='The base URL of the wordpress site to scrape images from')
  arparser.add_argument('image_ids', help='Comma-separated list of image IDs to scrape')
  # default --images-directory to '~/Documents/img/scraped_images'
  arparser.add_argument(
    '--images-directory',
    help='Directory to save the downloaded images',
    default=os.path.expanduser('~/Documents/img/scraped_images')
  )

  args = arparser.parse_args()

  scraper = WpGalleryScraper(args.site, args.images_directory)
  scraper.pull_image_records(args.image_ids.split(','))
