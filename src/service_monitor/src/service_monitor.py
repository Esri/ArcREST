"""
    @author: A Chapkowski
    @contact:  achapkowski@esri.com
    @company: Esri
    @version: 1.0.0
    @description:  Writes a server's log file to local disk
    @requirements: Python 2.7.x, ArcGIS 10.2.x
    @copyright: Esri, 2014
"""
import arcgisserver as admin
from datetime import datetime, timedelta
import ConfigParser
import sys
import os
def trace():
    """
        trace finds the line, the filename
        and error message and returns it
        to the user
    """
    import traceback
    tb = sys.exc_info()[2]
    tbinfo = traceback.format_tb(tb)[0]
    # script name + line number
    line = tbinfo.split(", ")[1]
    # Get Python syntax error
    #
    synerror = traceback.format_exc().splitlines()[-1]
    return line, __file__, synerror
def create_timestamp():
    """ returns a string timestamp YYYYMMDDThhmmss"""
    return datetime.now().strftime("%Y%m%dT%H%M%S")
def get_config_value(config_file, section, variable):
    """ extracts a config file value """
    try:
        parser = ConfigParser.SafeConfigParser()
        parser.read(config_file)
        return parser.get(section, variable)
    except:
        return None
if __name__ == "__main__":
    try:
        config_file = os.path.dirname(__file__) + os.sep + "server_test.ini"#sys.argv[0]
        if os.path.isfile(config_file):
            #  Get configuration values
            #
            admin_url = get_config_value(config_file=config_file,
                                         section="server_information",
                                         variable="admin_url")
            token_url = get_config_value(config_file=config_file,
                                         section="credentials",
                                         variable="tokenURL")
            username = get_config_value(config_file=config_file,
                                        section="credentials",
                                        variable="username")
            password = get_config_value(config_file=config_file,
                                         section="credentials",
                                         variable="password")
            service_type = get_config_value(config_file=config_file,
                                         section="reporting",
                                         variable="service_type")
            out_path = get_config_value(config_file=config_file,
                                         section="reporting",
                                         variable="out_folder")
            report_name = get_config_value(config_file=config_file,
                                         section="reporting",
                                         variable="report_name")
            days_back = get_config_value(config_file=config_file,
                                         section="reporting",
                                         variable="days_back")        
            fileFormat = get_config_value(config_file=config_file,
                                         section="reporting",
                                         variable="file_format") # tab or csv
            #   Local variables
            #
            gps = []
            now = datetime.now()
            way_back = None
            file_name = os.path.join(out_path, 
                                     "%s_%s.%s" % (report_name, 
                                                   create_timestamp(),
                                                   fileFormat.lower())
                                     )
            #  Logic
            #
            if days_back is not None and \
               days_back != "None":
                days_back = int(days_back)
                
            else:
                days_back = None
                
            if os.path.isdir(out_path) == False:
                os.makedirs(out_path)
            
            ags = admin.ArcGISServer(url=admin_url, 
                     token_url=token_url, 
                     username=username, 
                     password=password)
            log = ags.log
            #startTime, endTime
            services = ags.services
            for gp in services.find_services(service_type=service_type):
                if gp['folderName'] != "/":
                    gps.append(gp['folderName'] + "/%s.%s" % (gp['serviceName'], gp['type']))
                else:
                    gps.append("%s.%s" % (gp['serviceName'], gp['type']))
            if days_back is None:        
                out_error_table = log.query(services=",".join(gps),
                                        export=True,
                                        exportType=fileFormat,
                                        out_path=file_name)
            else:
                out_error_table = log.query(startTime=now - timedelta(days=days_back), 
                                            endTime=now,
                                            services=",".join(gps),
                                            export=True,
                                            exportType=fileFormat,
                                            out_path=file_name)
        else:
            raise AttributeError("A configuration file path is required to run this tool.")
    except:
        line, filename, synerror = trace()
        print "error on line: %s" % line
        print "error in file name: %s" % filename
        print "with error message: %s" % synerror