from __future__ import (absolute_import, division, print_function)

from qtpy.QtWidgets import QMainWindow, QLineEdit, QApplication
from addie.utilities import load_ui

try:
    import pyoncat
except ImportError:
    print('failed to import pyoncat')
    pyoncat = None


# Create token store
class InMemoryTokenStore(object):
    def __init__(self):
        self._token = None

    def set_token(self, token):
        self._token = token

    def get_token(self):
        return self._token


class OncatAuthenticationHandler:
    def __init__(self, parent=None, next_ui='from_database_ui', next_function=None):
        o_oncat = OncatAuthenticationWindow(parent=parent,
                                            next_ui=next_ui,
                                            next_function=next_function)
        parent.oncat_authentication_ui = o_oncat
        if parent.oncat_authentication_ui_position:
            o_oncat.move(parent.oncat_authentication_ui_position)
        o_oncat.show()

        parent.oncat_authentication_ui.activateWindow()
        parent.oncat_authentication_ui.setFocus()


class OncatAuthenticationWindow(QMainWindow):
    def __init__(self, parent=None, next_ui='from_database_ui', next_function=None):
        QMainWindow.__init__(self, parent=parent)
        self.parent = parent
        self.next_ui = next_ui
        self.next_function = next_function

        self.ui = load_ui('oncat_authentication.ui', baseinstance=self)

        self.center()
        self.init_widgets()
        self.ui.password.setFocus()

    def center(self):
        frameGm = self.frameGeometry()
        screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
        centerPoint = QApplication.desktop().screenGeometry(screen).center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())

    def init_widgets(self):
        self.ui.ucams.setText(self.parent.ucams)
        self.ui.password.setEchoMode(QLineEdit.Password)
        self.ui.password.setFocus()
        self.ui.authentication_message.setVisible(False)
        self.ui.authentication_message.setStyleSheet("color: red")

    def is_valid_password(self):
        userid = str(self.ui.ucams.text()).strip()
        password = str(self.ui.password.text())

        # Initialize token store
        token_store = InMemoryTokenStore()

        # # Setup ONcat object
        # oncat = pyoncat.ONCat(
        #     'https://oncat.ornl.gov',
        #     client_id='cf46da72-9279-4466-bc59-329aea56bafe',
        #     client_secret=None,
        #     token_getter=token_store.get_token,
        #     token_setter=token_store.set_token,
        #     flow=pyoncat.RESOURCE_OWNER_CREDENTIALS_FLOW
        # )

        # pyoncat is not available
        if pyoncat is None:
            return False

        # Setup ONcat object
        oncat = pyoncat.ONCat(
            'https://oncat.ornl.gov',
            client_id='cf46da72-9279-4466-bc59-329aea56bafe',
            scopes = ['api:read', 'settings:read'],
            client_secret=None,
            token_getter=token_store.get_token,
            token_setter=token_store.set_token,
            flow=pyoncat.RESOURCE_OWNER_CREDENTIALS_FLOW
        )

        try:
            oncat.login(userid, password)
            self.parent.ucams = userid
            self.parent.oncat = oncat
        except:
            return False

        return True

    def ok_clicked(self):
        # do something
        if self.is_valid_password():
            self.close()
            self.next_function()
            # if self.next_ui == 'from_database_ui':
            #     self.parent.launch_import_from_database_handler()
            # elif self.next_ui == 'from_run_number_ui':
            #     self.parent.launch_import_from_run_number_handler()

        else:
            self.ui.password.setText("")
            self.ui.authentication_message.setVisible(True)

    def password_changed(self, password):
        self.ui.authentication_message.setVisible(False)

    def cancel_clicked(self):
        self.close()

    def closeEvent(self, c):
        self.parent.oncat_authentication_ui_position = self.pos()
