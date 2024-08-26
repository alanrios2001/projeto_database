import enum
from datetime import datetime

from sqlalchemy import create_engine, ForeignKey, func, Column, Integer, Sequence
from sqlalchemy.orm import (
    relationship,
    mapped_column,
    Mapped,
    sessionmaker,
    DeclarativeBase,
)

from sqlalchemy.dialects.mysql import TIMESTAMP, TEXT, VARCHAR

USERNAME = "root"
PASSWORD = "root"
HOST = "localhost"
PORT = 3306
DATABASE = "sistema_hospitalar"

engine = create_engine('duckdb:///meu_banco.duckdb')

LocalSession = sessionmaker(engine, autocommit=False)


class SexoEnum(enum.Enum):
    M = "M"
    F = "F"


class BaseModel(DeclarativeBase):
    pass


class Pacientes(BaseModel):
    __tablename__ = "pacientes"

    id = Column(Integer, Sequence('paciente_id_seq'), primary_key=True)
    nome = mapped_column(VARCHAR(100), nullable=False)
    data_nascimento = mapped_column(TIMESTAMP, nullable=False)
    sexo: Mapped[SexoEnum] = mapped_column(nullable=False)
    endereco = mapped_column(TEXT, nullable=True)
    telefone = mapped_column(TEXT, nullable=True)
    email = mapped_column(TEXT, nullable=True)
    cpf = mapped_column(TEXT, nullable=True)
    rg = mapped_column(TEXT, nullable=True)

    prontuarios: Mapped['Prontuarios'] = relationship(back_populates="pacientes")
    atendimentos: Mapped['Atendimentos'] = relationship(back_populates="pacientes")


class Medicos(BaseModel):
    __tablename__ = "medicos"

    id = Column(Integer, Sequence('medicos_id_seq'), primary_key=True)
    nome = mapped_column(VARCHAR(100), nullable=False)
    crm = mapped_column(TEXT, nullable=False)
    especialidade = mapped_column(TEXT, nullable=True)
    telefone = mapped_column(TEXT, nullable=True)
    email = mapped_column(TEXT, nullable=True)

    atendimentos: Mapped['Atendimentos'] = relationship(back_populates="medicos")
    prontuarios: Mapped['Prontuarios'] = relationship(back_populates="medicos")


class Atendimentos(BaseModel):
    __tablename__ = "atendimentos"

    id = Column(Integer, Sequence('atendimentos_id_seq'), primary_key=True)
    id_paciente: Mapped[int] = mapped_column(ForeignKey("pacientes.id"))
    id_medico: Mapped[int] = mapped_column(ForeignKey("medicos.id"))
    data_atendimento = mapped_column(TIMESTAMP, default=datetime.now, server_default=func.now())
    motivo_atendimento = mapped_column(TEXT, nullable=True)
    diagnostico = mapped_column(TEXT, nullable=True)
    tratamento = mapped_column(TEXT, nullable=True)
    medicamentos = mapped_column(TEXT, nullable=True)
    exames = mapped_column(TEXT, nullable=True)
    observacoes = mapped_column(TEXT, nullable=True)

    medicos: Mapped['Medicos'] = relationship(back_populates="atendimentos")
    pacientes: Mapped['Pacientes'] = relationship(back_populates="atendimentos")


class Prontuarios(BaseModel):
    __tablename__ = "prontuarios"

    id = Column(Integer, Sequence('prontuarios_id_seq'), primary_key=True)
    id_paciente: Mapped[int] = mapped_column(ForeignKey("pacientes.id"))
    id_medico: Mapped[int] = mapped_column(ForeignKey("medicos.id"))
    data_entrada = mapped_column(TIMESTAMP, default=datetime.now, server_default=func.now())
    data_saida = mapped_column(TIMESTAMP, default=None, server_default=None)
    motivo_saida = mapped_column(TEXT, nullable=True)
    diagnostico = mapped_column(TEXT, nullable=True)
    tratamento = mapped_column(TEXT, nullable=True)
    medicamentos = mapped_column(TEXT, nullable=True)
    exames = mapped_column(TEXT, nullable=True)
    observacoes = mapped_column(TEXT, nullable=True)

    pacientes: Mapped['Pacientes'] = relationship(back_populates="prontuarios")
    medicos: Mapped['Medicos'] = relationship(back_populates="prontuarios")


def create_database():
    BaseModel.metadata.create_all(engine)


if __name__ == "__main__":
    create_database()
