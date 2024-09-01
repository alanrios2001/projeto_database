from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from core.models.db import (
    LocalAsyncSession, Consultas, Pacientes, GeneroEnum
)


async def buscar_consulta_paciente(session: AsyncSession, nome: str):
    query = (select(Consultas).
             options(selectinload(Consultas.paciente)).
             where(Pacientes.nome.like(nome))
             )

    print(query)
    result = (await session.scalars(query)).all()

    if not result:
        print('Consulta não encontrada.')
        return None
    print('Consulta encontrada:')
    print('-----------------------------------')
    for r in result:
        print('ID consulta:', r.id)
        print('Data:', r.data)
        print('Paciente:', r.paciente.nome)
        print('Médico:', r.medico.nome)
        print('-----------------------------------')


if __name__ == '__main__':
    import asyncio

    async def main():
        async with LocalAsyncSession() as session:
            await buscar_consulta_paciente(session, 'Maria')

    asyncio.run(main())
