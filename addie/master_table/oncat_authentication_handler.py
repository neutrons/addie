import pyoncat
import oauthlib

try:
    from PyQt4.QtGui import QMainWindow, QLineEdit, QApplication
    from PyQt4 import QtGui
except:
    try:
        from PyQt5.QtWidgets import QMainWindow, QLineEdit, QApplication
        from PyQt5 import QtGui
    except:
        raise ImportError("Requires PyQt4 or PyQt5")

from addie.ui_oncat_authentication import Ui_MainWindow as UiMainWindow


# Create token store
class InMemoryTokenStore(object):
    def __init__(self):
        self._token = None

    def set_token(self, token):
        self._token = token

    def get_token(self):
        return self._token


class OncatAuthenticationHandler:

    def __init__(self, parent=None):
        o_oncat = OncatAuthenticationWindow(parent=parent)
        o_oncat.show()
        if parent.oncat_authentication_ui_position:
            o_oncat.move(parent.oncat_authentication_ui_position)


class OncatAuthenticationWindow(QMainWindow):

    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent=parent)
        self.parent = parent

        self.ui = UiMainWindow()
        self.ui.setupUi(self)

        self.center()
        self.init_widgets()

    def center(self):
        frameGm = self.frameGeometry()
        screen = QApplication.desktop().screenNumber(QtGui.QApplication.desktop().cursor().pos())
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
        userid = str(self.ui.ucams.text())
        password = str(self.ui.password.text())

        # Initialize token store
        token_store = InMemoryTokenStore()

        # Setup ONcat object
        oncat = pyoncat.ONCat(
            'https://oncat.ornl.gov',
            client_id='cf46da72-9279-4466-bc59-329aea56bafe',
            client_secret=None,
            token_getter=token_store.get_token,
            token_setter=token_store.set_token,
            flow=pyoncat.RESOURCE_OWNER_CREDENTIALS_FLOW
        )

        try:
            oncat.login(userid, password)
        except:
            return False

        return True

    def ok_clicked(self):
        # do something
        if self.is_valid_password():
            self.close()

            self.parent.launch_import_from_database_handler()

        else:
            self.ui.password.setText("")
            self.ui.authentication_message.setVisible(True)

    def password_changed(self, password):
        self.ui.authentication_message.setVisible(False)

    def cancel_clicked(self):
        self.close()

    def closeEvent(self, c):
        self.parent.oncat_authentication_ui_position = self.pos()