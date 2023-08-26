import os

import yaml

cwd=os.getcwd()
print(cwd)

with open('github_config.yml', 'r', encoding='utf8') as github_config_file:
    github_config = yaml.load(github_config_file, Loader=yaml.FullLoader)
    print(github_config)
print(github_config['user_name'])

with open('uploader_config.yml', 'r', encoding='utf8') as uploader_config_file:
    uploader_config = yaml.safe_load(uploader_config_file)
    print(uploader_config)
