from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models.db import (
    LocalAsyncSession, Pacientes, Medicos, Consultas, TransacoesFinanceiras, Prontuarios,
    Diagnosticos, Prescricoes, Medicamentos, RecursosHospitalares,
    TipoConsultaEnum, EspecialidadeEnum, GeneroEnum, StatusEnum, TipoTransacaoEnum
)


async def query_medicamento(
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

    return result.all()


if __name__ == '__main__':
    import asyncio

    async def main():
        async with LocalAsyncSession() as session:
            result = await query_medicamento(session,
                                             nome="Dipirona",
                                             )
            print(result)

    asyncio.run(main())