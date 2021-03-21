import argparse
import json
import logging
import requests
import sys
from urllib.parse import urlparse

logging.basicConfig(format='%(levelname)s: %(message)s')

def command_line_args():
  parser = argparse.ArgumentParser('Start remote CodeCompass parsing')

  parser.add_argument(
    '-u', '--user',
    required=True,
    help='Jenkins user name')

  parser.add_argument(
    '-t', '--token',
    required=True,
    help='User token on Jenkins')

  parser.add_argument(
    '-j', '--job',
    required=True,
    help='Jenkins job name')

  parser.add_argument(
    '-n', '--name',
    required=True,
    help='Project name')

  parser.add_argument(
    '-z', '--zip',
    required=True,
    help='Path of .zip file containing the analyzed project')

  parser.add_argument(
    '--url',
    required=True,
    type=urlparse,
    help='URL of Jenkins server')

  return parser.parse_args()

def check_url(url):
  """
  This function checks if the given URL is a proper candidate for remote
  CodeCompass parsing. The URL must contain http:// or https:// scheme
  otherwise post request can't be made.
  The function also warns about the fact that the "path" part of the URL will
  not be used by the script.
  """
  if not url.netloc or not url.scheme:
    logging.error('Invalid URL')
    logging.error('Consider using http:// or https://')
    return False

  if url.path:
    logging.warning('URL path will be ommitted: %s', url.path)

  return True

def get_crumb_header(args):
  """
  Latest versions of Jenkins require a crumb which identifies the authorized
  user during a REST API request to Jenkins. The function returns a tuple of
  HTTP header field name and the crumb. The header must be set with this field
  name and the crumb as its value.
  In case of any network errors this function returns None.
  """
  try:
    response = requests.post(
      f'{args.url.scheme}://{args.url.netloc}/crumbIssuer/api/json',
      auth=(args.user, args.token))
  except requests.exceptions.InvalidSchema as ex:
    logging.error(ex)
    logging.error('Make sure to add http:// or https:// in the URL')
    return
  except requests.exceptions.ConnectionError as ex:
    logging.error(ex)
    return

  if response.status_code != 200:
    logging.error('(401) Unauthorized user')
    return

  content = json.loads(response.content)

  return content['crumbRequestField'], content['crumb']

def start_jenkins_job(args):
  """
  This function triggers a given Jenkins job. A .zip file given as command line
  argument is uploaded to this job as parameter.
  """
  crumb_header = get_crumb_header(args)

  if not crumb_header:
    return False

  requests.post(
    f'{args.url.scheme}://{args.url.netloc}'
    f'/job/{args.job}/buildWithParameters',
    auth=(args.user, args.token),
    headers={crumb_header[0]: crumb_header[1]},
    files={'source': open(args.zip, 'rb')},
    data={'project_name': args.name})

  return True

def main():
  args = command_line_args()

  if not check_url(args.url):
    sys.exit(1)

  if not start_jenkins_job(args):
    sys.exit(1)

if __name__ == '__main__':
  main()
