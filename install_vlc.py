import requests
import hashlib
import subprocess
import os


def main():

    # Get the expected SHA-256 hash value of the VLC installer
    expected_sha256 = get_expected_sha256()

    # Download (but don't save) the VLC installer from the VLC website
    installer_data = download_installer()

    # Verify the integrity of the downloaded VLC installer by comparing the
    # expected and computed SHA-256 hash values
    if installer_ok(installer_data, expected_sha256):

        # Save the downloaded VLC installer to disk
        installer_path = save_installer(installer_data)

        # Silently run the VLC installer
        run_installer(installer_path)

        # Delete the VLC installer from disk
        delete_installer(installer_path)

def get_expected_sha256():
    """Downloads the text file containing the expected SHA-256 value for the VLC installer file from the 
    videolan.org website and extracts the expected SHA-256 value from it.

    Returns:
        str: Expected SHA-256 hash value of VLC installer
    """
    # TODO: Step 1
    # Hint: See example code in lab instructions entitled "Extracting Text from a Response Message Body"
    # Hint: Use str class methods, str slicing, and/or regex to extract the expected SHA-256 value from the text
    sha256_val = f'https://download.videolan.org/pub/videolan/vlc/last/win64/vlc-3.0.23-win64.exe.sha256'

    print('Downloading expected SHA-256 of VLC Installer...', end='')
    resp_msg = requests.get(sha256_val)

    if resp_msg.status_code == requests.codes.ok:
        print('success')
    else: 
        print('failure')
        print(f'Response Code: {resp_msg.status_code} ({resp_msg.reason})')
        exit('Script excetion aborted.')
    
    text = resp_msg.text
    #expected_hash = text[:64]
    expected_hash = text.split()
    hash_256 = expected_hash[0]
    print(f'Expected SHA-256 of VLC installer: {hash_256}')
       
    return hash_256

def download_installer():
    """Downloads, but does not save, the .exe VLC installer file for 64-bit Windows.

    Returns:
        bytes: VLC installer file binary data
    """
    # TODO: Step 2
    # Hint: See example code in lab instructions entitled "Downloading a Binary File"
   
    sha256_val = f'https://download.videolan.org/pub/videolan/vlc/last/win64/vlc-3.0.23-win64.exe'
    print('Downloading VLC Installer...', end='')
    resp_msg = requests.get(sha256_val)

    if resp_msg.status_code == requests.codes.ok:
        print('success')
        return resp_msg.content
    else: 
        print('failure')
        print(f'Response Code: {resp_msg.status_code} ({resp_msg.reason})')
        exit('Script execution aborted.')
    
    return

def installer_ok(installer_data, expected_sha256):
    """Verifies the integrity of the downloaded VLC installer file by calculating its SHA-256 hash value 
    and comparing it against the expected SHA-256 hash value. 

    Args:
        installer_data (bytes): VLC installer file binary data
        expected_sha256 (str): Expeced SHA-256 of the VLC installer

    Returns:
        bool: True if SHA-256 of VLC installer matches expected SHA-256. False if not.
    """    
    # TODO: Step 3
    # Hint: See example code in lab instructions entitled "Computing the Hash Value of a Response Message Body"
    installer_sha256 = hashlib.sha256(installer_data).hexdigest()
    print('Calculated SHA-256 of VLC Installer:', installer_sha256)

    sha256_match = (installer_sha256 == expected_sha256)
    
    if not sha256_match:
        print('Error: SHA-256 of VLC installer not as expected')
        return sha256_match

    return sha256_match

def save_installer(installer_data):
    """Saves the VLC installer to a local directory.

    Args:
        installer_data (bytes): VLC installer file binary data

    Returns:
        str: Full path of the saved VLC installer file
    """
    # TODO: Step 4
    # Hint: See example code in lab instructions entitled "Downloading a Binary File"
    temp_path = os.getenv('TEMP')
    installer_filename = 'VLC_installer.exe'
    installer_path = os.path.join(temp_path, installer_filename)

    #save the installer file
    print(f'Saving the VLC installer file to {installer_path}...', end='')
    with open(installer_path, 'wb') as file:
        file.write(installer_data)
    print('complete')

    return installer_path

def run_installer(installer_path):
    """Silently runs the VLC installer.

    Args:
        installer_path (str): Full path of the VLC installer file
    """    
    # TODO: Step 5
    # Hint: See example code in lab instructions entitled "Running the VLC Installer"
    print('Installing VLC...', end='')

    subprocess.run([installer_path, '/L=1033', '/S'], shell=True)
    print('complete')
    return
    
def delete_installer(installer_path):
    # TODO: Step 6
    # Hint: See example code in lab instructions entitled "Running the VLC Installer"
    """Deletes the VLC installer file.

    Args:
        installer_path (str): Full path of the VLC installer file
    """
    print(f'Deleting the VLC installer from {installer_path}...', end='')
    if os.path.exists(installer_path) and os.path.isfile(installer_path):
        os.remove(installer_path)
        print('success')
    else: 
        print('failure')

    return

if __name__ == '__main__':
    main()