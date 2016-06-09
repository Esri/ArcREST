from __future__ import print_function
# Esri start of added imports
import sys, os, arcpy
# Esri end of added imports

import os
import sys
import arcpy
import glob
import shutil
import zipfile
import inspect

def zipws(path, zip, keep):
    path = os.path.normpath(path)
    # os.walk visits every subdirectory, returning a 3-tuple
    #  of directory name, subdirectories in it, and file names
    #  in it.
    #
    for (dirpath, dirnames, filenames) in os.walk(path):
        # Iterate over every file name
        #
        for file in filenames:
            # Ignore .lock files
            #
            if not file.endswith('.lock') and \
               not file.endswith('.pyc'):
                #arcpy.AddMessage("Adding %s..." % os.path.join(path, dirpath, file))
                try:
                    if keep:
                        zip.write(os.path.join(dirpath, file),
                                  os.path.join(os.path.basename(path),
                                               os.path.join(dirpath, file)[len(path)+len(os.sep):]))
                    else:
                        zip.write(os.path.join(dirpath, file),
                                  os.path.join(dirpath[len(path):], file))

                except Exception as e:
                    pass#arcpy.AddWarning("    Error adding %s: %s" % (file, e.message))
def download_arcrest():
    """downloads arcrest to disk"""
    url = "https://github.com/Esri/ArcREST/archive/master.zip"
    file_name = os.path.join(arcpy.env.scratchFolder, os.path.basename(url))
    scratch_folder = os.path.join(arcpy.env.scratchFolder, "temp34asdf3d")
    arcrest_zip = os.path.join(scratch_folder, g_ESRI_variable_1)
    arcresthelper_zip = os.path.join(scratch_folder, g_ESRI_variable_2)
    if sys.version_info.major == 3:
        import urllib.request
        urllib.request.urlretrieve(url, file_name)
    else:
        import urllib
        urllib.urlretrieve(url, file_name)
    if os.path.isdir(scratch_folder):
        shutil.rmtree(scratch_folder)
    os.makedirs(scratch_folder)
    zip_obj = zipfile.ZipFile(file_name, 'r')
    zip_obj.extractall(scratch_folder)
    zip_obj.close()
    del zip_obj
    zip_obj = zipfile.ZipFile(arcrest_zip, 'w')
    zipws(path=os.path.join(scratch_folder, "arcrest-master", "src", "arcrest"), zip=zip_obj, keep=True)
    zip_obj.close()
    del zip_obj
    zip_obj = zipfile.ZipFile(arcresthelper_zip, 'w')
    zipws(path=os.path.join(scratch_folder, "arcrest-master", "src", "arcresthelper"), zip=zip_obj, keep=True)
    zip_obj.close()
    del zip_obj
    shutil.rmtree(os.path.join(scratch_folder, "arcrest-master"))
    return arcrest_zip, arcresthelper_zip

def trace():
    """
        trace finds the line, the filename
        and error message and returns it
        to the user
    """
    import traceback
    import sys
    tb = sys.exc_info()[2]
    tbinfo = traceback.format_tb(tb)[0]
    # script name + line number
    line = tbinfo.split(", ")[1]
    # Get Python syntax error
    #
    synerror = traceback.format_exc().splitlines()[-1]
    return line, __file__, synerror

def installPackages(arcrest_zip, arcresthelper_zip, site_package):
    try:
        arcpy.AddMessage("Processing {0}".format(site_package))
        if not os.path.isfile(arcrest_zip):
            arcpy.AddError("... ArcRest zip does not exist...")
            return;
        if not os.path.isfile(arcresthelper_zip):
            arcpy.AddError("... ArcRestHelper zip does not exist...")
            return;

        arcrestPath = os.path.join(site_package,"arcrest")
        if os.path.isdir(arcrestPath):
            initFile = os.path.join(arcrestPath,'__init__.py')
            if os.path.isfile(initFile):
                with open(initFile, "r") as ins:
                    for line in ins:
                        if '__version__' in line:
                            version = line.replace('__version__ = ','').strip()
                            arcpy.AddMessage("\t... ArcREST is at version: %s ..." % version)
                            break;
            shutil.rmtree(arcrestPath)
            arcpy.AddMessage("\t... Removing previous verion of the Arcrest Module ...")
        arcpy.AddMessage("\t... Adding the ArcRest Module ...")
        zip_ref = zipfile.ZipFile(arcrest_zip, 'r')
        zip_ref.extractall(site_package)
        zip_ref.close()
        del zip_ref
        if os.path.isfile(initFile):
            with open(initFile, "r") as ins:
                for line in ins:
                    if '__version__' in line:
                        version = line.replace('__version__ = ','').strip()
                        arcpy.AddMessage("\t... ArcREST is now at version: %s ..." % version)
                        break;
        arcpy.AddMessage("\t-----------------------------------------------")
        arcresthelperPath = os.path.join(site_package,"arcresthelper")
        if os.path.isdir(arcresthelperPath):
            initFile = os.path.join(arcresthelperPath,'__init__.py')
            if os.path.isfile(initFile):
                with open(initFile, "r") as ins:
                    for line in ins:
                        if '__version__' in line:
                            version = line.replace('__version__ = ','').strip()
                            arcpy.AddMessage("\t... ArcRESTHelper is at version: %s ..." % version)
                            break;
            shutil.rmtree(arcresthelperPath)
            arcpy.AddMessage("\t... Removing previous verion of the ArcRESTHelper Module ...")
        arcpy.AddMessage("\t... Adding the ArcRESTHelper Module ...")
        zip_ref = zipfile.ZipFile(arcresthelper_zip, 'r')
        zip_ref.extractall(site_package)
        zip_ref.close()
        del zip_ref
        initFile = os.path.join(arcresthelperPath,'__init__.py')
        if os.path.isfile(initFile):
            with open(initFile, "r") as ins:
                for line in ins:
                    if '__version__' in line:
                        version = line.replace('__version__ = ','').strip()
                        arcpy.AddMessage("\t... ArcRESTHelper is now at version: %s ..." % version)
                        break;
    except:
        arcpy.AddError(str(trace()))
        print (str(trace()))
    arcpy.AddMessage("The modules has been loaded to {0} ...".format(site_package))

def main():
    arcrestZip = 'arcrest.zip'
    arcrestHelperZip = 'arcresthelper.zip'

    get_latest = arcpy.GetParameter(0)
    installInBoth = arcpy.GetParameter(1)
    base_folder = os.path.dirname(__file__)
    #arcpy.AddMessage("%s: " % base_folder)
    base_folder = os.path.dirname(base_folder)
    #arcpy.AddMessage("%s: " % base_folder)
    base_folder = os.path.dirname(base_folder)
    #arcpy.AddMessage("%s: " % base_folder)
    base_file = os.path.splitext(os.path.basename(__file__))[0]

    if get_latest:
        arcrest_zip, arcresthelper_zip = download_arcrest()
    else:
        commondata = os.path.join(base_folder, "commondata")
        if os.path.isdir(os.path.join(commondata, base_file)):
            arcrest_zip = os.path.join(commondata,base_file, arcrestZip)
            arcresthelper_zip = os.path.join(commondata, base_file, arcrestHelperZip)
        elif os.path.isdir(os.path.join(commondata, "userdata")):
            arcrest_zip = os.path.join(commondata, "userdata", arcrestZip)
            arcresthelper_zip = os.path.join(commondata,  "userdata", arcrestHelperZip)

    site_package = None
    site_package64 = None
    defPath =  os.path.dirname(os.__file__)
    if ('ArcGIS' in defPath):
        if ('x64' in defPath):
            site_package = os.path.join(defPath.replace('x64',''), 'site-packages')
            site_package64 = os.path.join(defPath, 'site-packages')
        else:
            site_package = os.path.join(defPath, 'site-packages')
            site_package64 = os.path.join(defPath.replace('ArcGIS','ArcGISx64'), 'site-packages')
    else:
        site_package = os.path.join(defPath,'site-packages')
##    for p in sys.path:
##        if p.lower().find("site-packages") > -1:
##            site_package = p
##            break
##        del p
    if site_package is None:
        raise arcpy.ExecuteError("Could not find the site-package folder")
    installPackages(arcrest_zip,arcresthelper_zip, site_package)

    if site_package64 is not None and installInBoth == True:
        arcpy.AddMessage(" ")
        arcpy.AddMessage("-----------------------------------------------")
        arcpy.AddMessage(" ")
        installPackages(arcrest_zip,arcresthelper_zip, site_package64)
    arcpy.AddMessage(" ")
    arcpy.AddMessage("... Process Complete ...".format(site_package))
if __name__ == "__main__":
    main()
