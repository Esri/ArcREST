from arcrest.agol import admin

if __name__ == "__main__":
    try:
        url = ""
        username = ""
        password = ""
        agol = admin.AGOL(username=username,password=password)

        results = agol.get_group_content('5d64803bfeeb4db7b105bd5692919a40')
        print results['total']
        for result in results['results']:
            print result['id']


    except ValueError, e:
        print e

