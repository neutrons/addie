from addie.ui_table_tree import Ui_Dialog as UiDialog

try:
    from PyQt4.QtGui import QDialog, QTreeWidgetItem
    from PyQt4 import QtCore
except ImportError:
    try:
        from PyQt5.QtWidgets import QDialog, QTreeWidgetItem
        from PyQt5 import QtCore
    except ImportError:
        raise ImportError("Requires PyQt4 or PyQt5")

class TableTreeHandler:

    def __init__(self, parent=None):

        if parent.table_tree_ui == None:
            table_tree_ui = TableTree(parent=parent)
            table_tree_ui.show()
        else:
            parent.table_tree_ui.activateWindow()
            parent.table_tree_ui.setFocus()


class TableTree(QDialog):

    tree_column = 0

    def __init__(self, parent=None):
        self.parent = parent
        QDialog.__init__(self, parent=parent)
        self.ui = UiDialog()
        self.ui.setupUi(self)

        self.init_tree()

    def init_tree(self):
        # fill the self.ui.treeWidget
        # self.addItems(self.ui.treeWidget.invisibleRootItem())
        self.addItems(self.ui.treeWidget.invisibleRootItem())
        self.ui.treeWidget.itemChanged.connect(self.tree_item_changed)

    def addParent(self, parent, title, name):
        item = QTreeWidgetItem(parent, [title])
        item.setData(self.tree_column, QtCore.Qt.UserRole, '')
        item.setChildIndicatorPolicy(QTreeWidgetItem.ShowIndicator)
        item.setCheckState(self.tree_column, QtCore.Qt.Checked)
        item.setExpanded(True)
        return item

    def addChild(self, parent, title, name):
        item = QTreeWidgetItem(parent, [title])
        item.setData(self.tree_column, QtCore.Qt.UserRole, '')
        item.setCheckState(self.tree_column, QtCore.Qt.Checked)
        return item

    def addItems(self, parent):
        td = self.parent.tree_dict
        absolute_parent = parent

        tree_ui = {'h1': [],
                   'h2': [],
                   'h3': []}

        h1_index = 0
        h2_index = 0
        h3_index = 0

        def set_h_indexes(location, h1=None, h2=None, h3=None):
            location['h_index']['h1'] = h1
            location['h_index']['h2'] = h2
            location['h_index']['h3'] = h3

        for _key_h1 in td.keys():

            # if there are children, we need to use addParent
            if td[_key_h1]['children']:

                _h1_parent = self.addParent(absolute_parent,
                                            td[_key_h1]['name'],
                                            _key_h1)
                td[_key_h1]['ui'] = _h1_parent
                tree_ui['h1'].append(_h1_parent)

                for _key_h2 in td[_key_h1]['children'].keys():

                    # if there are children, we need to use addParent
                    if td[_key_h1]['children'][_key_h2]['children']:

                        _h2_parent = self.addParent(_h1_parent,
                                                    td[_key_h1]['children'][_key_h2]['name'],
                                                    _key_h2)
                        td[_key_h1]['children'][_key_h2]['ui'] = _h2_parent
                        tree_ui['h2'].append(_h2_parent)

                        for _key_h3 in td[_key_h1]['children'][_key_h2]['children']:
                            _h3_child = self.addChild(_h2_parent,
                                                      td[_key_h1]['children'][_key_h2]['children'][_key_h3]['name'],
                                                      _key_h3)
                            td[_key_h1]['children'][_key_h2]['children'][_key_h3]['ui'] = _h3_child

                            set_h_indexes(td[_key_h1]['children'][_key_h2]['children'][_key_h3], h3=h3_index)
                            tree_ui['h3'].append(_h3_child)
                            h3_index += 1

                    else: # key_h2 has no children, it's a leaf
                        _h3_child = self.addChild(_h1_parent,
                                                  td[_key_h1]['children'][_key_h2]['name'],
                                                  _key_h2)
                        td[_key_h1]['children'][_key_h2]['ui'] = _h3_child
                        tree_ui['h2'].append(_h3_child)
                        tree_ui['h3'].append(None)
                        h3_index += 1

                    set_h_indexes(td[_key_h1]['children'][_key_h2], h2=h2_index)
                    h2_index += 1

            else: #_key_h1 has no children, using addChild
                _child = self.addChild(absolute_parent,
                                       td[_key_h1]['name'],
                                       _key_h1)
                td[_key_h1]['ui'] = _child
                tree_ui['h1'].append(_child)
                tree_ui['h2'].append(None)
                tree_ui['h3'].append(None)
                h2_index += 1

            set_h_indexes(td[_key_h1], h1=h1_index)
            h1_index += 1
            h3_index += 1

            self.tree_ui = tree_ui

    def tree_item_changed(self, item, _):
        pass


    def closeEvent(self):
        self.parent.table_tree_ui = None

