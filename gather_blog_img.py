import re, os, requests, shutil
import base64
import time
from itertools import chain

from requests.adapters import HTTPAdapter
from urllib3 import Retry

img_patten = r'!\[.*?\]\((.*?)\)+|<img.*?src=[\'\"](.*?)[\'\"].*?>'
token = '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'


def download_img(url, asset_folder):
    print(url)
    # download the image
    session = requests.Session()
    retry = Retry(connect=3, backoff_factor=0.5)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    # if it is a GitHub image, request it with token
    if url.startswith('https://raw.githubusercontent.com'):
        # r = requests.get(url, headers={'Authorization': 'token ' + token})
        # 更真实的请求头
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Authorization': 'token ' + token,
        }
        # 403错误的话， 等一会儿再请求
        while True:
            try:
                r = session.get(url, headers=headers)
                break
            except:
                print('sleep 2s before retrying...')
                time.sleep(2)
                continue
        # save the image
        new_path = os.path.join(asset_folder, os.path.basename(url))
        with open(new_path, 'wb') as f:
            f.write(r.content)
        # return the local path
        return new_path
    else:
        print('not a GitHub image, skip')
        return url


def get_title(target_path):
    with open(target_path, 'r', encoding='utf8') as f:
        lines = f.readlines()
        in_header = len(lines) > 0 and lines[0].startswith("---")
        if not in_header:
            # the file does not have a header
            return
        # start from the second line
        for line in lines[1:]:
            if line.startswith("---"):
                break
            elif line.startswith("title:"):
                title = line.split(":")[1].strip()
                # remove the quotation marks and ( )
                title = title.replace("\"", "").replace("(", "").replace(")", "")
                return title


def create_local_repo(md_path, dst_dir):
    md_name = get_title(md_path)
    asset_folder = os.path.join(dst_dir, md_name + '.assets')
    if not os.path.exists(asset_folder):
        os.mkdir(asset_folder)
    return asset_folder, md_name


def md_img_gather(md_path, dst_dir):
    # test whether the path is a markdown file
    if not md_path.endswith('.md'):
        return
    # create a new directory to store the images
    asset_folder, md_name = create_local_repo(md_path, dst_dir)
    print("start downloading images for " + md_name)
    # find all the urls in the markdown file
    with open(md_path, 'r', encoding='utf-8') as f:
        text = f.read()
        matches = re.compile(img_patten).findall(text)
        if matches and len(matches) > 0:
            cnt = 0
            for match in list(chain(*matches)):
                if match and len(match) > 0:
                    # check whether the url is a local file
                    if match.startswith('http'):
                        cnt += 1
                        # create a thread to download the image
                        new_path = download_img(match, asset_folder)
                        # replace the url in the markdown file
                        text = text.replace(match, new_path)
                        if cnt % 5 == 0:
                            with open(os.path.join(dst_dir, md_name + '.md'), 'w', encoding='utf-8') as f:
                                f.write(text)
                            time.sleep(2)
                    else:
                        # test whether the file exists
                        if os.path.exists(os.path.join(match)):
                            # copy the image to the new directory
                            new_path = os.path.join(asset_folder, os.path.basename(match))
                            shutil.copyfile(match, new_path)
                            # replace the url in the markdown file
                            new_path_relative = os.path.join(os.path.dirname(new_path), os.path.basename(new_path))
                            text = text.replace(match, new_path_relative)
                        else:
                            print('The file {0} in {1} is missing.'.format(match, md_name))
            # write the new markdown file to the new directory
        with open(os.path.join(dst_dir, md_name + '.md'), 'w', encoding='utf-8') as f:
            f.write(text)
        print('The markdown file {0} has been processed.'.format(md_name))


if __name__ == '__main__':
    # path = input('Please enter the directory or file path: ')
    path = '/Users/tianjiaye/临时文稿/_posts'
    # dst_dir = input('Please enter the destination directory: ')
    dst_dir = '/Users/tianjiaye/临时文稿/gather_md'
    if os.path.isdir(path):
        if dst_dir == '':
            dst_dir = path
        elif not os.path.exists(dst_dir):
            os.mkdir(dst_dir)
        # gather all the markdown files in the directory recursively
        for root, dirs, files in os.walk(path):
            for file in files:
                if file.endswith('.md'):
                    md_img_gather(os.path.join(root, file), dst_dir)
    elif os.path.isfile(path):
        md_img_gather(path, dst_dir)
