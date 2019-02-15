#!/usr/bin/env python
import getpass
import pyoncat

# Create token store
class InMemoryTokenStore(object):
    def __init__(self):
        self._token = None

    def set_token(self, token):
        self._token = token

    def get_token(self):
        return self._token


def pyoncatForADDIE(useRcFile=True):
    # Get username and password
    userid = raw_input("UCAMS/XCAMS UserID: ")
    password  = getpass.getpass()

    # Initialize token store
    token_store = InMemoryTokenStore()

    # Setup ONcat object 
    oncat = pyoncat.ONCat(
        'https://oncat.ornl.gov',
        client_id = 'cf46da72-9279-4466-bc59-329aea56bafe',
        client_secret = None,
        token_getter = token_store.get_token,
        token_setter = token_store.set_token,
        flow = pyoncat.RESOURCE_OWNER_CREDENTIALS_FLOW
    )

    # Try to login
    oncat.login(userid, password)

    print("Successful login!!!")

if __name__ =="__main__":
    useRcFile= True 
    pyoncatForADDIE(useRcFile=useRcFile)
