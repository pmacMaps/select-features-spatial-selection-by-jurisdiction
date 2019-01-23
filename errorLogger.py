#--------------------------------------------------------------------------------------------------------------------------------------------------------------#
# Name:        Error Logging Function
#
# Purpose:     Create an error message that includes the file name and line number of the error.
#
# Author:      Patrick McKinney
#
# Created:     11/6/2017
#
# Updated:     11/6/2017
#
# Disclaimer:  CUMBERLAND COUNTY ASSUMES NO LIABILITY ARISING FROM USE OF THESE MAPS OR DATA. THE MAPS AND DATA ARE PROVIDED WITHOUT
#              WARRANTY OF ANY KIND, EITHER EXPRESSED OR IMPLIED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND
#              FITNESS FOR A PARTICULAR PURPOSE.
#              Furthermore, Cumberland County assumes no liability for any errors, omissions, or inaccuracies in the information provided regardless
#              of the cause of such, or for any decision made, action taken, or action not taken by the user in reliance upon any maps or data provided
#              herein. The user assumes the risk that the information may not be accurate.
#--------------------------------------------------------------------------------------------------------------------------------------------------------------#

# import modules
import sys, linecache, arcpy

# Function to handle errors
def PrintException(error):
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    arcpy.AddError('\nerror: {}\nFILE: {}, LINE: {}\n\n\t "{}": {}'.format(error, filename, lineno, line.strip(), exc_obj))
    # exit Python
    sys.exit()
# end PrintException