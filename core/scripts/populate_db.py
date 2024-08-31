from faker import Faker
from sqlalchemy.ext.asyncio import AsyncSession

from core.models.db import (
    LocalAsyncSession, Pacientes, Medicos, Consultas, TransacoesFinanceiras, Prontuarios,
    Diagnosticos, Prescricoes, Medicamentos, RecursosHospitalares,
    TipoConsultaEnum, EspecialidadeEnum, GeneroEnum, StatusEnum, TipoTransacaoEnum
)
from random import choice, randint
from datetime import datetime

fake = Faker('pt_BR')


async def create_pacientes(session: AsyncSession, num: int = 100):
    pacientes = []
    for _ in range(num):
        paciente = Pacientes(
            nome=fake.name(),
            data_nascimento=datetime.combine(fake.date_of_birth(minimum_age=18, maximum_age=90), datetime.min.time()),
            genero=choice(list(GeneroEnum)),
            endereco=fake.address(),
            telefone=fake.phone_number(),
            email=fake.email(),
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        pacientes.append(paciente)
    session.add_all(pacientes)
    await session.commit()


async def create_medicos(session: AsyncSession, num: int = 100):
    medicos = []
    for _ in range(num):
        medico = Medicos(
            nome=fake.name(),
            crm=fake.bothify(text='CRM-####-UF'),
            especialidade=choice(list(EspecialidadeEnum)),
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        medicos.append(medico)
    session.add_all(medicos)
    await session.commit()


async def create_consultas(session: AsyncSession, num: int = 100):
    consultas = []
    pacientes_ids = session.query(Pacientes.id).all()
    medicos_ids = session.query(Medicos.id).all()

    for _ in range(num):
        consulta = Consultas(
            paciente_id=choice(pacientes_ids)[0],
            profissional_id=choice(medicos_ids)[0],
            data=fake.date_time_between(start_date='-1y', end_date='now'),
            tipo_consulta=choice(list(TipoConsultaEnum)).value,
            created_at=datetime.now(),
        )
        consultas.append(consulta)
    session.add_all(consultas)
    await session.commit()


async def create_transacoes_financeiras(session: AsyncSession, num: int = 100):
    transacoes = []
    pacientes_ids = session.query(Pacientes.id).all()

    for _ in range(num):
        transacao = TransacoesFinanceiras(
            paciente_id=choice(pacientes_ids)[0],
            tipo_transacao=choice(list(TipoTransacaoEnum)),
            valor=str(randint(100, 10000)),  # valor como string
            data=fake.date_time_between(start_date='-2y', end_date='now'),
            created_at=datetime.now(),
        )
        transacoes.append(transacao)
    session.add_all(transacoes)
    await session.commit()


async def create_prontuarios(session: AsyncSession, num: int = 100):
    prontuarios = []
    pacientes_ids = session.query(Pacientes.id).all()

    for _ in range(num):
        prontuario = Prontuarios(
            paciente_id=choice(pacientes_ids)[0],
            observacoes=fake.text(max_nb_chars=200),
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        prontuarios.append(prontuario)
    session.add_all(prontuarios)
    await session.commit()


async def create_diagnosticos(session: AsyncSession, num: int = 100):
    diagnosticos = []
    consultas_ids = session.query(Consultas.id).all()

    for _ in range(num):
        diagnostico = Diagnosticos(
            consulta_id=choice(consultas_ids)[0],
            conteudo=fake.text(max_nb_chars=200),
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        diagnosticos.append(diagnostico)
    session.add_all(diagnosticos)
    await session.commit()


async def create_prescricoes(session: AsyncSession, num: int = 100):
    prescricoes = []
    consultas_ids = session.query(Consultas.id).all()

    for _ in range(num):
        prescricao = Prescricoes(
            consulta_id=choice(consultas_ids)[0],
            conteudo=fake.text(max_nb_chars=200),
            created_at=datetime.now(),
        )
        prescricoes.append(prescricao)
    session.add_all(prescricoes)
    await session.commit()


async def create_medicamentos(session: AsyncSession, num: int = 100):
    medicamentos = []
    for _ in range(num):
        medicamento = Medicamentos(
            nome=fake.word(),
            validade=fake.future_date(end_date='+2y'),
            quantidade=randint(10, 500),
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        medicamentos.append(medicamento)
    session.add_all(medicamentos)
    await session.commit()


async def create_recursos_hospitalares(session: AsyncSession, num: int = 100):
    recursos = []
    for _ in range(num):
        recurso = RecursosHospitalares(
            nome=fake.word(),
            marca=fake.company(),
            status=choice(list(StatusEnum)),
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        recursos.append(recurso)
    session.add_all(recursos)
    await session.commit()


async def populate_all() -> None:
    async with LocalAsyncSession() as session:
        await create_pacientes(session)
        await create_medicos(session)


if __name__ == "__main__":
    import asyncio

    asyncio.run(populate_all())
