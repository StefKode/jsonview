import os
import sys
import json
from PyQt6.QtWidgets import QMainWindow, QApplication, QHeaderView
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6 import QtCore
from ui_jsontree import Ui_MainWindow


class MainWindow (QMainWindow):
    def __init__(self):
        QMainWindow.__init__( self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self._model = QStandardItemModel()
        self._model.setColumnCount(2)
        self.ui.treeView.setModel(self._model)

        # Set style options to ensure branch lines are visible
        self.ui.treeView.setAlternatingRowColors(True)
        self.ui.treeView.setStyleSheet(
            """
            QTreeView {
                background-color: #fff;
                alternate-background-color: #eee;
                color: #000;
            }
            QTreeView::branch:has-siblings:!adjoins-item{
              border-image:url(images/vline.png) 0;
            }
            QTreeView::branch:has-siblings:adjoins-item{
              border-image:url(images/branch-more.png) 0;
            }
            QTreeView::branch:!has-children:!has-siblings:adjoins-item{
              border-image:url(images/branch-end.png) 0;
            }
            QTreeView::branch:has-children:!has-siblings:closed,
            QTreeView::branch:closed:has-children:has-siblings{
              border-image:none;
              image:url(images/branch-closed.png);
            }
            QTreeView::branch:open:has-children:!has-siblings,
            QTreeView::branch:open:has-children:has-siblings{
              border-image:none;
              image:url(images/branch-open.png);
            }
            """
        )

        with open("data.json", "r") as f:
            data = f.read()
        self.add_items(self._model, json.loads(data))
        self.ui.treeView.expandAll()
        self.ui.treeView.header().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)

    def add_items(self, parent, data):
        """
        Recursively add items to the tree view from JSON data.
        """
        if isinstance(data, dict):
            for key, value in data.items():
                key_item = QStandardItem(key)
                key_item.setEditable(False)
                if isinstance(value, (dict, list)):
                    # If value is dict or list, create an empty item in the second column
                    value_item = QStandardItem("")
                    parent.appendRow([key_item, value_item])
                    self.add_items(key_item, value)  # Recursively add children to the key
                else:
                    # If value is primitive, directly add to the second column
                    value_item = QStandardItem(str(value))
                    parent.appendRow([key_item, value_item])
        elif isinstance(data, list):
            for index, value in enumerate(data):
                key_item = QStandardItem(f"[{index}]")
                key_item.setEditable(False)
                if isinstance(value, (dict, list)):
                    # Handle nested dict or list
                    value_item = QStandardItem("")
                    parent.appendRow([key_item, value_item])
                    self.add_items(key_item, value)
                else:
                    # Primitive value, set it in the second column
                    value_item = QStandardItem(str(value))
                    parent.appendRow([key_item, value_item])
        else:
            # Primitive value case (int, str, etc.)
            value_item = QStandardItem(str(data))
            parent.appendRow([QStandardItem("Value"), value_item])



# Start the software
env = QtCore.QProcessEnvironment.systemEnvironment()
script_d = os.path.dirname(os.path.realpath(__file__))
os.chdir(script_d)

app = QApplication(sys.argv)
app.setStyle("Fusion")
ui = MainWindow()
ui.show()
sys.exit(app.exec())

