from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from core.models.db import (
    LocalAsyncSession, Pacientes, Medicos, Consultas, TransacoesFinanceiras, Prontuarios,
    Diagnosticos, Prescricoes, Medicamentos, RecursosHospitalares,
    TipoConsultaEnum, EspecialidadeEnum, GeneroEnum, StatusEnum, TipoTransacaoEnum
)


async def registrar_paciente(
        session: AsyncSession,
        nome: str,
        data_nascimento: str,
        genero: GeneroEnum,
        endereco: str = None,
        telefone: str = None,
        email: str = None
):
    paciente = Pacientes(
        nome=nome,
        data_nascimento=data_nascimento,
        genero=genero,
        endereco=endereco,
        telefone=telefone,
        email=email
    )

    session.add(paciente)
    await session.commit()

    return paciente


async def consultar_paciente(session: AsyncSession, nome: str):
    query = select(Pacientes).where(Pacientes.nome.like(nome))
    result = (await session.scalars(query)).all()

    # print(query)
    if not result:
        print('Paciente não encontrado.')
        return None
    print('Paciente encontrado:')
    print('-----------------------------------')
    for r in result:
        print('ID:', r.id)
        print('Nome:', r.nome)
        print('Data de Nascimento:', r.data_nascimento)
        print('Gênero:', r.genero)
        print('Endereço:', r.endereco)
        print('Telefone:', r.telefone)
        print('Email:', r.email)
    return result

if __name__ == '__main__':
    import asyncio

    async def main():
        async with LocalAsyncSession() as session:
            await registrar_paciente(
                session,
                nome="João da Silva",
                data_nascimento="1990-01-01",
                genero=GeneroEnum.MASCULINO,
                endereco="Rua das Flores, 123",
                telefone="(11) 99999-9999",
                email="@g.com")

            await consultar_paciente(session, nome="João da Silva")

    asyncio.run(main())
