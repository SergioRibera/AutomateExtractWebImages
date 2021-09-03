# Auto Extract Images
It allows by means of a command to extract all the images of a url/web page, even allowing to generate a pdf with them.

## Instalation
> This need python 3.9+ installed
Process to installation dependencies
```bash
python -m pip install -r requirements.txt
```

## Usage

```plaintext
    python ./main.py [OPTIONS]
    
    Options:
        OPTION                              NECESARY         DESCRIPTION
        --url <url>                            *             This is the url where download all images
        --path <path>                          *             This is the directory where download all images
        --cookies <cookies>                                  Cookies of session to access into web
        --pdf-geometry <x,y,width,height>                    Define the size (in mm) and position of the images on page
        --output-pdf <name>                                  Enable generate PDF from all images downloaded
        --no-enumerate                                       Disable enumeration images from 0..n
```

Example Simple:
> `python .\main.py --url "https://example.com" --path "images"`
> This command download all images on url and save into "images" folder whit numeration 0..n

Generating PDF
> `python .\main.py --url "https://example.com" --path "images" --pdf-output example.pdf`
> This download images like a last example and generate pdf into `.` path with "example.pdf" name

#### Made with the ❤️ by [SergioRibera](https://sergioribera.com)