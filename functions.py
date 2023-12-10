import glob
import os
import shutil
import subprocess
import base64
from PIL import ImageGrab
import binascii
from PIL import Image
from io import BytesIO


ERROR_MSG = "error"
SUCCEED_MSG = "done"


def dir(folder_path):
    """
    the function get a folder path and return list of the file init
    :param folder_path: the path to the folder we want to check
    :return: list of all the file of the folder
    """
    try:
        folder_path = folder_path + '/*.*'
        file_list = glob.glob(folder_path)
        return_val = " ".join(file_list)
    except FileNotFoundError:
        return_val = ERROR_MSG
    finally:
        return return_val


def delete(file_path):
    """
    delete a file
    :param file_path: the file we want to delete
    :return: succeed if the func succeed and error_msg if not
    """
    try:
        os.remove(file_path)
        return_val = SUCCEED_MSG
    except FileNotFoundError:
        return_val = ERROR_MSG
    finally:
        return return_val


def copy(parameter):
    """
    copy a file
    :param parameter: contains two parameters: the path to the file we want to copy and where to copy it to
    :return: succeed if the func succeed and error_msg if not
    """
    try:
        list = parameter.split(' ')
        shutil.copy(list[0], list[1])
        return_val = SUCCEED_MSG
    except shutil.eror as err:
        return_val = ERROR_MSG
    finally:
        return return_val



def execute(path):
    """
    open a program
    :param path: path to what we want to open
    :return: succeed if the func succeed and error_msg if not
    """
    try:
        subprocess.call(path)
        return_val = SUCCEED_MSG
    except OSError as err:
        return_val = ERROR_MSG
    finally:
        return return_val


def screenshot():
    """
    take a screenshot and return it, if it doesn't work return error
    """
    try:
        ImageGrab.grab(all_screens=True).save('screenshot.jpg')
        with open('screenshot.jpg', 'rb') as img:
            ret_val = base64.b64encode(img.read()).decode('utf-8')
        os.remove('screenshot.jpg')
    except OSError as err:
        ret_val = ERROR_MSG
    return ret_val


def save_image(screenshot):
    """
    get a file and save and open it
    :param screenshot: the file we want to open
    :return: return if the func worked and error if not
    """
    try:
        decoded_image = base64.b64decode(screenshot)
        image = Image.open(BytesIO(decoded_image))
        image.save('screenshot.jpg', 'jpeg')
        return_val = "screenshot has taken in success"
    except binascii.Error as err:
        return_val = ERROR_MSG
    finally:
        return return_val