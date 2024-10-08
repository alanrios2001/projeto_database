import enum
import os
from datetime import datetime

from sqlalchemy import (
    create_engine,
    ForeignKey,
    func,
    Column,
    Integer,
    Sequence,
    text,
    DATETIME,
    FLOAT,
    UniqueConstraint,
)
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import (
    relationship,
    mapped_column,
    Mapped,
    sessionmaker,
    DeclarativeBase,
)

from sqlalchemy.ext.asyncio import async_sessionmaker

from sqlalchemy.dialects.mysql import VARCHAR
from sqlalchemy.sql.ddl import CreateTable

from config import settings

USERNAME = settings.database.USERNAME
PASSWORD = settings.database.PASSWORD
HOST = settings.database.HOST
PORT = settings.database.PORT
DATABASE = settings.database.DATABASE


connection_string = f"mysql+mysqldb://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/"

default_engine = create_engine(connection_string)


def create_database():
    with default_engine.connect() as conn:
        conn.execute(text("CREATE DATABASE IF NOT EXISTS sistema_hospitalar"))


create_database()

engine = create_engine(connection_string + DATABASE)

async_engine = create_async_engine(
    connection_string.replace("mysqldb", "asyncmy") + DATABASE
)

LocalSession = sessionmaker(engine, autocommit=False)

LocalAsyncSession = async_sessionmaker(async_engine, autocommit=False)


base_dir = os.path.dirname(os.path.abspath(__file__))
duck_db_path = os.path.join(base_dir, "sistema_hospitalar.duckdb")

duck_db_engine = create_engine(f"duckdb:///{duck_db_path}")

LocalSessionDuckDB = sessionmaker(duck_db_engine, autocommit=False)


class GeneroEnum(enum.Enum):
    MASCULINO = "MASCULINO"
    FEMININO = "FEMININO"


class StatusEnum(enum.Enum):
    DISPONIVEL = "DISPONIVEL"
    EM_USO = "EM_USO"
    EM_MANUTENCAO = "EM_MANUTENCAO"
    QUEBRADO = "QUEBRADO"


class TipoTransacaoEnum(enum.Enum):
    ENTRADA = "ENTRADA"
    SAIDA = "SAIDA"


class TipoConsultaEnum(enum.Enum):
    ROTINA = "ROTINA"
    URGENCIA = "URGENCIA"
    RETORNO = "RETORNO"


class EspecialidadeEnum(enum.Enum):
    CARDIOLOGISTA = "CARDIOLOGISTA"
    CLINICO_GERAL = "CLINICO_GERAL"
    DERMATOLOGISTA = "DERMATOLOGISTA"
    ENDOCRINOLOGISTA = "ENDOCRINOLOGISTA"
    GINECOLOGISTA = "GINECOLOGISTA"
    NEUROLOGISTA = "NEUROLOGISTA"
    OFTALMOLOGISTA = "OFTALMOLOGISTA"
    ORTOPEDISTA = "ORTOPEDISTA"
    OTORRINOLARINGOLOGISTA = "OTORRINOLARINGOLOGISTA"
    PEDIATRA = "PEDIATRA"
    PSIQUIATRA = "PSIQUIATRA"
    UROLOGISTA = "UROLOGISTA"
    NUTRICIONISTA = "NUTRICIONISTA"
    FISIOTERAPEUTA = "FISIOTERAPEUTA"
    PSICOLOGO = "PSICOLOGO"
    FONOAUDIOLOGO = "FONOAUDIOLOGO"
    FARMACEUTICO = "FARMACEUTICO"


class BaseModel(DeclarativeBase):
    pass


class TransacoesFinanceiras(BaseModel):
    __tablename__ = "transacoes_financeiras"

    id = Column(
        Integer,
        Sequence("transacoes_financeiras_id_seq"),
        primary_key=True,
        autoincrement=True,
    )
    paciente_id: Mapped[int] = mapped_column(ForeignKey("pacientes.id"))
    tipo_transacao: Mapped[TipoTransacaoEnum] = mapped_column(nullable=False)
    valor = mapped_column(FLOAT, nullable=False)
    data = mapped_column(DATETIME, default=datetime.now, server_default=func.now())
    created_at = mapped_column(
        DATETIME, default=datetime.now, server_default=func.now()
    )
    deleted_at = mapped_column(DATETIME, default=None, server_default=None)

    paciente: Mapped["Pacientes"] = relationship(
        back_populates="transacoes_financeiras"
    )


class Pacientes(BaseModel):
    __tablename__ = "pacientes"

    id = Column(
        Integer, Sequence("paciente_id_seq"), primary_key=True, autoincrement=True
    )
    nome = mapped_column(VARCHAR(100), nullable=False)
    data_nascimento = mapped_column(DATETIME, nullable=False)
    genero: Mapped[GeneroEnum] = mapped_column(nullable=False)
    endereco = mapped_column(VARCHAR(250), nullable=True)
    telefone = mapped_column(VARCHAR(50), nullable=True)
    email = mapped_column(VARCHAR(100), nullable=True)
    created_at = mapped_column(
        DATETIME, default=datetime.now, server_default=func.now()
    )
    updated_at = mapped_column(
        DATETIME, default=datetime.now, server_default=func.now()
    )
    deleted_at = mapped_column(DATETIME, default=None, server_default=None)

    transacoes_financeiras: Mapped["TransacoesFinanceiras"] = relationship(
        back_populates="paciente"
    )
    consultas: Mapped["Consultas"] = relationship(back_populates="paciente")
    prontuario: Mapped["Prontuarios"] = relationship(back_populates="paciente")


class Medicos(BaseModel):
    __tablename__ = "profissionais_saude"

    id = Column(
        Integer, Sequence("medicos_id_seq"), primary_key=True, autoincrement=True
    )
    nome = mapped_column(VARCHAR(100), nullable=False)
    genero: Mapped[GeneroEnum] = mapped_column(nullable=False)
    crm = mapped_column(VARCHAR(100), nullable=False)
    especialidade: Mapped[EspecialidadeEnum] = mapped_column(nullable=False)
    created_at = mapped_column(
        DATETIME, default=datetime.now, server_default=func.now()
    )
    updated_at = mapped_column(
        DATETIME, default=datetime.now, server_default=func.now()
    )
    deleted_at = mapped_column(DATETIME, default=None, server_default=None)

    consultas: Mapped["Consultas"] = relationship(back_populates="medico")


class Consultas(BaseModel):
    __tablename__ = "consultas"

    id = Column(
        Integer, Sequence("consultas_id_seq"), primary_key=True, autoincrement=True
    )
    paciente_id: Mapped[int] = mapped_column(
        ForeignKey("pacientes.id"), primary_key=True
    )
    profissional_id: Mapped[int] = mapped_column(ForeignKey("profissionais_saude.id"))
    data = mapped_column(DATETIME, default=datetime.now, server_default=func.now())
    tipo_consulta: Mapped[TipoConsultaEnum] = mapped_column(nullable=True)
    created_at = mapped_column(
        DATETIME, default=datetime.now, server_default=func.now()
    )
    deleted_at = mapped_column(DATETIME, default=None, server_default=None)

    medico: Mapped["Medicos"] = relationship(back_populates="consultas")
    paciente: Mapped["Pacientes"] = relationship(back_populates="consultas")
    diagnosticos: Mapped["Diagnosticos"] = relationship(back_populates="consulta")
    prescricoes: Mapped["Prescricoes"] = relationship(back_populates="consulta")

    __table_args__ = (UniqueConstraint("id"),)


class Prontuarios(BaseModel):
    __tablename__ = "prontuarios"

    id = Column(
        Integer, Sequence("prontuarios_id_seq"), primary_key=True, autoincrement=True
    )
    paciente_id: Mapped[int] = mapped_column(ForeignKey("pacientes.id"))
    observacoes = mapped_column(VARCHAR(250), nullable=True, default=None)
    created_at = mapped_column(
        DATETIME, default=datetime.now, server_default=func.now()
    )
    updated_at = mapped_column(
        DATETIME, default=datetime.now, server_default=func.now()
    )
    deleted_at = mapped_column(DATETIME, default=None, server_default=None)

    paciente: Mapped["Pacientes"] = relationship(back_populates="prontuario")


class Diagnosticos(BaseModel):
    __tablename__ = "diagnosticos"

    id = Column(
        Integer, Sequence("diagnosticos_id_seq"), primary_key=True, autoincrement=True
    )
    consulta_id: Mapped[int] = mapped_column(ForeignKey("consultas.id"))
    conteudo = mapped_column(VARCHAR(500), nullable=True, default=None)
    created_at = mapped_column(
        DATETIME, default=datetime.now, server_default=func.now()
    )
    updated_at = mapped_column(
        DATETIME, default=datetime.now, server_default=func.now()
    )
    deleted_at = mapped_column(DATETIME, default=None, server_default=None)

    consulta: Mapped["Consultas"] = relationship(back_populates="diagnosticos")


class Prescricoes(BaseModel):
    __tablename__ = "prescricoes"

    id = Column(
        Integer, Sequence("prescricoes_id_seq"), primary_key=True, autoincrement=True
    )
    consulta_id: Mapped[int] = mapped_column(ForeignKey("consultas.id"))
    conteudo = mapped_column(VARCHAR(500), nullable=True, default=None)
    created_at = mapped_column(
        DATETIME, default=datetime.now, server_default=func.now()
    )
    deleted_at = mapped_column(DATETIME, default=None, server_default=None)

    consulta: Mapped["Consultas"] = relationship(back_populates="prescricoes")


class Medicamentos(BaseModel):
    __tablename__ = "medicamentos"

    id = Column(
        Integer, Sequence("medicamentos_id_seq"), primary_key=True, autoincrement=True
    )
    nome = mapped_column(VARCHAR(100), nullable=False)
    laboratorio = mapped_column(VARCHAR(100), nullable=False)
    validade = mapped_column(DATETIME, nullable=False)
    quantidade = mapped_column(Integer, nullable=False)
    created_at = mapped_column(
        DATETIME, default=datetime.now, server_default=func.now()
    )
    updated_at = mapped_column(
        DATETIME, default=datetime.now, server_default=func.now()
    )
    deleted_at = mapped_column(DATETIME, default=None, server_default=None)


class RecursosHospitalares(BaseModel):
    __tablename__ = "recursos_hospitalares"

    id = Column(
        Integer,
        Sequence("recursos_hospitalares_id_seq"),
        primary_key=True,
        autoincrement=True,
    )
    nome = mapped_column(VARCHAR(100), nullable=False)
    marca = mapped_column(VARCHAR(100), nullable=False)
    status: Mapped[StatusEnum] = mapped_column(nullable=False)
    created_at = mapped_column(
        DATETIME, default=datetime.now, server_default=func.now()
    )
    updated_at = mapped_column(
        DATETIME, default=datetime.now, server_default=func.now()
    )
    deleted_at = mapped_column(DATETIME, default=None, server_default=None)


def create_database(sgb: str = "mysql"):
    if sgb == "mysql":
        local_engine = engine
    elif sgb == "duckdb":
        local_engine = duck_db_engine
    for table in BaseModel.metadata.tables.values():
        print(str(CreateTable(table).compile(local_engine)))
    BaseModel.metadata.create_all(local_engine)


if __name__ == "__main__":
    sgbd = ""
    while sgbd not in ["mysql", "duckdb"]:
        sgbd = input("Digite o SGBD para criar o banco e as tabelas(mysql ou duckdb): ")
    create_database(sgbd)
