#!env/python3

from types import prepare_class
import requests, os, sys
from tqdm import tqdm
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin, urlparse


# Debugs
def print_fail(message, end = '\n'):
    print('\n[\x1b[1;31m x\x1b[0m ] \x1b[1;31m' + message.strip() + '\x1b[0m' + end)
    help()
    quit(2)

def is_valid(url):
    """
    Checks whether `url` is a valid URL.
    """
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)

def get_all_images(url):
    """
    Returns all image URLs on a single `url`
    """
    soup = bs(requests.get(url).content, "html.parser")
    urls = []
    for img in tqdm(soup.find_all("img"), "Extracting images"):
        img_url = img.attrs.get("src")
        if not img_url:
            # if img does not contain src attribute, just skip
            continue
        # make the URL absolute by joining domain with the URL that is just extracted
        img_url = urljoin(url, img_url)
        try:
            pos = img_url.index("?")
            img_url = img_url[:pos]
        except ValueError:
            pass
        # finally, if the url is valid
        if is_valid(img_url):
            urls.append(img_url)
    return urls

def download(url, pathname):
    """
    Downloads a file given an URL and puts it in the folder `pathname`
    """
    # if path doesn't exist, make that path dir
    if not os.path.isdir(pathname):
        os.makedirs(pathname)
    # download the body of response by chunk, not immediately
    response = requests.get(url, stream=True)
    # get the total file size
    file_size = int(response.headers.get("Content-Length", 0))
    # get the file name
    filename = os.path.join(pathname, url.split("/")[-1])
    # progress bar, changing the unit to bytes instead of iteration (default by tqdm)
    progress = tqdm(response.iter_content(1024), f"Downloading {filename}", total=file_size, unit="B", unit_scale=True, unit_divisor=1024)
    with open(filename, "wb") as f:
        for data in progress.iterable:
            # write data read to the file
            f.write(data)
            # update the progress bar manually
            progress.update(len(data))

def help():
    print("----------- Help Guide --------------")
    print("\n python ./main.py [OPTIONS]")
    print("\n\n Options:")
    print("\t--url <url>                This is the url where download all images")
    print("\t--path <path>              This is the directory where download all images")
    print("\t--cookies <cookies>        Cookies of session to access into web")
    print("\t--pdf                      Enable generate PDF from all images downloaded")
    print("\t--enumerate                Enumerate images from 0..n")
    # print("\t--ignore [name name ...]   List of images names to ignore on download (Regex are valid)\n\n")
    pass

# Process arguments
def process_args(args: list, argToSearch: str, typeValue: str, defaultValue: str = ""):
    lenArgs = len(args)
    for i in range(0, lenArgs):
        argText = args[i].removeprefix("--").lower()
        if argText == argToSearch:
            if typeValue == "bool":
                return True
            elif typeValue == "str":
                if i + 1 >= lenArgs:
                    print_fail(f"Value for \"{argToSearch}\" not found")
                return args[i + 1]
    if typeValue == "bool":
        return False
    return defaultValue



if __name__ == "__main__":
    if len(sys.argv) > 1:
        args = sys.argv[1:]
        stop = False
        if process_args(args, "help", "bool", defaultValue=False):
            help()
            stop = True
        if not stop:
            url = process_args(args, "url", "str")
            path = process_args(args, "path", "str")
            enable_pdf = process_args(args, "pdf", "bool", defaultValue=False)
            enable_enumerate = process_args(args, "enumerate", "bool", defaultValue=False)
            ignore_list = []
            if not url == "":
                if not path == "":
                    imgs = get_all_images(url)
                    for img in imgs:
                        # for each image, download it
                        download(img, path)
                else:
                    print_fail("Path is empty")
            else:
                print_fail("Url is empty")
    else:
        print_fail("This require options")