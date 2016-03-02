from __future__ import print_function
from __future__ import absolute_import
import arcrest

if __name__ == "__main__":
    sh = arcrest.AGOLTokenSecurityHandler(username="username", password="password")
    admin = arcrest.manageorg.Administration(securityHandler=sh)
    user = admin.content.users.user()
    ip = arcrest.manageorg.ItemParameter()
    ip.title = "A very large fgdb"
    ip.type = "File Geodatabase"
    ip.tags = "fgdb"
    ip.description = "description"
    ip.snippet = "snippet"
    res = user.addItem(itemParameters=ip,
                       filePath=r"C:\temp3\40a87ec04f334df8bd92d9842f19570f.zip",
                       multipart=True)

    # the result object is a UserItem object, not JSON.  This is for version 3.5.3/3.5.4
