from arcrest.agol import layer

if __name__ == "__main__":
    try:
        url = ""
        username = ""
        password = ""
        fl = layer.FeatureLayer(url=url, username=username, password=password)
        #  Add attachment to a record
        fl.addAttachment(oid=1, file_path=r"c:\temp\Desert.jpg")
        # Delete all attachments with the name Desert.jpg
        for attach in fl.listAttachments(oid=1)['attachmentInfos']:
            if attach['name'] == "Desert.jpg":
                fl.deleteAttachment(oid=1, attachment_id=attach['parentID'])
            else:
                print attach['name']

    except ValueError, e:
        print e


