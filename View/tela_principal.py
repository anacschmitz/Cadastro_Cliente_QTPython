import json

import requests
from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QComboBox, QWidget, QPushButton, QMessageBox, QSizePolicy, \
    QLabel, QLineEdit, QTableWidget, QAbstractItemView, QTableWidgetItem

from Model.cliente import Cliente
from Controller.Cliente_dao import DataBase

class MainWindow(QMainWindow):
    txt_telefone_fixo: QLineEdit | QLineEdit

    def __init__(self):
        super().__init__()

        self.setMinimumSize(500, 900)

        self.setWindowTitle('Cadastro de clientes')

        self.lbl_cpf = QLabel('Cpf')
        self.txt_cpf = QLineEdit()
        self.txt_cpf.setInputMask('000.000.000-00')
        self.lbl_nome = QLabel('Nome')
        self.txt_nome = QLineEdit()
        self.lbl_telefone_fixo = QLabel('Telefone Fixo')
        self.txt_telefone_fixo = QLineEdit()
        self.txt_telefone_fixo.setInputMask('(00)0000-0000')
        self.lbl_ttelefone_celular = QLabel('Telefone Celular')
        self.txt_telefone_celular = QLineEdit()
        self.txt_telefone_celular.setInputMask('(00)00000-0000')
        self.lbl_sexo = QLabel('Sexo')
        self.cb_sexo = QComboBox()
        self.cb_sexo.addItems(['Não Informado', 'Masculino', 'Feminino'])
        self.lbl_cep = QLabel('Cep')
        self.txt_cep = QLineEdit()
        self.txt_cep.setInputMask('00.000-000')
        self.lbl_logradouro = QLabel('Logradouro')
        self.txt_logradouro = QLineEdit()
        self.lbl_numero = QLabel('Numero')
        self.txt_numero = QLineEdit()
        self.lbl_complemento = QLabel('Complemento')
        self.txt_complemento = QLineEdit()
        self.lbl_bairro = QLabel('Bairro')
        self.txt_bairro = QLineEdit()
        self.lbl_municipio = QLabel('Município')
        self.txt_municipio = QLineEdit()
        self.lbl_estado = QLabel('Estado')
        self.txt_estado = QLineEdit()
        self.btn_salvar = QPushButton('Salvar')
        self.btn_limpar = QPushButton('Limpar')
        self.btn_remover = QPushButton('Remover')
        self.tabela_clientes = QTableWidget()

        self.tabela_clientes.setColumnCount(12)
        self.tabela_clientes.setHorizontalHeaderLabels(['CPF', 'Nome', 'Telefone Fixo', 'Telefone Celular'
                                                        'Sexo', 'Cep', 'Logradouro', 'Número',
                                                        'Complemento', 'Bairro', 'Município', 'Estado'])

        self.tabela_clientes.setSelectionMode(QAbstractItemView.NoSelection)
        self.tabela_clientes.setEditTriggers(QAbstractItemView.NoEditTriggers)

        layout = QVBoxLayout()
        layout.addWidget(self.lbl_cpf)
        layout.addWidget(self.txt_cpf)
        layout.addWidget(self.lbl_nome)
        layout.addWidget(self.txt_nome)
        layout.addWidget(self.lbl_telefone_fixo)
        layout.addWidget(self.txt_telefone_fixo)
        layout.addWidget(self.lbl_sexo)
        layout.addWidget(self.cb_sexo)
        layout.addWidget(self.lbl_cep)
        layout.addWidget(self.txt_cep)
        layout.addWidget(self.lbl_logradouro)
        layout.addWidget(self.txt_logradouro)
        layout.addWidget(self.lbl_numero)
        layout.addWidget(self.txt_numero)
        layout.addWidget(self.lbl_complemento)
        layout.addWidget(self.txt_complemento)
        layout.addWidget(self.lbl_bairro)
        layout.addWidget(self.txt_bairro)
        layout.addWidget(self.lbl_municipio)
        layout.addWidget(self.txt_municipio)
        layout.addWidget(self.lbl_estado)
        layout.addWidget(self.txt_estado)
        layout.addWidget(self.tabela_clientes)
        layout.addWidget(self.btn_salvar)
        layout.addWidget(self.btn_limpar)
        layout.addWidget(self.btn_remover)

        self.container = QWidget()
        self.container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setCentralWidget(self.container)
        self.container.setLayout(layout)

        self.btn_remover.setVisible(False)
        self.btn_salvar.clicked.connect(self.salvar_cliente)
        self.popula_tabela_clientes()
        self.tabela_clientes.cellDoubleClicked.connect(self.carrega_dados)
        self.txt_cpf.editingFinished.connect(self.consulta_cliente)
        self.txt_cep.editingFinished.connect(self.consulta_endereco)
        self.btn_remover.clicked.connect(self.remover_cliente)
        self.btn_limpar.clicked.connect(self.limpar_campos)



    def consulta_cliente(self):
        if self.txt_cpf.text().replace('.', '').replace('-', '') != '':
            db = DataBase()
            retorno = db.consultar_cliente(str(self.txt_cpf.text()).replace('.', '').replace('.', ''))

            if retorno is not None:
                self.btn_salvar.setText('Atualizar')
                msg = QMessageBox()
                msg.setWindowTitle('Cliente já cadastrado')
                msg.setText(f'O CPF {self.txt_cpf.text()} já está cadastrado')

                msg.exec()
                self.txt_nome.setText(retorno[1])
                self.txt_telefone_fixo.setText(retorno[2])
                self.txt_telefone_celular.setText(retorno[3])
                sexo_map = {'Não Informado':0, 'Feminino': 1, 'Masculino': 2}
                self.cb_sexo.setCurrentIndex(sexo_map.get(retorno[4], 0))
                self.txt_cep.setText(retorno[5])
                self.txt_logradouro.setText(retorno[6])
                self.txt_numero.setText((retorno[7]))
                self.txt_complemento.setText(retorno[8])
                self.txt_bairro.setText(retorno[9])
                self.txt_municipio.setText(retorno[10])
                self.txt_estado.setText(retorno[11])
                self.btn_remover.setVisible(True)

    def remover_cliente(self):
        msg = QMessageBox()
        msg.setWindowTitle('Remover Cliente')
        msg.setText('Ese cliente será removido.')
        msg.setInformativeText(f'Você deseja remover o cliente de cpf {self.txt_cpf.text()} ?')
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg.button(QMessageBox.Yes).setText('Sim')
        msg.button(QMessageBox.No).setText('Não')
        resposta = msg.exec()
        self.limpar_campos()

        if resposta == QMessageBox.Yes:
            db = DataBase()
            retorno = db.deletar_cliente(self.txt_cpf.text())

            if retorno == 'OK':
                nv_msg = QMessageBox()
                nv_msg.setWindowTitle('Remover Cliente')
                nv_msg.setText('Cliente removido com sucesso.')
                nv_msg.exec()
            else:
                nv_msg = QMessageBox()
                nv_msg.setWindowTitle('Remover Cliente')
                nv_msg.setText('Erro ao remover cliente.')
                nv_msg.exec()
        self.txt_cpf.setReadOnly(False)
        self.popula_tabela_clientes()

    def salvar_cliente(self):
        db = DataBase()

        cliente = Cliente(
            cpf=self.txt_cpf.text(),
            nome=self.txt_nome.text(),
            telefone_fixo=self.txt_telefone_fixo.text(),
            telefone_celular=self.txt_telefone_celular.text(),
            sexo=self.cb_sexo.currentText(),
            cep=self.txt_cep.text(),
            logradouro=self.txt_logradouro.text(),
            numero=self.txt_numero.text(),
            complemento=self.txt_complemento.text(),
            bairro=self.txt_bairro.text(),
            municipio=self.txt_municipio.text(),
            estado=self.txt_estado.text(),
        )


        if self.btn_salvar.text() == 'Salvar':
            retorno = db.registrar_cliente(cliente)

            if retorno == 'Ok':
                msg = QMessageBox()
                msg.setWindowTitle('Cadastro realizado')
                msg.setText('Cadastro realizado com sucesso')
                msg.exec()
                self.limpar_campos()
            elif 'UNIQUE constraint failed:' in retorno.args[0]:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setWindowTitle('Cliente já cadastrado')
                msg.setText(f'O CPF {self.txt_cpf.text()} já está cadastrado')
                msg.exec()
            else:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setWindowTitle('Erro ao cadastrar')
                msg.setText(f'Erro ao cadastrar o cliente, verifique os dados')
                msg.exec()

        elif self.btn_salvar.text() == 'Atualizar':

            retorno = db.atualizar_cliente(cliente)
            if retorno == 'OK':
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setWindowTitle('Cadastro Atualizado ')
                msg.setText('Cadastro atualizado com sucesso')
                msg.exec()
                self.limpar_campos()
            else:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setWindowTitle('Erro ao Atualizar')
                msg.setText('Erro ao cadastrar verfique os dados inseridos')
                msg.exec()

        self.popula_tabela_clientes()
        self.txt_cpf.setReadOnly(False)

    def limpar_campos(self):
        for widget in self.container.children():
            if isinstance(widget, QLineEdit):
                widget.clear()
            elif isinstance(widget, QComboBox):
                widget.setCurrentIndex(0)
        self.btn_remover.setVisible(False)
        self.btn_salvar.setText('Salvar')
        self.txt_cpf.setReadOnly(False)

    def consulta_endereco(self):
        url = f'https://viacep.com.br/ws/{str(self.txt_cep.text()).replace(".", "").replace("-", "")}/json/'
        response = requests.get(url)
        endereco = json.loads(response.text)

        if response.status_code == 200 and 'erro' not in endereco:
            self.txt_logradouro.setText(endereco['logradouro'])
            self.txt_bairro.setText(endereco['bairro'])
            self.txt_municipio.setText(endereco['localidade'])
            self.txt_estado.setText(endereco['uf'])
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowTitle('Consultar CEP')
            msg.setText('Erro ao consultar CEP verifique os dados inseridos')
            msg.exec()

    def popula_tabela_clientes(self):
        self.tabela_clientes.setRowCount(0)
        db = DataBase()
        lista_clientes = db.consultar_todos_cliente()
        self.tabela_clientes.setRowCount(len(lista_clientes))

        for linha, cliente in enumerate(lista_clientes):
            for coluna, valor in enumerate(cliente):
                self.tabela_clientes.setItem(linha, coluna, QTableWidgetItem(str(valor)))

    def carrega_dados(self, row, column):
        self.txt_cpf.setText(self.tabela_clientes.item(row, 0).text())
        self.txt_nome.setText(self.tabela_clientes.item(row, 1).text())
        self.txt_telefone_fixo.setText(self.tabela_clientes.item(row, 2).text())
        self.txt_telefone_celular.setText(self.tabela_clientes.item(row, 3).text())
        sexo_map = {'Não Informado': 0, 'Masculino': 1 , 'Feminino': 2}
        self.cb_sexo.setCurrentIndex(sexo_map.get(self.tabela_clientes.item(row, 4).text(), 0))
        self.txt_cep.setText(self.tabela_clientes.item(row, 5).text())
        self.txt_logradouro.setText(self.tabela_clientes.item(row, 6).text())
        self.txt_numero.setText(self.tabela_clientes.item(row, 7).text())
        self.txt_complemento.setText(self.tabela_clientes.item(row, 8).text())
        self.txt_bairro.setText(self.tabela_clientes.item(row, 9).text())
        self.txt_municipio.setText(self.tabela_clientes.item(row, 10).text())
        self.txt_estado.setText(self.tabela_clientes.item(row, 11).text())
        self.btn_salvar.setText('Atualizar')
        self.btn_remover.setVisible(True)
        self.txt_cpf.setReadOnly(True)


