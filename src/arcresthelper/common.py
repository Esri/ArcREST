import os
import sys
import json

import random
import string
import datetime
import time

from urlparse import urlparse
import gc

#----------------------------------------------------------------------
def trace():
    """
        trace finds the line, the filename
        and error message and returns it
        to the user
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
    """ raised when error occurs in utility module functions """
    pass
#----------------------------------------------------------------------  
def noneToValue(value,newValue):
    if value is None:
        return newValue
    else:
        return value
#----------------------------------------------------------------------  
def getLayerIndex(url):
    urlInfo = None
    urlSplit = None
    inx = None   
    try:
        urlInfo = urlparse(url)
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
    urlInfo = None
    urlSplit = None   
    try:
        urlInfo = urlparse(url)
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
def random_string_generator(size=6, chars=string.ascii_uppercase):
    try:
        return ''.join(random.choice(chars) for _ in range(size))
    except:
        line, filename, synerror = trace()
        raise CommonError({
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
    """
       converts datetime object to a UTC timestamp for AGOL
       Inputs:
          dt - datetime object
       Output:
          Long value
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
        raise CommonError({
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
def online_time_to_string(value,timeFormat):
    """
       Converts a timestamp to date/time string
       Inputs:
          value - timestamp as long
          timeFormat - output date/time format
       Output:
          string
    """
    try:
        return datetime.datetime.fromtimestamp(value /1000).strftime(timeFormat)
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
    try:    
        """ converts unicode to anscii """
        
        if isinstance(obj, dict):
            return {unicode_convert(key): unicode_convert(value) for key, value in obj.iteritems()}
        elif isinstance(obj, list):
            return [unicode_convert(element) for element in obj]
        elif isinstance(obj, unicode):
            return obj.encode('utf-8')
        else:
            return obj
    except:
        return obj
def find_replace_string(obj,find,replace):
    try:
        strobj = str(obj)
        newStr =  string.replace(strobj,find, replace)
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
def find_replace(obj,find,replace):
    
    """ searchs an object and does a find and replace """
    try:
        if isinstance(obj, dict):
            return {find_replace(key,find,replace): find_replace(value,find,replace) for key, value in obj.iteritems()}
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
        raise CommonError({
                    "function": "find_replace",
                    "line": line,
                    "filename":  filename,
                    "synerror": synerror,
                                    }
                                    )
    finally:                
        pass   
#----------------------------------------------------------------------
def init_log(log_file):

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
    sys.stdout = sys.__stdout__
    if log_file is not None:
        log_file.close()
        del log_file
        
#----------------------------------------------------------------------
class Tee(object):
    """ Combines standard output with a file for logging"""

    def __init__(self, *files):
        self.files = files
    def write(self, obj):
        for f in self.files:
            f.write(obj)


