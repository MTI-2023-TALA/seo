from typing import Dict
from bs4 import BeautifulSoup as bs
import requests
import re

class Heading:
  def __init__(self, name, text):
    self.name = name
    self.text = text
  
  def get_name(self):
    return self.name

  def get_text(self):
    return self.text

  def __str__(self):
    return self.name + ": " + self.text

url="http://www.prisma.io/docs/reference/api-reference/command-reference"
response = requests.get(url)
html = response.content
soup = bs(html, "lxml")


def get_title(soup):
    title = soup.find('title').string
    title_length = len(title)
    title_words = len(title.split(' '))
    return title

def get_meta_description(soup):
  description = soup.find("meta", property="og:description")
  if description:
    description_text = description.get("content")
    description_length = len(description_text)
    description_words = len(description_text.split(' '))
    return description_text
  else:
    return "No description"

def get_meta_keywords(soup):
  keywords = soup.find("meta", property="og:keywords")
  if keywords:
    return keywords.get("content")
  else:
    return "No keywords"

def get_url(soup):
  url = soup.find("meta", property="og:url")
  if url:
    url_text = url.get("content")
    url_length = len(url_text)
    return url_text
  else:
    return "No URL"

def get_structure(soup):
  headings = soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6"])

  formatted_headings = []
  for heading in headings:
    formatted_headings.append(Heading(heading.name, heading.text.strip()))
  return formatted_headings

def get_textual_content(soup):
  d = {}
  decoded_html = html.decode("utf-8")
  decoded_html_split = re.split('\\s+', decoded_html)

  for word in decoded_html_split:
    if word in d:
      d[word] += 1
    else:
      d[word] = 1

  sorted_most_used_words = []
  for k, v in sorted(d.items(), key=lambda kv: kv[1], reverse=True):
    sorted_most_used_words.append("%s => %s" % (k,v))
  return sorted_most_used_words[:10]

def get_other_content(soup):
  robots = soup.find("meta", property="og:robots")
  if robots:
    robots_text = robots.get("content")

  canonicals = soup.select('link[rel*=canonical]')
  if canonicals:
    canonicals_text = '\n'.join(canonical['href'] for canonical in canonicals)
  
  list_hreflangs = [[a['href'], a["hreflang"]] for a in soup.find_all('link', href=True, hreflang=True)]

  nb_images = soup.find_all('img')
  nb_images_text = len(nb_images)

  nb_images_alt = soup.find_all('img', alt=True)
  nb_images_alt_text = len(nb_images_alt)

  nb_images_no_alt_text = nb_images_text - nb_images_alt_text

  outbound_links = [[a.get_text(), a["href"]] for a in soup.find_all('a', href=True)]
  outbound_links_text = len(outbound_links)