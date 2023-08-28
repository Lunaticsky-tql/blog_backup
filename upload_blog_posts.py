import base64
import datetime
import hashlib
import json
import os
import random
import re
import sys
import time
from itertools import chain

import requests
import yaml

blog_base_dir = sys.path[0]
with open(os.path.join(blog_base_dir, "github_config.yml"), 'r', encoding='utf8') as github_config_file:
    github_config = yaml.safe_load(github_config_file)
headers = {
    'Authorization': 'token ' + github_config['token']
}
url_base = 'https://api.github.com/repos/{}/{}/contents/'.format(github_config['user_name'], github_config['repo'])
optional_tip = ['primary', 'secondary', 'success', 'info', 'warning', 'danger', 'light']
sleeping=False


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
def blob_sha(content):
    # return the blob sha of the image which is used to check files on GitHub
    return hashlib.sha1(b'blob %d\0' % len(content) + content).hexdigest()


def upload_dir(md_name, text):
    # test if the directory exists on GitHub
    url_dict = url_base + md_name
    r = requests.get(url_dict, headers=headers)
    if r.status_code == 200:
        print('Directory already exists!')
        return True
    # upload the new directory (with old md file) to GitHub
    md_base64 = base64.b64encode(text.encode('utf-8'))
    url = url_base + md_name + '/' + md_name + '.md'
    data = {
        'message': 'create directory',
        'content': md_base64.decode('utf-8'),
    }
    data = json.dumps(data)
    r = requests.put(url, headers=headers, data=data)
    if r.status_code == 201:
        return False
    return False


def update_md(md_base64, r, url_md):
    data = {
        'message': 'update md',
        'content': md_base64.decode('utf-8'),
        'sha': r.json()['sha'],
    }
    data = json.dumps(data)
    r = requests.put(url_md, headers=headers, data=data)
    if r.status_code == 200:
        # print('md file updated successfully!')
        pass
    else:
        print('md file updated failed!')


def create_md(md_base64, url_md):
    data = {
        'message': 'create md',
        'content': md_base64.decode('utf-8'),
    }
    data = json.dumps(data)
    r = requests.put(url_md, headers=headers, data=data, verify=False)
    if r.status_code == 201:
        print('md file created successfully!')
    else:
        print('md file created failed!')


def upload_img(md_name, img_data, img_sha1, img_name, is_dir_exists):
    url_dict = url_base + md_name
    # check if the image exists on GitHub
    if is_dir_exists:
        r = requests.get(url_dict, headers=headers)
        if r.status_code == 200:
            for file in r.json():
                if file['sha'] == img_sha1:
                    return file['download_url'], True
    # use current time + random number + original file name as file name
    file_name = datetime.datetime.now().strftime('%Y%m%d%H%M%S%f') + '_' + str(
        random.randint(100, 999)) + '_' + img_name
    url = url_dict + '/' + file_name
    data = {
        'message': 'upload image',
        'content': img_data.decode('utf-8'),
    }
    data = json.dumps(data)
    r = requests.put(url, headers=headers, data=data)
    # return the download url
    return r.json()['content']['download_url'], False


def replace_img_tag(content):
    # replace the zoom tag with width and height
    # style="zoom:50%;" -> width="50%" height="50%"
    zoom_pattern = re.compile(r'style="zoom:(\d+)%;"')
    zoom_tags = zoom_pattern.findall(content)
    # replace them
    print(zoom_tags)
    if zoom_tags and len(zoom_tags) > 0:
        for zoom_tag in zoom_tags:
            if int(zoom_tag) < 50:
                # replace with 50%
                content = content.replace('style="zoom:' + zoom_tag + '%;"', 'width="50%" height="50%"')
            else:
                content = content.replace('style="zoom:' + zoom_tag + '%;"',
                                          'width="' + zoom_tag + '%" height="' + zoom_tag + '%"')
    print("Zoom tags replaced")
    return content


def write_new_md_to_local(content, new_md_path, is_temp=False):
    with open(new_md_path, 'w', encoding='utf-8') as new_md:
        new_md.write(content)
    # if not is_temp:
    #     print("New md file saved to local")
    # else:
    #     print("Temp markdown file saved to local")


def upload_to_github(md_path, md_title,dst_dir):
    """Upload the file to GitHub and my blog"""
    with open(md_path, 'r', encoding='utf-8') as md:
        text = md.read()
        is_dir_exists = upload_dir(md_title, text)
        img_patten = r'!\[.*?\]\((.*?)\)|<img.*?src=[\'\"](.*?)[\'\"].*?>'
        text = replace_img_tag(text)
        # save the temp md file to local
        if md_path.endswith('_temp.md'):
            temp_md_path = md_path
        else:
            temp_md_path = os.path.join(os.path.dirname(md_path), md_title + '_temp.md')
        write_new_md_to_local(text, temp_md_path, is_temp=True)
        matches = re.compile(img_patten).findall(text)
        if matches and len(matches) > 0:
            processed = 0
            for match in list(chain(*matches)):
                original_match = match
                print(match)
                if match and len(match) > 0:
                    img_name = os.path.basename(match)
                    # picture to base64 for upload
                    if match.startswith('http'):
                        # change the text of last row of result view
                        processed += 1
                        print("The image{0} is already online".format(match))
                        continue
                    else:
                        # try to fix the relative path
                        if not os.path.exists(match):
                            match = os.path.join(os.path.dirname(md_path), match)
                            print("Relative path to absolute path: {0}".format(match))
                        if not os.path.exists(match):
                            print("Image not found: {0}".format(match))
                            continue
                        with open(match, 'rb') as match_f:
                            match_content = match_f.read()
                            img_base64 = base64.b64encode(match_content)
                            img_sha1 = blob_sha(match_content)
                    # upload the images to GitHub
                    url_ol, is_img_exists = upload_img(md_title, img_base64, img_sha1, img_name,
                                                       is_dir_exists)
                    if url_ol:
                        if sleeping:
                            # random sleep to avoid GitHub limit
                            time.sleep(random.randint(1, 3))
                            print("Sleeping ...")
                        text = text.replace(original_match, url_ol)
                        processed += 1
                        if is_img_exists:
                            print("The image{0} is already online".format(match))
                    else:
                        print("The image{0} is not uploaded".format(match))
                        write_new_md_to_local(text, temp_md_path)
        # save the new md file to local
        new_md_path = os.path.join(dst_dir, md_title + '_ol.md')
        write_new_md_to_local(text, new_md_path)
        # if temp md file exists, delete it
        if os.path.exists(temp_md_path):
            os.remove(temp_md_path)
        # upload the new md file to GitHub
        # get the old md file sha
        url_md = url_base + md_title + '/' + md_title + '.md'
        md_base64 = base64.b64encode(text.encode('utf-8'))
        r = requests.get(url_md, headers=headers, verify=False)
        if r.status_code == 200:
            update_md(md_base64, r, url_md)
        else:
            create_md(md_base64, url_md)
        print("The markdown file is uploaded to GitHub")

if __name__ == '__main__':
    # path = input('Please enter the directory or file path: ')
    path = '/Users/tianjiaye/临时文稿/gather_md'
    # dst_dir = input('Please enter the destination directory: ')
    dst_dir = '/Users/tianjiaye/临时文稿/_posts_tmp'
    if os.path.isdir(path):
        if dst_dir == '':
            dst_dir = path
        elif not os.path.exists(dst_dir):
            os.mkdir(dst_dir)
        # gather all the markdown files in the directory recursively
        for root, dirs, files in os.walk(path):
            for file in files:
                if file.endswith('.md'):
                    upload_to_github(os.path.join(root, file), get_title(os.path.join(root, file)), dst_dir)
    elif os.path.isfile(path):
        upload_to_github(path, get_title(path), dst_dir)
