import requests
import hashlib

def downloadURLFile(url): # Main function for downloading our URL file.
    local_filepath = url.split('/')[-1] # Extract file name from end of the URL.
    local_filename = local_filepath.split('?')[0] # Strip away queries tailing after the file name from the URL.

    try:
        r = requests.get(url, stream=True) # Stores our GET request to variable 'r'.
    except:
        print("{} is an invalid url".format(url)) # End function if URL input is invalid.
        return

    header_md5 = "n/a"
    file_md5 = "n/a"
    accept_bytes_check = "n/a"

    print("Extracting Etag to verify MD5...") # To verify file after downloading, we'll grab the file's MD5 hash, which may be stored in the page's header's Etag.

    try:
        header_md5 = r.headers['ETag']
        header_md5 = header_md5.replace('"', '').strip()
        print("Etag extracted: {}".format(header_md5))
    except KeyError:
        print("KeyError raised: ETag was not found in the header to verify MD5...")

    try:
        accept_bytes_check = r.headers['Accept-Ranges'] # Check if the file server supports byte range GET requests.
    except KeyError:
        print("KeyError raised: Accept-Ranges was not found in header to verify byte range GET resquests...")

    if accept_bytes_check == "bytes":
        print("This file server supports byte range GET requests, and will be downloaded in chunks...")
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024): # Itterates over the file's contents and sets each file "chunk" to 1024 bytes
                if chunk:
                    f.write(chunk)
    else:
        print("This file server does NOT support byte range GET requests, and will be downloaded at once!")

        try:
            with open(local_filename, 'wb') as f:
                f.write(r.content) # Downloads the whole file at once.
        except:
            print("Url entry cannot end with a '/' symbol.") # Ends program if the URL path ends with '/'.
            return

    print("{} has been downloaded!".format(local_filename))

    if header_md5 != "n/a": # If there is no header MD5 extracted to verify before downloading, the program won't waste time extracting the MD5 of the file after downloading.
        print("Extracting MD5 from downloaded file for integrity...")
        file_md5 = hashlib.md5(open(local_filename,'rb').read()).hexdigest()
        print("MD5 extracted: {}".format(file_md5))

    if header_md5 == file_md5: # Check downloaded file for integrity.
        print("{}'s MD5 checksum has been verified!".format(local_filename))
    else:
        print("{}'s MD5 checksum has NOT been verified.".format(local_filename))


if __name__ == "__main__":

    while True:
        request = input("Input URL here. To exit, type 'exit' >>> ")
        if request.lower() == 'exit':
            break
        else:
            downloadURLFile(request)
