from __future__ import print_function
from __future__ import absolute_import


import os
import sys
import json

import random
import string
import datetime
import time

from .packages.six.moves import urllib_parse as urlparse
import gc
import operator
#----------------------------------------------------------------------
def trace():
    """Determine information about where an error was thrown.

    Returns:
        tuple: line number, filename, error message

    """
    import traceback, inspect
    tb = sys.exc_info()[2]
    tbinfo = traceback.format_tb(tb)[0]
    filename = inspect.getfile(inspect.currentframe())
    # script name + line number
    line = tbinfo.split(", ")[1]
    # Get Python syntax error
    #
    synerror = traceback.format_exc().splitlines()[-1]
    return line, filename, synerror

class ArcRestHelperError(Exception):
    """Raised when error occurs in utility module functions."""
    pass
def merge_dicts(dicts, op=operator.add):
    """Merge a list of dictionaries.

    Args:
        dicts (list): a list of dictionary objects
        op (operator): an operator item used to merge the dictionaries. Defaults to :py:func:`operator.add`.

    Returns:
        dict: the merged dictionary

    """
    a = None
    for b in dicts:

        if a is None:
            a = b.copy()
        else:
            a = dict(a.items() + b.items() + [(k, op(a[k], b[k])) for k in set(b) & set(a)])
    return a

##----------------------------------------------------------------------
#def merge_dicts(dicts):
    #'''
    #Given any number of dicts, shallow copy and merge into a new dict,
    #precedence goes to key value pairs in latter dicts.
    #'''
   ## result = {}
    #z = None
    #for dictionary in dicts:
        ##result.update(dictionary)
        #if z is None:
            #z = dictionary.copy()
        #else:
            #z.update(dictionary)

    #return z
#def merge_two_dicts(x, y):
    #'''Given two dicts, merge them into a new dict as a shallow copy.'''
    #z = x.copy()
    #z.update(y)
    #return z
#----------------------------------------------------------------------
def noneToValue(value, newValue):
    """Convert ``None`` to a different value.

    Args:
        value: The value to convert. This can be anything.
        newValue: The resultant value. This can be anything.

    Returns:
        newValue

    """
    if value is None:
        return newValue
    else:
        return value
#----------------------------------------------------------------------
def getLayerIndex(url):
    """Extract the layer index from a url.

    Args:
        url (str): The url to parse.

    Returns:
        int: The layer index.

    Examples:
        >>> url = "http://services.arcgis.com/<random>/arcgis/rest/services/test/FeatureServer/12"
        >>> arcresthelper.common.getLayerIndex(url)
        12

    """
    urlInfo = None
    urlSplit = None
    inx = None
    try:
        urlInfo = urlparse.urlparse(url)
        urlSplit = str(urlInfo.path).split('/')
        inx = urlSplit[len(urlSplit)-1]

        if is_number(inx):
            return int(inx)

    except:
        return 0
    finally:
        urlInfo = None
        urlSplit = None

        del urlInfo
        del urlSplit

        gc.collect()
#----------------------------------------------------------------------
def getLayerName(url):
    """Extract the layer name from a url.

    Args:
        url (str): The url to parse.

    Returns:
        str: The layer name.

    Examples:
        >>> url = "http://services.arcgis.com/<random>/arcgis/rest/services/test/FeatureServer/12"
        >>> arcresthelper.common.getLayerIndex(url)
        'test'

    """
    urlInfo = None
    urlSplit = None
    try:
        urlInfo = urlparse.urlparse(url)
        urlSplit = str(urlInfo.path).split('/')
        name = urlSplit[len(urlSplit)-3]
        return name
    except:
        return url

    finally:
        urlInfo = None
        urlSplit = None

        del urlInfo
        del urlSplit

        gc.collect()
#----------------------------------------------------------------------

def getOrgId(url):
    """Extract the org ID from a url.

    Args:
        url (str): The url to parse.

    Returns:
        str: The org ID.

    Examples:
        >>> url = "http://services.arcgis.com/<random>/arcgis/rest/services/test/FeatureServer/12"
        >>> arcresthelper.common.getLayerIndex(url)
        '<random>'

    """
    urlInfo = None
    urlSplit = None
    try:
        urlInfo = urlparse.urlparse(url)
        urlSplit = str(urlInfo.path).split('/')
        name = urlSplit[len(urlSplit)-7]
        return name
    except:
        return url

    finally:
        urlInfo = None
        urlSplit = None

        del urlInfo
        del urlSplit

        gc.collect()

#----------------------------------------------------------------------
def random_string_generator(size=6, chars=string.ascii_uppercase):
    """Generates a random string from a set of characters.

    Args:
        size (int): The length of the resultant string. Defaults to 6.
        chars (str): The characters to be used by :py:func:`random.choice`. Defaults to :py:const:`string.ascii_uppercase`.

    Returns:
        str: The randomly generated string.

    Examples:
        >>> arcresthelper.common.random_string_generator()
        'DCNYWU'
        >>> arcresthelper.common.random_string_generator(12, "arcREST")
        'cESaTTEacTES'

    """
    try:
        return ''.join(random.choice(chars) for _ in range(size))
    except:
        line, filename, synerror = trace()
        raise ArcRestHelperError({
                    "function": "random_string_generator",
                    "line": line,
                    "filename":  filename,
                    "synerror": synerror,
                                    }
                                    )
    finally:
        pass
#----------------------------------------------------------------------
def random_int_generator(maxrange):
    """Generates a random integer from 0 to `maxrange`, inclusive.

    Args:
        maxrange (int): The upper range of integers to randomly choose.

    Returns:
        int: The randomly generated integer from :py:func:`random.randint`.

    Examples:
        >>> arcresthelper.common.random_int_generator(15)
        9

    """
    try:
        return random.randint(0,maxrange)
    except:
        line, filename, synerror = trace()
        raise ArcRestHelperError({
                    "function": "random_int_generator",
                    "line": line,
                    "filename":  filename,
                    "synerror": synerror,
                                    }
                                    )
    finally:
        pass
#----------------------------------------------------------------------
def local_time_to_online(dt=None):
    """Converts datetime object to a UTC timestamp for AGOL.

    Args:
        dt (datetime): The :py:class:`datetime.datetime` object to convert. Defaults to ``None``, i.e., :py:func:`datetime.datetime.now`.

    Returns:
        float: A UTC timestamp as understood by AGOL (time in ms since Unix epoch * 1000)

    Examples:
        >>> arcresthelper.common.local_time_to_online() # PST
        1457167261000.0
        >>> dt = datetime.datetime(1993, 3, 5, 12, 35, 15) # PST
        >>> arcresthelper.common.local_time_to_online(dt)
        731392515000.0
    See Also:
       :py:func:`online_time_to_string` for converting a UTC timestamp

    """
    is_dst = None
    utc_offset = None
    try:
        if dt is None:
            dt = datetime.datetime.now()

        is_dst = time.daylight > 0 and time.localtime().tm_isdst > 0
        utc_offset =  (time.altzone if is_dst else time.timezone)

        return (time.mktime(dt.timetuple()) * 1000) + (utc_offset * 1000)
    except:
        line, filename, synerror = trace()
        raise ArcRestHelperError({
                    "function": "local_time_to_online",
                    "line": line,
                    "filename":  filename,
                    "synerror": synerror,
                                    }
                                    )
    finally:
        is_dst = None
        utc_offset = None

        del is_dst
        del utc_offset

#----------------------------------------------------------------------
def online_time_to_string(value, timeFormat, utcOffset=0):
    """Converts AGOL timestamp to formatted string.

    Args:
        value (float): A UTC timestamp as reported by AGOL (time in ms since Unix epoch * 1000)
        timeFormat (str): Date/Time format string as parsed by :py:func:`datetime.strftime`.
        utcOffset (int): Hours difference from UTC and desired output. Default is 0 (remain in UTC).

    Returns:
        str: A string representation of the timestamp.

    Examples:
        >>> arcresthelper.common.online_time_to_string(1457167261000.0, "%Y-%m-%d %H:%M:%S")
        '2016-03-05 00:41:01'
        >>> arcresthelper.common.online_time_to_string(731392515000.0, '%m/%d/%Y %H:%M:%S', -8) # PST is UTC-8:00
        '03/05/1993 12:35:15'

    See Also:
       :py:func:`local_time_to_online` for converting a :py:class:`datetime.datetime` object to AGOL timestamp

    """

    try:
        return datetime.datetime.fromtimestamp(value/1000 + utcOffset*3600).strftime(timeFormat)
    except:
        line, filename, synerror = trace()
        raise ArcRestHelperError({
                    "function": "online_time_to_string",
                    "line": line,
                    "filename":  filename,
                    "synerror": synerror,
                                    }
                                    )
    finally:
        pass
#----------------------------------------------------------------------
def is_number(s):
    """Determines if the input is numeric

    Args:
        s: The value to check.
    Returns:
        bool: ``True`` if the input is numeric, ``False`` otherwise.

    """
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False
#----------------------------------------------------------------------
def init_config_json(config_file):
    """Deserializes a JSON configuration file.

    Args:
        config_file (str): The path to the JSON file.
    Returns:
        dict: A dictionary object containing the JSON data. If ``config_file`` does not exist, returns ``None``.

    """
    json_data = None
    try:
        if os.path.exists(config_file):
        #Load the config file

            with open(config_file) as json_file:
                json_data = json.load(json_file)
                return unicode_convert(json_data)
        else:
            return None
    except:
        line, filename, synerror = trace()
        raise ArcRestHelperError({
                    "function": "init_config_json",
                    "line": line,
                    "filename":  filename,
                    "synerror": synerror,
                                    }
                                    )
    finally:
        json_data = None

        del json_data

        gc.collect()

#----------------------------------------------------------------------
def write_config_json(config_file, data):
    """Serializes an object to disk.

    Args:
        config_file (str): The path on disk to save the file.
        data (object): The object to serialize.

    """
    outfile = None
    try:
        with open(config_file, 'w') as outfile:
            json.dump(data, outfile)
    except:
        line, filename, synerror = trace()
        raise ArcRestHelperError({
                    "function": "init_config_json",
                    "line": line,
                    "filename":  filename,
                    "synerror": synerror,
                                    }
                                    )
    finally:
        outfile = None

        del outfile

        gc.collect()

#----------------------------------------------------------------------
def unicode_convert(obj):
    """Converts unicode objects to anscii.

    Args:
        obj (object): The object to convert.
    Returns:
        The object converted to anscii, if possible. For ``dict`` and ``list``, the object type is maintained.

    """
    try:
        if isinstance(obj, dict):
            return {unicode_convert(key): unicode_convert(value) for key, value in obj.items()}
        elif isinstance(obj, list):
            return [unicode_convert(element) for element in obj]
        elif isinstance(obj, unicode):
            return obj.encode('utf-8')
        else:
            return obj
    except:
        return obj

def find_replace_string(obj, find, replace):
    """Performs a string.replace() on the input object.

    Args:
        obj (object): The object to find/replace. It will be cast to ``str``.
        find (str): The string to search for.
        replace (str): The string to replace with.
    Returns:
        str: The replaced string.

    """
    try:
        strobj = str(obj)
        newStr =  string.replace(strobj, find, replace)
        if newStr == strobj:
            return obj
        else:
            return newStr

    except:
        line, filename, synerror = trace()
        raise ArcRestHelperError({
                    "function": "find_replace_string",
                    "line": line,
                    "filename":  filename,
                    "synerror": synerror,
                                    }
                                    )
    finally:
        pass

def find_replace(obj, find, replace):
    """ Searches an object and performs a find and replace.

    Args:
        obj (object): The object to iterate and find/replace.
        find (str): The string to search for.
        replace (str): The string to replace with.
    Returns:
        object: The object with replaced strings.

    """
    try:
        if isinstance(obj, dict):
            return {find_replace(key,find,replace): find_replace(value,find,replace) for key, value in obj.items()}
        elif isinstance(obj, list):
            return [find_replace(element,find,replace) for element in obj]
        elif obj == find:
            return unicode_convert(replace)
        else:
            try:
                return unicode_convert(find_replace_string(obj, find, replace))
                #obj = unicode_convert(json.loads(obj))
                #return find_replace(obj,find,replace)
            except:
                return unicode_convert(obj)
    except:
        line, filename, synerror = trace()
        raise ArcRestHelperError({
                    "function": "find_replace",
                    "line": line,
                    "filename":  filename,
                    "synerror": synerror,
                                    }
                                    )
    finally:
        pass
#----------------------------------------------------------------------
def chunklist(l, n):
    """Yield successive n-sized chunks from l.

    Args:
        l (object): The object to chunk.
        n (int): The size of the chunks.
    Yields:
        The next chunk in the object.
    Raises:
        TypeError: if ``l`` has no :py:func:`len`.
    Examples:
        >>> for c in arcresthelper.common.chunklist(list(range(20)), 6):
        ...     print(c)
        [0, 1, 2, 3, 4, 5]
        [6, 7, 8, 9, 10, 11]
        [12, 13, 14, 15, 16, 17]
        [18, 19]
        >>> list(arcresthelper.common.chunklist(string.ascii_uppercase, 7))
        ['ABCDEFG', 'HIJKLMN', 'OPQRSTU', 'VWXYZ']

    """
    n = max(1, n)
    for i in range(0, len(l), n):
        yield l[i:i+n]
#----------------------------------------------------------------------
def init_log(log_file):
    """ Creates log file on disk and "Tees" :py:class:`sys.stdout` to console and disk

    Args:
        log_file (str): The path on disk to append or create the log file.

    Returns:
        file: The opened log file.
    """
    #Create the log file
    log = None
    try:
        log = open(log_file, 'a')

        #Change the output to both the windows and log file
        #original = sys.stdout
        sys.stdout = Tee(sys.stdout, log)
    except:
        pass
    return log

def close_log(log_file):
    """ Closes the open file and returns :py:class:`sys.stdout` to the default (i.e., console output).

    Args:
        log_file (file): The file object to close.

    """
    sys.stdout = sys.__stdout__
    if log_file is not None:
        log_file.close()
        del log_file

#----------------------------------------------------------------------
class Tee(object):
    """Combines standard output with a file for logging."""
    def __init__(self, *files):
        self.files = files
    def write(self, obj):
        for f in self.files:
            f.write(obj)
