import json

import requests
from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QComboBox, QWidget, QPushButton, QMessageBox, QSizePolicy, \
    QLabel, QLineEdit, QTableWidget, QAbstractItemView, QTableWidgetItem, QTextEdit, QHeaderView

from infra.configs.connection import DBConnectionHandler
from infra.entities.Cliente import Cliente
from infra.repository.cliente_repository import ClienteRepository


class MainWindow(QMainWindow):
    # txt_telefone_fixo: QLineEdit | QLineEdit

    def __init__(self):
        super().__init__()

        conn = DBConnectionHandler()
        self.setMinimumSize(500, 800)

        self.setWindowTitle('Cadastro de clientes')

        self.lbl_cpf = QLabel('Cpf')
        self.txt_cpf = QLineEdit()
        self.txt_cpf.setInputMask('000.000.000-00')
        self.lbl_nome = QLabel('Nome')
        self.txt_nome = QLineEdit()
        self.lbl_telefone_fixo = QLabel('Telefone Fixo')
        self.txt_telefone_fixo = QLineEdit()
        self.txt_telefone_fixo.setInputMask('(00)0000-0000')
        self.lbl_telefone_celular = QLabel('Telefone Celular')
        self.txt_telefone_celular = QLineEdit()
        self.txt_telefone_celular.setInputMask('(00)00000-0000')
        self.lbl_genero = QLabel('Sexo')
        self.cb_genero = QComboBox()
        self.cb_genero.addItems(['Não Informado', 'Masculino', 'Feminino'])
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
        self.btn_atualizar = QPushButton('Atualizar')
        self.tabela_clientes = QTableWidget()

        self.tabela_clientes.setColumnCount(13)
        self.tabela_clientes.setHorizontalHeaderLabels(['CPF', 'Nome', 'Telefone Fixo', 'Telefone Celular',
                                                        'Sexo', 'Cep', 'Logradouro',
                                                        'Número',
                                                        'Complemento', 'Bairro', 'Município', 'Estado'])

        header = self.tabela_clientes.horizontalHeader()
        for i in range(self.tabela_clientes.columnCount()):
            if i != 2:
                header.setSectionResizeMode(i, QHeaderView.ResizeToContents)

        self.tabela_clientes.setSelectionMode(QAbstractItemView.NoSelection)
        self.tabela_clientes.setEditTriggers(QAbstractItemView.NoEditTriggers)

        layout = QVBoxLayout()
        layout.addWidget(self.lbl_cpf)
        layout.addWidget(self.txt_cpf)
        layout.addWidget(self.lbl_nome)
        layout.addWidget(self.txt_nome)
        layout.addWidget(self.lbl_telefone_fixo)
        layout.addWidget(self.txt_telefone_fixo)
        layout.addWidget(self.lbl_genero)
        layout.addWidget(self.cb_genero)
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

        self.tabela_clientes.cellDoubleClicked.connect(self.carrega_dados)

        self.btn_remover.setVisible(True)
        self.btn_salvar.clicked.connect(self.salvar_cliente)
        self.popula_tabela_clientes()
        self.btn_remover.clicked.connect(self.remover_cliente)

        self.btn_limpar.clicked.connect(self.limpar_campos)
        self.popula_tabela_clientes()

        self.txt_cpf.editingFinished.connect(self.consulta_cliente)
        self.txt_cep.editingFinished.connect(self.consulta_endereco)

    def consulta_cliente(self):
        if self.txt_cpf.text().replace('.', '').replace('-', '') != '':

            db = ClienteRepository()
            retorno = db.select(self.txt_cpf.text())

            if retorno is not None:
                self.btn_salvar.setText('Atualizar')
                msg = QMessageBox()
                msg.setWindowTitle('Cliente já cadastrado')
                msg.setText(f'O CPF {self.txt_cpf.text()} já está cadastrado')

                msg.exec()
                self.txt_cpf.setText(retorno[0])
                self.txt_nome.setText(retorno[1])
                self.txt_telefone_fixo.setText(retorno[2])
                self.txt_telefone_celular.setText(retorno[3])
                genero_map = {'Não Informado':0, 'Feminino': 1, 'Masculino': 2}
                self.cb_genero.setCurrentIndex(genero_map.get(retorno[4], 0))
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
        msg.setText('Esse cliente será removido.')
        msg.setInformativeText(f'Você deseja remover o cliente de cpf {self.txt_cpf.text()} ?')
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg.button(QMessageBox.Yes).setText('Sim')
        msg.button(QMessageBox.No).setText('Não')
        resposta = msg.exec()
        self.limpar_campos()

        if resposta == QMessageBox.Yes:
            db = ClienteRepository()
            retorno = db.delete(self.txt_cpf.text())

            if retorno == 'OK':
                new_msg = QMessageBox()
                new_msg.setWindowTitle('Remover Cliente')
                new_msg.setText('Cliente removido com sucesso.')
                new_msg.exec()
                self.limpar_campos()
            else:
                new_msg = QMessageBox()
                new_msg.setWindowTitle('Remover Cliente')
                new_msg.setText('Erro ao remover cliente.')
                new_msg.exec()

        self.txt_cpf.setReadOnly(False)
        self.btn_limpar.clicked.connect(self.limpar_campos)
        self.btn_atualizar.clicked.connect(self.salvar_cliente)
        self.popula_tabela_clientes()

    def salvar_cliente(self):
        db = ClienteRepository()

        cliente = Cliente(
            cpf=self.txt_cpf.text(),
            nome=self.txt_nome.text(),
            telefone_fixo=self.txt_telefone_fixo.text(),
            telefone_celular=self.txt_telefone_celular.text(),
            genero=self.cb_genero.currentText(),
            cep=self.txt_cep.text(),
            logradouro=self.txt_logradouro.text(),
            numero=self.txt_numero.text(),
            complemento=self.txt_complemento.text(),
            bairro=self.txt_bairro.text(),
            municipio=self.txt_municipio.text(),
            estado=self.txt_estado.text(),
        )

        if self.btn_salvar.text() == 'Salvar':
            retorno = db.insert(cliente)
            print(retorno)

            if retorno == 'ok':
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

            cliente.cpf = self.txt_cpf.text()
            db.update(cliente)

            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setWindowTitle('Cadastro Atualizado ')
            msg.setText('Cadastro atualizado com sucesso')
            msg.exec()
            self.limpar_campos()

        self.popula_tabela_clientes()
        # self.txt_cpf.setReadOnly(True)

    def limpar_campos(self):
        for widget in self.container.children():
            if isinstance(widget, QTextEdit):
                widget.clear()
            elif isinstance(widget, QLineEdit):
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
        conn = ClienteRepository()
        lista_clientes = conn.select_all()
        self.tabela_clientes.setRowCount(len(lista_clientes))

        linha = 0
        for cliente in lista_clientes:
            valores = [cliente.cpf, cliente.nome, cliente.telefone_fixo, cliente.telefone_celular,
                       cliente.genero, cliente.cep, cliente.logradouro, cliente.numero,
                       cliente.complemento, cliente.bairro, cliente.municipio, cliente.estado]
            for valor in valores:
                item = QTableWidgetItem(str(valor))
                self.tabela_clientes.setItem(linha, valores.index(valor), item)
                self.tabela_clientes.item(linha, valores.index(valor))
            linha += 1

    def carrega_dados(self, row, column):
        self.txt_cpf.setText(self.tabela_clientes.item(row, 0).text())
        self.txt_nome.setText(self.tabela_clientes.item(row, 1).text())
        self.txt_telefone_fixo.setText(self.tabela_clientes.item(row, 2).text() if self.tabela_clientes.item(row, 2) is not None else '')
        self.txt_telefone_celular.setText(self.tabela_clientes.item(row, 3).text() if self.tabela_clientes.item(row, 3) is not None else '')
        sexo_map = {'Não Informado': 0, 'Masculino': 1, 'Feminino': 2}
        self.cb_genero.setCurrentIndex(sexo_map.get(self.tabela_clientes.item(row, 4).text(), 0))
        self.txt_cep.setText(self.tabela_clientes.item(row, 5).text() if self.tabela_clientes.item(row, 5) is not None else '')
        self.txt_logradouro.setText(self.tabela_clientes.item(row, 6).text() if self.tabela_clientes.item(row, 6) is not None else '')
        self.txt_numero.setText(self.tabela_clientes.item(row, 7).text() if self.tabela_clientes.item(row, 7) is not None else '')
        self.txt_complemento.setText(self.tabela_clientes.item(row, 8).text() if self.tabela_clientes.item(row, 8) is not None else '')
        self.txt_bairro.setText(self.tabela_clientes.item(row, 9).text() if self.tabela_clientes.item(row, 9) is not None else '')
        self.txt_municipio.setText(self.tabela_clientes.item(row, 10).text() if self.tabela_clientes.item(row, 10) is not None else '')
        self.txt_estado.setText(self.tabela_clientes.item(row, 11).text() if self.tabela_clientes.item(row, 11) is not None else '')
        self.btn_salvar.setText('Atualizar')
        self.btn_remover.setVisible(True)
        self.txt_cpf.setReadOnly(True)
