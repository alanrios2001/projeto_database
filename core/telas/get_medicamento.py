from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models.db import (
    LocalAsyncSession, Pacientes, Medicos, Consultas, TransacoesFinanceiras, Prontuarios,
    Diagnosticos, Prescricoes, Medicamentos, RecursosHospitalares,
    TipoConsultaEnum, EspecialidadeEnum, GeneroEnum, StatusEnum, TipoTransacaoEnum
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

    result = await session.scalars(query)

    if result:
        print('Medicamentos encontrados:')
    else:
        print('Nenhum medicamento encontrado.')
        return None
    for row in result:
        print('-----------------------------------')
        print('Nome:', row.nome)
        print('Laboratório:', row.laboratorio)
        print('Quantidade:', row.quantidade)
        print('Validade:', row.validade)

    return result.all()


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


    asyncio.run(main())
