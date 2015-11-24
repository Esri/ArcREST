
"""
   This sample shows how to loop through the folders
   and print their titles

"""
from arcrest.security import AGOLTokenSecurityHandler
import arcrest

if __name__ == "__main__":
    username = ""#Username
    password = ""#password
    proxy_port = None
    proxy_url = None

    agolSH = AGOLTokenSecurityHandler(username=username,
                                      password=password)
    
    
    admin = arcrest.manageorg.Administration(securityHandler=agolSH)
    content = admin.content
    user = content.users.user()
    
    for folder in user.folders:
        title = folder['title']
        print("Analyzing {}".format(title))
        user.currentFolder = title
        print("Current folder is {}".format(user.currentFolder))
        print("Current folder has {} items".format(len(user.items))) 