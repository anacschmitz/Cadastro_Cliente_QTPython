import sys
from PySide6.QtWidgets import QApplication

from Controller.Cliente_dao import DataBase
from View.tela_principal import MainWindow

db = DataBase()
db.connect()
db.create_table_cliente()
db.close_connection()

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()