from infra.configs.base import Base
from sqlalchemy import Column, String, Integer

class Cliente(Base):
    __tablename__ = 'cliente'

    id = Column(Integer, autoincrement=True, primary_key=True)
    cpf = Column(String(20), nullable=True)
    nome = Column(String(25), nullable=True)
    telefone_fixo = Column(String(20), nullable=False)
    telefone_celular = Column(String(20), nullable=False)
    genero = Column(String(20), nullable=False)
    cep = Column(String(20), nullable=False)
    logradouro = Column(String(25), nullable=False)
    numero = Column(String(5), nullable=False)
    complemento = Column(String(10), nullable=False)
    bairro = Column(String(15), nullable=False)
    municipio = Column(String(40), nullable=False)
    estado = Column(String(15), nullable=False)

    def __repr__(self):
        return f'ID do cliente: {self.id}\nCliente: {self.nome}\nCPF:' \
               f'{self.cpf}\nGênero: {self.genero}\n' \
               f'Contatos:\nTelefone Fixo: {self.telefone_fixo}    Telefone Celular:' \
               f' {self.telefone_celular}' \
               f'Endereço: {self.logradouro}, {self.numero} - {self.complemento}\n CEP: {self.cep} - ' \
               f'{self.bairro} - {self.municipio} - {self.estado}'
