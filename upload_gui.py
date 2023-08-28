import math
import sys
import time
from queue import Queue
from threading import Thread
from tkinter.filedialog import askopenfilename
import ttkbootstrap as ttk
import yaml
from ttkbootstrap.constants import *
from ttkbootstrap import utility
import tkmacosx as tkmac
from ttkbootstrap.dialogs import Messagebox
import re, os, requests, datetime
import base64, hashlib
from itertools import chain
import json
import random
import signal, subprocess
from PIL import ImageGrab
from PIL import Image
import platform

from ttkbootstrap.scrolled import ScrolledFrame

# 解决Unverified HTTPS request is being made
requests.packages.urllib3.disable_warnings()
if platform.system().lower() == 'windows':
    is_windows = True
else:
    is_windows = False

blog_base_dir =sys.path[0]
blog_dir = os.path.join(blog_base_dir, "source", "_posts")
blog_theme = "fluid"
blog_img_dir = os.path.join(blog_base_dir, "themes", blog_theme, "source", "img")
category_list = []
tag_list = []

with open(os.path.join(blog_base_dir,"uploader_config.yml"), 'r', encoding='utf-8') as uploader_config_file:
    uploader_config = yaml.safe_load(uploader_config_file)
with open(os.path.join(blog_base_dir,"github_config.yml"), 'r', encoding='utf8') as github_config_file:
    github_config = yaml.safe_load(github_config_file)
headers = {
    'Authorization': 'token ' + github_config['token']
}
url_base = 'https://api.github.com/repos/{}/{}/contents/'.format(github_config['user_name'], github_config['repo'])
optional_tip = ['primary', 'secondary', 'success', 'info', 'warning', 'danger', 'light']


def get_categories_and_tags(categories, tags, target_path):
    with open(target_path, 'r', encoding='utf8') as f:
        lines = f.readlines()
        in_header = len(lines) > 0 and lines[0].startswith("---")
        if not in_header:
            # the file does not have a header
            return
        in_tags = False
        # start from the second line
        for line in lines[1:]:
            if line.startswith("---"):
                break
            elif line.startswith("categories:"):
                for cat in line.split(":")[1].split(","):
                    if cat.strip():
                        categories.append(cat.strip())
            elif line.startswith("tags:"):
                in_tags = True
                # if there are tags behind "tags:" and is not space
                if len(line.split(":")[1].strip()) > 0:
                    tags.append(line.split(":")[1].strip())
            # look for tags in lines below "tags:"
            elif in_tags:
                if line.startswith("  -"):
                    tags.append(line.split("-")[1].strip())
                else:
                    in_tags = False


def get_all_categories_and_tags():
    categories = []
    tags = []
    for file in os.listdir(blog_dir):
        if file.endswith(".md"):
            target_path = os.path.join(blog_dir, file)
            get_categories_and_tags(categories, tags, target_path)
    # sort according to frequency and remove duplicates
    categories = sorted(categories, key=categories.count, reverse=True)
    categories = list(dict.fromkeys(categories))
    tags = sorted(tags, key=tags.count, reverse=True)
    tags = list(dict.fromkeys(tags))
    return categories, tags


def middle_window(root, width=529, height=442):
    """Center window on screen"""
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width / 2) - (width / 2)
    y = (screen_height / 2) - (height / 2)
    root.geometry(f'{width}x{height}+{int(x)}+{int(y)}')


class Uploader(ttk.Frame):
    queue = Queue()
    searching = False
    showing_tags = False
    uploading = False
    generating = False
    deploying = False
    generating_shell_process = None
    deploying_shell_process = None

    def __init__(self, master):
        super().__init__(master, padding=15)
        self.img_path = None
        self.picture_btn = None
        self.deploy_thread = None
        self.deploy_btn = None
        self.look_thread = None
        self.lookup_btn = None
        self.upload_thread = None
        self.category_cbo = None
        self.process_start_btn = None
        self.tag_set_btn = None
        self.tag_window = None
        self.pack(fill=BOTH, expand=YES)

        # application variables
        self.path_var = ttk.StringVar(value='')
        self.title_var = ttk.StringVar(value='')
        self.tag_var = ttk.StringVar(value='')
        self.hide_var = ttk.BooleanVar(value=False)

        # header and labelframe option container
        option_text = "Upload Options"
        self.option_lf = ttk.Labelframe(self, text=option_text, padding=15)
        self.option_lf.pack(fill=X, expand=YES, anchor=N)

        self.create_path_row()
        self.create_title_row()
        self.create_category_row()
        self.create_tag_row()
        self.create_process_row()
        self.create_results_view()
        self.progressbar = ttk.Progressbar(
            master=self,
            bootstyle=(STRIPED, SUCCESS)
        )
        self.progressbar.pack(fill=X, expand=YES)

    def create_path_row(self):
        """Add path row to labelframe"""
        path_row = ttk.Frame(self.option_lf)
        path_row.pack(fill=X, expand=YES)
        path_lbl = ttk.Label(path_row, text="Md Path", width=8)
        path_lbl.pack(side=LEFT, padx=(15, 0))
        path_ent = ttk.Entry(path_row, textvariable=self.path_var)
        path_ent.pack(side=LEFT, fill=X, expand=YES, padx=5)
        self.browse_btn = ttk.Button(
            master=path_row,
            text="Browse",
            command=self.on_browse,
            bootstyle=OUTLINE,
            width=8
        )
        self.browse_btn.pack(side=LEFT, padx=5)

    def create_title_row(self):
        """Add title row to labelframe"""
        title_row = ttk.Frame(self.option_lf)
        title_row.pack(fill=X, expand=YES, pady=15)
        title_lbl = ttk.Label(title_row, text="Title", width=8)
        title_lbl.pack(side=LEFT, padx=(15, 0))
        title_ent = ttk.Entry(title_row, textvariable=self.title_var)
        title_ent.pack(side=LEFT, fill=X, expand=YES, padx=5)
        title_set_btn = ttk.Button(
            master=title_row,
            text="Set",
            command=self.on_set_info,
            bootstyle=OUTLINE,
            width=8
        )
        title_set_btn.pack(side=LEFT, padx=5)

    def create_category_row(self):
        """Add category row to labelframe"""
        category_row = ttk.Frame(self.option_lf)
        category_row.pack(fill=X, expand=YES)
        category_lbl = ttk.Label(category_row, text="Category", width=8)
        category_lbl.pack(side=LEFT, padx=(15, 0))
        self.category_cbo = ttk.Combobox(master=category_row, values=category_list)
        self.category_cbo.pack(side=LEFT, fill=X, expand=YES, padx=5)

    def create_tag_row(self):
        """Add tag row to labelframe"""
        tag_row = ttk.Frame(self.option_lf)
        tag_row.pack(fill=X, expand=YES, pady=15)
        tag_lbl = ttk.Label(tag_row, text="Tags", width=8)
        tag_lbl.pack(side=LEFT, padx=(15, 0))
        tag_ent = ttk.Entry(tag_row, textvariable=self.tag_var)
        tag_ent.pack(side=LEFT, fill=X, expand=YES, padx=5)
        self.tag_set_btn = ttk.Checkbutton(
            master=tag_row,
            text="Show tags",
            command=self.show_existing_tags,
            bootstyle=(OUTLINE, TOOLBUTTON),
            width=8
        )
        self.tag_set_btn.pack(side=LEFT, padx=5)

    def create_process_row(self):
        """Add process row to labelframe"""
        process_row = ttk.Frame(self.option_lf)
        process_row.pack(fill=X, expand=YES)
        process_hide = ttk.Checkbutton(master=process_row, text="Hide", variable=self.hide_var)
        process_hide.pack(side=LEFT, expand=YES, padx=5)
        process_hide.state(['!alternate'])
        self.lookup_btn = tkmac.CircleButton(
            master=process_row,
            text="👀",
            command=self.on_look_up,
            bg='#ADEFD1',
            activebackground='#B8F5E0',
            borderless=True,
            radius=15,
        )
        self.lookup_btn.pack(side=LEFT, expand=YES, padx=5)
        self.deploy_btn = tkmac.CircleButton(
            master=process_row,
            text="🚀",
            command=self.on_deploy,
            bg='#81C1D2',
            activebackground='#ADEFD1',
            borderless=True,
            radius=15,
        )
        self.deploy_btn.pack(side=LEFT, expand=YES, padx=5)
        self.picture_btn = tkmac.CircleButton(
            master=process_row,
            text="📷",
            command=self.on_picture,
            bg='#D3D3D3',
            activebackground='#ADEFD1',
            borderless=True,
            radius=15,
        )
        self.picture_btn.pack(side=LEFT, expand=YES, padx=5)
        self.process_start_btn = ttk.Button(
            master=process_row,
            text="Upload",
            command=self.on_upload,
            width=8
        )
        self.process_start_btn.pack(side=RIGHT, expand=YES, padx=5)

    def create_results_view(self):
        """Add result treeview to labelframe"""
        self.resultview = ttk.Treeview(
            master=self,
            bootstyle=INFO,
            columns=[0],
            show=HEADINGS,
            height=5
        )
        self.resultview.pack(fill=BOTH, expand=YES, pady=10)

        # setup columns and use `scale_size` to adjust for resolution
        self.resultview.heading(0, text='Info', anchor=CENTER)
        self.resultview.column(
            column=0,
            anchor=W,
            width=utility.scale_size(self, 500),
        )

    def on_browse(self):
        """Callback for directory browse"""
        if is_windows:
            initial_browse_dir = uploader_config['windows']['initial_browse_dir']
        else:
            initial_browse_dir = uploader_config['linux']['initial_browse_dir']
        path = askopenfilename(title="Select a file", filetypes=([
            ("Markdown files", "*.md")]), initialdir=initial_browse_dir)
        if path:
            self.path_var.set(path)
            md_name = os.path.basename(path)[:-3]
            if md_name.endswith('_ol'):
                md_name = md_name[:-3]
            self.title_var.set(md_name)
            # find category and tags in the file
            category_selected, tags_selected = self.find_article_info(path)
            if category_selected:
                self.category_cbo.set(category_selected)
            if tags_selected:
                # combine tags into a string "tag1#tag2#tag3"
                tags = '#'.join(tags_selected)
                self.tag_var.set(tags)

    def show_existing_tags(self):
        """Callback for tag button"""
        if not Uploader.showing_tags:
            # set the button text to "Hide tags"
            Uploader.showing_tags = True
            self.tag_set_btn.config(text="Hide tags")
            # create a new window to show existing tags
            self.tag_window = ttk.Window(title="Existing Tags")
            tag_colors = ["#53B57B", "#F0AC50", "#EA7A99", "#4BB1EA", "#A84BEA", "#FF644D", "#FFD10D"]
            tag_highlight = ["#5ABD87", "#E8B76D", "#ED91AB", "#74B6E7", "#B952FF", "#ED6D5A", "#FFD43D"]
            # scrollable frame
            if uploader_config["tag_option_ui"] == "scrollable":
                sf = ScrolledFrame(self.tag_window, autohide=True, width=100, height=400)
                sf.pack(fill=BOTH, expand=YES, padx=10, pady=10)
                for i, tag in enumerate(tag_list):
                    tag_btn = tkmac.Button(
                        master=sf,
                        text=tag,
                        command=lambda tag=tag: self.add_tag_to_input_box(tag),
                        width=80,
                        height=30,
                        bg=tag_colors[i % len(tag_colors)],
                        fg="white",
                        activebackground=tag_highlight[i % len(tag_colors)],
                        activeforeground="black",
                    )
                    tag_btn.pack(anchor=W, padx=5, pady=5)
            else:
                # self-adaptive and grid layout ( sqrt(n) * sqrt(n) )
                n_elements = len(tag_list)
                n_cols = int(math.sqrt(n_elements))
                n_rows = int(math.ceil(n_elements / n_cols))
                for i in range(n_rows):
                    for j in range(n_cols):
                        index = i * n_cols + j
                        if index < n_elements:
                            tag = tag_list[index]
                            tag_btn = tkmac.Button(
                                master=self.tag_window,
                                text=tag,
                                command=lambda tag=tag: self.add_tag_to_input_box(tag),
                                width=80,
                                height=30,
                                bg=tag_colors[index % len(tag_colors)],
                                fg="white",
                                activebackground=tag_highlight[index % len(tag_colors)],
                                activeforeground="black",
                                borderless=True
                            )
                            tag_btn.grid(row=i, column=j, padx=5, pady=5)
            # set it to the right of the main window
            self.tag_window.geometry("+%d+%d" % (self.winfo_rootx() + self.winfo_width(),
                                                 self.winfo_rooty()))
            self.tag_window.resizable(False, False)
            # when the window is closed, set the button text back to "Show tags"
            self.tag_window.protocol("WM_DELETE_WINDOW", self.hide_existing_tags)
        else:
            # set the button text to "Show tags"
            Uploader.showing_tags = False
            self.tag_set_btn.config(text="Show tags")
            # destroy the tag window
            self.tag_window.destroy()

    def hide_existing_tags(self):
        """Callback for tag window"""
        Uploader.showing_tags = False
        self.tag_set_btn.config(text="Show tags")
        self.tag_window.destroy()

    def on_upload(self):
        """Upload the file to GitHub and my blog"""
        if not self.path_var.get() or not self.path_var.get().endswith('.md') or not os.path.exists(
                self.path_var.get()):
            # show error message
            Messagebox.show_error(
                title="Error",
                message="Please select a file to upload",
                parent=self,
            )
            return
        md_path = self.path_var.get()
        is_hide = self.hide_var.get()
        # check if the title is valid
        title = self.title_var.get()
        category = self.category_cbo.get()
        tags = self.tag_var.get().split("#")
        article_config = {
            "title": title,
            "categories": category,
            "tags": tags,
        }
        if not title:
            Messagebox.show_error(
                title="Error",
                message="Please enter a title",
                parent=self,
            )
            return
        if not tags or not category:
            Messagebox.show_warning(
                title="Warning",
                message="No tags or category is set",
                parent=self,
            )
        # upload to GitHub
        Uploader.uploading = True
        # delete all rows in the treeview
        for i in self.resultview.get_children():
            self.resultview.delete(i)
        self.upload_thread = Thread(target=Uploader.upload_to_github,
                                    args=(self, md_path, title, article_config, is_hide),
                                    daemon=True)
        self.upload_thread.start()
        self.progressbar.configure(value=0)
        # change it to stop button
        self.process_start_btn.config(text="Stop", command=self.on_stop_processing, bootstyle="danger")
        self.listen_for_complete_task()

    def listen_for_complete_task(self):
        """Check if the upload task is complete"""
        listen_id = self.after(100, self.listen_for_complete_task)
        if not Uploader.uploading:
            self.process_start_btn.config(text="Upload", command=self.on_upload, bootstyle=OUTLINE)
            self.after_cancel(listen_id)
            # update category and tags list

    def listen_for_complete_deploying(self):
        """Check if the deployment task is complete"""
        listen_id_deploy = self.after(100, self.listen_for_complete_deploying)
        if not Uploader.deploying:
            self.deploy_btn.config(state=NORMAL)
            self.after_cancel(listen_id_deploy)

    def on_look_up(self):
        """Look up the file on my blog"""
        Uploader.generating = True
        # clear the treeview
        for i in self.resultview.get_children():
            self.resultview.delete(i)
        # set the progress bar to 0
        self.progressbar.configure(value=0, maximum=128, bootstyle=(SUCCESS, STRIPED))
        self.look_thread = Thread(target=Uploader.look_up, args=(self,), daemon=True)
        self.look_thread.start()
        # set the button disabled
        self.lookup_btn.config(state=DISABLED)
        self.listen_for_complete_generating()

    def on_deploy(self):
        """Deploy the blog"""
        Uploader.deploying = True
        # set the progress bar to 0
        self.deploy_thread = Thread(target=Uploader.deploy, args=(self,), daemon=True)
        self.deploy_thread.start()
        self.progressbar.configure(mode=INDETERMINATE, bootstyle=(SUCCESS, STRIPED))
        self.progressbar.start(10)
        # set the button disabled
        self.deploy_btn.config(state=DISABLED)
        self.listen_for_complete_deploying()

    def on_picture(self):
        img = ImageGrab.grabclipboard()
        if isinstance(img, Image.Image):
            # use the current title or the current time as the file name
            # get the system time
            file_name = self.title_var.get() or datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
            print(file_name)
            img_save = blog_img_dir + file_name + ".png"
            img.save(img_save)
            self.img_path = "/img/" + file_name + ".png"
            self.picture_btn.config(bg="#3f51b5")

    def deploy(self):
        """Deploy the blog"""
        if is_windows:
            deploy_cmd = "cd " + blog_base_dir + " && deploy.bat"
        else:
            deploy_cmd = "cd " + blog_base_dir + " && ./deploy.sh"
        Uploader.deploying_shell_process = subprocess.Popen(deploy_cmd, shell=True, stdout=subprocess.PIPE,
                                                            stderr=subprocess.PIPE,
                                                            universal_newlines=True, encoding='utf-8')
        while Uploader.deploying_shell_process.poll() is None:
            line = Uploader.deploying_shell_process.stdout.readline()
            # insert the line to the treeview
            self.resultview.insert("", END, values=[line])
            # scroll to the bottom
            self.resultview.see(self.resultview.get_children()[-1])
            # update the progress bar
            success_str = "Deploy done"
            if success_str in line:
                self.progressbar.stop()
                self.progressbar.configure(mode=DETERMINATE)
                Uploader.deploying = False
                break

    def listen_for_complete_generating(self):
        """Check if the generating task is complete"""
        listen_id = self.after(100, self.listen_for_complete_generating)
        if not Uploader.generating:
            self.lookup_btn.config(state=NORMAL)
            self.lookup_btn.config(command=self.on_stop_look_up)
            self.after_cancel(listen_id)

    def look_up(self):
        """Look up the blog"""
        # kill the possible existing process run on the port 4000
        if is_windows:
            os.system("taskkill /f /im node.exe")
            cmd = "cd " + blog_base_dir + " && look.bat"
        else:
            os.system("lsof -t -i:4000 | xargs kill -9")
            cmd = "cd " + blog_base_dir + " && ./look.sh"
        Uploader.generating_shell_process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
                                                             stderr=subprocess.PIPE,
                                                             universal_newlines=True, encoding='utf-8', bufsize=256)
        while Uploader.generating_shell_process.poll() is None:
            line = Uploader.generating_shell_process.stdout.readline()
            # insert the line to the treeview
            print(line)
            self.resultview.insert("", END, values=[line])
            # scroll to the bottom
            self.resultview.see(self.resultview.get_children()[-1])
            # update the progress bar
            success_str = "Hexo is running at"
            if success_str in line:
                self.progressbar.configure(value=128, bootstyle=(PRIMARY, STRIPED))
                self.lookup_btn.config(bg='#F2969A',
                                       activebackground='#F2969A')
                Uploader.generating = False
                print("Hexo is running at http://localhost:4000/")
                # open the browser through shell
                if is_windows:
                    cmd = "start http://localhost:4000/"
                else:
                    cmd = "open http://localhost:4000/"
                os.system(cmd)
                break
            else:
                self.progressbar.step(1)

    def on_stop_look_up(self):
        """Stop the generating process"""
        self.lookup_btn.config(bg='#ADEFD1',
                               activebackground='#B8F5E0', command=self.on_look_up, state=NORMAL)
        self.progressbar.configure(value=0, bootstyle=(SUCCESS, STRIPED))
        print("Ready to stop the hexo server")
        Uploader.generating_shell_process.send_signal(signal.SIGINT)
        # free the port
        if is_windows:
            os.system("taskkill /f /im node.exe")
        else:
            os.system("kill -9 $(lsof -t -i:4000)")
        # clear the treeview
        for i in self.resultview.get_children():
            self.resultview.delete(i)

    def add_tag_to_input_box(self, tag):
        """Callback for adding tag to tag entry"""
        current_tag = self.tag_var.get()
        # add tag and avoid duplicate
        if current_tag == '':
            self.tag_var.set(tag)
        elif tag not in current_tag.split('#'):
            self.tag_var.set(current_tag + '#' + tag)

    def on_set_info(self):
        """Set the title according to the md name"""
        if not os.path.exists(self.path_var.get()) or not self.path_var.get().endswith('.md'):
            Messagebox.show_error("Error", "The path is not valid")
            return
        # get the md file name
        md_name = os.path.basename(self.path_var.get())[:-3]
        if md_name.endswith('_ol'):
            md_name = md_name[:-3]
        self.title_var.set(md_name)
        category_input, tag_input = self.find_article_info(self.path_var.get())
        if category_input:
            self.category_cbo.set(category_input)
        if tag_input:
            tags = '#'.join(tag_input)
            self.tag_var.set(tags)

    def upload_dir(self, md_name, text):
        # test if the directory exists on GitHub
        url_dict = url_base + md_name
        r = requests.get(url_dict, headers=headers)
        if r.status_code == 200:
            self.resultview.insert("", END, values=["Directory already exists"])
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
            self.resultview.insert("", END, values=["Directory created!"])
            return False
        return False

    def upload_to_github(self, md_path, md_title, config, is_hide=False):
        """Upload the file to GitHub and my blog"""
        md_title = md_title.replace("\"", "").replace("(", "").replace(")", "")
        with open(md_path, 'r', encoding='utf-8') as md:
            text = md.read()
            is_dir_exists = self.upload_dir(md_title, text)
            img_patten = r'!\[.*?\]\((.*?)\)|<img.*?src=[\'\"](.*?)[\'\"].*?>'
            text = Uploader.replace_img_tag(text)
            # save the temp md file to local
            if md_path.endswith('_temp.md'):
                temp_md_path = md_path
            else:
                temp_md_path = os.path.join(os.path.dirname(md_path), md_title + '_temp.md')
            self.write_new_md_to_local(text, temp_md_path, is_temp=True)
            matches = re.compile(img_patten).findall(text)
            self.progressbar.config(mode='determinate', maximum=len(matches) + 1)
            if matches and len(matches) > 0:
                self.resultview.insert("", END, values=["Uploading images..."])
                self.resultview.insert("", END, values=["image processed {0}/{1}".format(0, len(matches))])
                processed = 0
                for match in list(chain(*matches)):
                    original_match = match
                    if not Uploader.uploading:
                        self.resultview.insert("", END, values=["Upload canceled"])
                        self.progressbar.config(bootstyle=(STRIPED, DANGER))
                        return
                    print(match)
                    if match and len(match) > 0:
                        img_name = os.path.basename(match)
                        # picture to base64 for upload
                        if match.startswith('http'):
                            # change the text of last row of result view
                            processed += 1
                            self.resultview.item(self.resultview.get_children()[-2],
                                                 values=["Uploading images...already online"])
                            print("The image{0} is already online".format(match))
                            self.resultview.item(self.resultview.get_children()[-1],
                                                 values=["image processed {0}/{1}".format(processed, len(matches))])
                            self.progressbar.configure(value=processed)
                            continue
                        else:
                            # try to fix the relative path
                            if not os.path.exists(match):
                                match = os.path.join(os.path.dirname(md_path), match)
                                print("Relative path to absolute path: {0}".format(match))
                            if not os.path.exists(match):
                                self.resultview.insert("", END, values=["Image not found: {0}".format(match)])
                                print("Image not found: {0}".format(match))
                                continue
                            with open(match, 'rb') as match_f:
                                match_content = match_f.read()
                                img_base64 = base64.b64encode(match_content)
                                img_sha1 = Uploader.blob_sha(match_content)
                        # upload the images to GitHub
                        url_ol, is_img_exists = Uploader.upload_img(md_title, img_base64, img_sha1, img_name,
                                                                    is_dir_exists)
                        if url_ol:
                            if uploader_config['random_sleep_uploading']:
                                # random sleep to avoid GitHub limit
                                time.sleep(random.randint(1, 3))
                                print("Sleeping ...")
                            text = text.replace(original_match, url_ol)
                            processed += 1
                            if is_img_exists:
                                self.resultview.item(self.resultview.get_children()[-2],
                                                     values=["Uploading images...image skipped"])
                                self.resultview.item(self.resultview.get_children()[-1],
                                                     values=["Image processed {0}/{1}".format(processed, len(matches))])
                            else:
                                self.resultview.item(self.resultview.get_children()[-2], values=["image uploaded"])
                                self.resultview.item(self.resultview.get_children()[-1],
                                                     values=["Image processed {0}/{1}".format(processed, len(matches))])
                            self.progressbar.configure(value=processed)
                        else:
                            self.resultview.insert("", END, values=["Image upload failed"])
                            self.write_new_md_to_local(text, temp_md_path)
            # save the new md file to local
            new_md_path = os.path.join(blog_dir, md_title + '_ol.md')
            content = self.add_article_config(text, config, is_hide)
            self.write_new_md_to_local(content, new_md_path)
            # if temp md file exists, delete it
            print("Temp_md_path: ", temp_md_path)
            if os.path.exists(temp_md_path):
                os.remove(temp_md_path)
            if is_hide:
                # get the abbrlink from the new md file
                cmd_g = "cd " + blog_base_dir + " && hexo g"
                os.system(cmd_g)
                abbrlink = Uploader.get_abbrlink(new_md_path)
                web_path = config['url'] + '/posts/' + abbrlink
                # set the abbrlink to the clipboard
                self.clipboard_clear()
                self.clipboard_append(web_path)
                # tell the user the abbrlink
                self.resultview.insert("", END, values=["The abbrlink is: " + abbrlink])

            # upload the new md file to GitHub
            # get the old md file sha
            url_md = url_base + md_title + '/' + md_title + '.md'
            md_base64 = base64.b64encode(content.encode('utf-8'))
            r = requests.get(url_md, headers=headers, verify=False)
            if r.status_code == 200:
                self.update_md(md_base64, r, url_md)
            else:
                self.create_md(md_base64, url_md)
            self.resultview.insert("", END, values=["Successfully processed!"])
            self.progressbar.configure(value=len(matches) + 1)
            # update the global category list and tag list
            # if it is a list,use extend,if it is a string,use append
            if isinstance(config['categories'], list):
                category_list.extend(config['categories'])
            else:
                category_list.append(config['categories'])
            tag_list.extend(config['tags'])
            Uploader.uploading = False

    @staticmethod
    def blob_sha(content):
        # return the blob sha of the image which is used to check files on GitHub
        return hashlib.sha1(b'blob %d\0' % len(content) + content).hexdigest()

    def write_new_md_to_local(self, content, new_md_path, is_temp=False):
        with open(new_md_path, 'w', encoding='utf-8') as new_md:
            new_md.write(content)
        if not is_temp:
            self.resultview.insert("", END, values=["New markdown file saved to local"])
        else:
            print("Temp markdown file saved to local")

    @staticmethod
    def on_stop_processing():
        """Stop the uploading process"""
        Uploader.uploading = False

    @staticmethod
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

    @staticmethod
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

    def add_article_config(self, content, article_config, is_hide):
        # delete the old configs at the top of the file
        # if content.startswith('---'):
        has_date_tag = False
        if content.startswith('---\n'):
            # delete the first line
            content = content[4:]
            lines = content.splitlines()
            index = 0
            for index, line in enumerate(lines):
                if line.startswith('---'):
                    break
                if line.startswith('date:'):
                    has_date_tag = True
            content = '\n'.join(lines[index + 1:])
        config_text = '---\n'
        for key in article_config:
            if key == 'tags':
                config_text += key + ':\n'
                for tag in article_config[key]:
                    config_text += '  - ' + tag + '\n'
            else:
                if isinstance(article_config[key], list):
                    config_text += key + ': ' + ','.join(article_config[key]) + '\n'
                else:
                    config_text += key + ': ' + article_config[key] + '\n'
        # add the date
        if not has_date_tag:
            config_text += 'date: ' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '\n'
        if is_hide:
            config_text += 'hidden: true\n'
        if self.img_path:
            config_text += 'index_img: ' + self.img_path + '\n'
        config_text += '---\n'
        return config_text + content

    def update_md(self, md_base64, r, url_md):
        data = {
            'message': 'update md',
            'content': md_base64.decode('utf-8'),
            'sha': r.json()['sha'],
        }
        data = json.dumps(data)
        r = requests.put(url_md, headers=headers, data=data)
        if r.status_code == 200:
            self.resultview.item(self.resultview.get_children()[-1],
                                 values=["new md file saved to local and updated to GitHub"])
        else:
            self.resultview.item(self.resultview.get_children()[-1],
                                 values=["new md file saved to local but update md failed"])

    def create_md(self, md_base64, url_md):
        data = {
            'message': 'create md',
            'content': md_base64.decode('utf-8'),
        }
        data = json.dumps(data)
        r = requests.put(url_md, headers=headers, data=data, verify=False)
        if r.status_code == 201:
            self.resultview.item(self.resultview.get_children()[-1],
                                 values=["new md file saved to local and created to GitHub"])
        else:
            self.resultview.item(self.resultview.get_children()[-1],
                                 values=["new md file saved to local but create md failed"])

    @staticmethod
    def find_article_info(path):
        tags = []
        cats = []
        get_categories_and_tags(cats,tags,path)
        return cats, tags

    @staticmethod
    def get_abbrlink(new_md_path):
        with open(new_md_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            for line in lines:
                if line.startswith("abbrlink:"):
                    return line.split(":")[1].strip()
        return None


if __name__ == '__main__':
    app = ttk.Window(title="Upload Blog", themename="litera",
                     iconphoto='app_icon.png')
    app.eval('tk::PlaceWindow . center')
    middle_window(app)
    category_list, tag_list = get_all_categories_and_tags()
    Uploader(app)
    app.mainloop()
