# zip-system

### Downloading from S3 using Python

This file serves as a way to recursively download folders from AWS S3. It utilizes the `sh` library.

You will need to configure your AWS credentials locally before using this. I recommend looking up the Quickstart on how to do this via terminal.

```
pip install -r requirements.txt
```

```
python3 download_s3.py
```

### Using zip.py

This file serves as a way to zip up files.

You will need to ensure the "sample-data" folder and zip.py file is in the same directory. (For Now)

When zip.py starts up it will prompt you to enter the ID(s) of the files you would like zipped.

```
Enter the file IDs separated by commas:
```
Example of what to enter:
```
Enter the file IDs separated by commas: IHS-2005-0004, CRB-2009-0003, CRB-2006-0005
```
