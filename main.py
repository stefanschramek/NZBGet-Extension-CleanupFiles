#
# Cleanup Files post-processing script for NZBGet
#

import os
import sys

# NZBGet Exit Codes
NZBGET_POSTPROCESS_PARCHECK=92
NZBGET_POSTPROCESS_SUCCESS=93
NZBGET_POSTPROCESS_ERROR=94
NZBGET_POSTPROCESS_NONE=95

# Check if the script is called from nzbget 15.0 or later
if not 'NZBOP_NZBLOG' in os.environ:
  print('*** NZBGet post-processing script ***')
  print('This script is supposed to be called from nzbget (15.0 or later).')
  sys.exit(NZBGET_POSTPROCESS_ERROR)

#if os.environ['NZBOP_VERSION'][0:5] < '11.0':
#  print("NZBGet Version %s is not supported. Please update NZBGet." % (str(os.environ['NZBOP_VERSION'])))
#  sys.exit(NZBGET_POSTPROCESS_ERROR)

print('[DETAIL] Script successfully started')
sys.stdout.flush()

print("Script triggered from NZBGet Version %s." % (str(os.environ['NZBOP_VERSION'])))
status = 0
if 'NZBPP_TOTALSTATUS' in os.environ:
  if not os.environ['NZBPP_TOTALSTATUS'] == 'SUCCESS':
    print("Download failed with status %s." % (os.environ['NZBPP_STATUS']))
    sys.exit(NZBGET_POSTPROCESS_ERROR)
  else:
    # Check par status
    if os.environ['NZBPP_PARSTATUS'] == '1' or os.environ['NZBPP_PARSTATUS'] == '4':
      print("Par-repair failed.")
      sys.exit(NZBGET_POSTPROCESS_ERROR)
    # Check unpack status
    if os.environ['NZBPP_UNPACKSTATUS'] == '1':
      print("Unpack failed.")
      sys.exit(NZBGET_POSTPROCESS_ERROR)
    if os.environ['NZBPP_UNPACKSTATUS'] == '0' and os.environ['NZBPP_PARSTATUS'] == '0':
    # Unpack was skipped due to nzb-file properties or due to errors during par-check
      if os.environ['NZBPP_HEALTH'] < 1000:
        print("Download health is compromised and Par-check/repair disabled or no .par2 files found.")
        print("Please check your Par-check/repair settings for future downloads.")
        sys.exit(NZBGET_POSTPROCESS_ERROR)
#      else:
#        print("Par-check/repair disabled or no .par2 files found, and Unpack not required. Health is ok so handle as though download successful.")
#        print("Please check your Par-check/repair settings for future downloads.")

# Search for files
unwantedFileExtensions = os.environ['NZBPO_UNWANTEDFILEEXTENSIONS'].split(',')
unwantedFileNames = os.environ['NZBPO_UNWANTEDFILENAMES'].split(',')
for dirpath, dirnames, filenames in os.walk(os.environ['NZBPP_DIRECTORY']):
  for file in filenames:
    filePath = os.path.join(dirpath, file)
    fileName, fileExtension = os.path.splitext(file)
    if fileExtension in unwantedFileExtensions: # If the file extension is unwanted
      print("\"%s\" is unwanted and will be deleted." % filePath)
      try: # Delete file
        os.unlink(filePath)
        print("File \"%s\" successfully deleted." % filePath)
      except:
        print("Error: unable to delete file \"%s\"." % filePath)
        sys.exit(NZBGET_POSTPROCESS_ERROR)
    elif file in unwantedFileNames: # If the filename is unwanted
      print("\"%s\" is unwanted and will be deleted." % filePath)
      try: # Delete file
        os.unlink(filePath)
        print("File \"%s\" successfully deleted." % filePath)
      except:
        print("Error: unable to delete file \"%s\"." % filePath)
        sys.exit(NZBGET_POSTPROCESS_ERROR)
    else:
      print("\"%s\" is not an unwanted file." % filePath)
else:
  print("No more files for processing.")

sys.exit(NZBGET_POSTPROCESS_SUCCESS)
