from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from core.models.db import (
    LocalAsyncSession, Medicamentos
)


async def busca_medicamento(
        session: AsyncSession,
        nome: str = None,
        laboratorio: str = None,
        quantidade: int = None,
        validade: str = None
):
    query = select(Medicamentos)

    if nome is not None:
        query = query.where(Medicamentos.nome == nome)
    if laboratorio is not None:
        query = query.where(Medicamentos.laboratorio == laboratorio)
    if quantidade is not None:
        query = query.where(Medicamentos.quantidade == quantidade)
    if validade is not None:
        query = query.where(Medicamentos.validade == validade)
    #print(query)
    result = await session.scalars(query)

    if result:
        print('Medicamentos encontrados:')
    else:
        print('Nenhum medicamento encontrado.')
        return None
    for row in result:
        print('-----------------------------------')
        print('ID:', row.id)
        print('Nome:', row.nome)
        print('Laboratório:', row.laboratorio)
        print('Quantidade:', row.quantidade)
        print('Validade:', row.validade)

    return result.all()


async def retirar_medicamento(session: AsyncSession, medicamento_id: int, quantidade: int):
    stmt = (
        update(Medicamentos).
        where(Medicamentos.id == medicamento_id).
        values(quantidade=Medicamentos.quantidade - quantidade)
    )
    #print(stmt)
    await session.execute(stmt)
    await session.commit()


if __name__ == '__main__':
    import asyncio


    async def main():
        async with LocalAsyncSession() as session:
            await busca_medicamento(session,
                                    nome="Amoxicilina",
                                    laboratorio="EMS",
                                    quantidade=None,
                                    validade=None
                                    )
            await retirar_medicamento(session, 2, 1)


    asyncio.run(main())
