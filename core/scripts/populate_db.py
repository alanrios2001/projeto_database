from faker import Faker
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models.db import (
    LocalAsyncSession, Pacientes, Medicos, Consultas, TransacoesFinanceiras, Prontuarios,
    Diagnosticos, Prescricoes, Medicamentos, RecursosHospitalares,
    TipoConsultaEnum, EspecialidadeEnum, GeneroEnum, StatusEnum, TipoTransacaoEnum
)
from random import choice, randint
from datetime import datetime

EQUIPAMENTOS_RECURSOS = [
        ("Ventilador Mecânico", "Dräger"),
        ("Ventilador Mecânico", "GE Healthcare"),
        ("Monitor Cardíaco", "Philips"),
        ("Monitor Cardíaco", "Mindray"),
        ("Desfibrilador", "Zoll"),
        ("Desfibrilador", "Philips"),
        ("Bomba de Infusão", "B.Braun"),
        ("Bomba de Infusão", "Fresenius"),
        ("Oxímetro de Pulso", "Nonin Medical"),
        ("Oxímetro de Pulso", "GE Healthcare"),
        ("Aspirador Cirúrgico", "Medela"),
        ("Aspirador Cirúrgico", "Stryker"),
        ("Eletrocardiógrafo", "GE Healthcare"),
        ("Eletrocardiógrafo", "Philips"),
        ("Ultrassom", "Samsung Medison"),
        ("Ultrassom", "GE Healthcare"),
        ("Tomógrafo", "Siemens"),
        ("Tomógrafo", "GE Healthcare"),
        ("Máquina de Hemodiálise", "Fresenius"),
        ("Máquina de Hemodiálise", "Nipro"),
        ("Incubadora Neonatal", "Dräger"),
        ("Incubadora Neonatal", "GE Healthcare"),
        ("Autoclave", "Phoenix Luferco"),
        ("Autoclave", "Cristofoli"),
        ("Estetoscópio", "Littmann"),
        ("Estetoscópio", "Welch Allyn"),
        ("Termômetro Digital", "Omron"),
        ("Termômetro Digital", "Braun"),
        ("Cadeira de Rodas", "Ortobras"),
        ("Cadeira de Rodas", "Freedom"),
        ("Mesa Cirúrgica", "Maquet"),
        ("Mesa Cirúrgica", "Stryker"),
        ("Laringoscópio", "Welch Allyn"),
        ("Laringoscópio", "HEINE"),
        ("Esfigmomanômetro", "Welch Allyn"),
        ("Esfigmomanômetro", "Riester"),
        ("Lanterna Clínica", "HEINE"),
        ("Lanterna Clínica", "Welch Allyn"),
        ("Balança Antropométrica", "Filizola"),
        ("Balança Antropométrica", "Welmy"),
        ("Carrinho de Parada", "FAMI"),
        ("Carrinho de Parada", "Olidef"),
        ("Bisturi Elétrico", "Valleylab"),
        ("Bisturi Elétrico", "Medtronic"),
        ("Microscópio Cirúrgico", "Zeiss"),
        ("Microscópio Cirúrgico", "Leica Microsystems"),
        ("Colchão Pneumático", "Airbed"),
        ("Colchão Pneumático", "ComfortPlus"),
        ("Monitor Multiparâmetros", "Philips"),
        ("Monitor Multiparâmetros", "Mindray"),
        ("Carro de Emergência", "FAMI"),
        ("Carro de Emergência", "Olidef"),
        ("Ventilador Portátil", "Weinmann"),
        ("Ventilador Portátil", "Philips"),
        ("Bombas de Seringa", "B.Braun"),
        ("Bombas de Seringa", "Fresenius"),
        ("Mesa Ginecológica", "Biodex"),
        ("Mesa Ginecológica", "Carci"),
        ("Compressor de Ar", "Schulz"),
        ("Compressor de Ar", "Medic Air"),
        ("Iluminador Cirúrgico", "Dräger"),
        ("Iluminador Cirúrgico", "Philips")
    ]

MEDICAMENTOS_LABORATORIOS = [
        ("Paracetamol", "EMS"),
        ("Ibuprofeno", "Bayer"),
        ("Amoxicilina", "GlaxoSmithKline"),
        ("Omeprazol", "Aché"),
        ("Simvastatina", "Medley"),
        ("Atenolol", "AstraZeneca"),
        ("Diclofenaco", "Novartis"),
        ("Prednisona", "EMS"),
        ("Metformina", "Merck"),
        ("Losartana", "Torrent"),
        ("Enalapril", "Pfizer"),
        ("Clopidogrel", "Sanofi"),
        ("Aspirina", "Bayer"),
        ("Levotiroxina", "Sanofi"),
        ("Metoprolol", "Novartis"),
        ("Lorazepam", "Teva"),
        ("Cetirizina", "Pfizer"),
        ("Cetoprofeno", "Bayer"),
        ("Diazepam", "Roche"),
        ("Fluconazol", "Pfizer"),
        ("Amoxicilina", "EMS"),
        ("Simvastatina", "EMS"),
        ("Paracetamol", "Medley"),
        ("Omeprazol", "Bayer"),
        ("Metformina", "EMS"),
        ("Atenolol", "Medley"),
        ("Diclofenaco", "EMS"),
        ("Prednisona", "Sanofi"),
        ("Levotiroxina", "Merck"),
        ("Fluconazol", "Teva")
    ]


fake = Faker('pt_BR')


def get_nome(genero: GeneroEnum) -> str:
    if genero == GeneroEnum.MASCULINO:
        return fake.first_name_male() + ' ' + fake.last_name()
    else:
        return fake.first_name_female() + ' ' + fake.last_name()


def generate_diagnostico_text():
    sintomas = [
        "dor abdominal", "febre alta", "tosse persistente",
        "cansaço extremo", "inchaço nas pernas", "dor de cabeça intensa",
        "perda de apetite", "dor no peito", "tontura", "náuseas",
        "dificuldade para respirar", "coceira na pele", "manchas avermelhadas"
    ]

    conclusao = [
        "Suspeita de infecção viral. Recomendado repouso e ingestão de líquidos.",
        "Possível infecção bacteriana. Iniciado tratamento com antibiótico.",
        "Sintomas indicam possível quadro de hipertensão. Sugerida consulta com cardiologista.",
        "Alergia a substância não identificada. Indicado uso de anti-histamínico.",
        "Quadro compatível com sinusite. Prescrito tratamento com descongestionante nasal.",
        "Paciente apresenta sinais de bronquite. Iniciado tratamento com broncodilatador."
    ]

    diagnostico = (
        f"Paciente relata {choice(sintomas)} há {fake.random_int(min=1, max=10)} dias. "
        f"Exame físico revela {fake.word()} e {fake.word()}. "
        f"{choice(conclusao)}"
    )

    return diagnostico


def generate_prescricao_text():
    medicamentos = [
        "Paracetamol 500mg", "Amoxicilina 875mg", "Ibuprofeno 400mg",
        "Omeprazol 20mg", "Captopril 25mg", "Lorazepam 2mg",
        "Metformina 850mg", "Atenolol 50mg", "Diclofenaco 50mg",
        "Prednisona 20mg", "Simvastatina 40mg"
    ]

    instrucoes = [
        "Tomar 1 comprimido a cada 8 horas por 7 dias.",
        "Tomar 1 comprimido antes das refeições por 10 dias.",
        "Aplicar o creme 2 vezes ao dia por 14 dias.",
        "Ingerir 1 cápsula ao acordar e outra ao deitar, por 30 dias.",
        "Ingerir 1 comprimido ao dia, antes de dormir.",
        "Tomar 1 comprimido após as refeições, por 15 dias.",
        "Aplicar na área afetada 3 vezes ao dia.",
        "Administrar 2 gotas a cada 4 horas, conforme necessário.",
        "Usar 1 injeção subcutânea diariamente, por 7 dias."
    ]

    prescricao = (
        f"{choice(medicamentos)} - {choice(instrucoes)} "
        f"Em caso de reação adversa, {fake.catch_phrase().lower()}."
    )

    return prescricao


def generate_prontuario_observacao():
    estados = [
        "Paciente apresenta sinais de melhora significativa.",
        "Estado clínico estável, sem alterações nas últimas 24 horas.",
        "Paciente relata dores ocasionais na região abdominal.",
        "Sinais vitais dentro dos parâmetros normais.",
        "Paciente continua em observação para monitoramento da febre.",
        "Melhora gradual observada nas últimas 48 horas.",
        "Paciente apresenta leve dificuldade respiratória.",
        "Condição clínica deteriorada nas últimas 12 horas.",
        "Paciente relata aumento de apetite e disposição.",
        "Mantida a prescrição inicial. Monitoramento contínuo necessário."
    ]

    recomendacoes = [
        "Recomendada continuidade do tratamento atual.",
        "Sugerido ajuste na medicação para controle da dor.",
        "Solicitado exame de sangue para monitorar níveis inflamatórios.",
        "Recomendado repouso e hidratação abundante.",
        "Encaminhado para consulta com especialista.",
        "Acompanhamento diário até estabilização do quadro.",
        "Agendada revisão em uma semana.",
        "Revisão de medicação agendada para amanhã.",
        "Paciente orientado sobre sinais de alerta e retorno imediato se necessário.",
        "Sugerida alta hospitalar caso mantenha evolução positiva."
    ]

    observacao = (
        f"{choice(estados)} {choice(recomendacoes)} "
        f"Paciente segue orientações médicas conforme protocolo."
    )

    return observacao


async def create_pacientes(session: AsyncSession, num: int):
    pacientes = []
    for _ in range(num):
        genero = choice(list(GeneroEnum))
        paciente = Pacientes(
            nome=get_nome(genero),
            data_nascimento=fake.date_of_birth(minimum_age=18, maximum_age=90).strftime('%Y-%m-%d %H:%M:%S'),
            genero=genero,
            endereco=fake.address(),
            telefone=fake.phone_number(),
            email=fake.email(),
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        pacientes.append(paciente)
    session.add_all(pacientes)
    await session.commit()


async def create_medicos(session: AsyncSession, num: int):
    medicos = []
    for _ in range(num):
        genero = choice(list(GeneroEnum))
        medico = Medicos(
            nome=get_nome(genero),
            genero=choice(list(GeneroEnum)),
            crm=fake.bothify(text='CRM-####-UF'),
            especialidade=choice(list(EspecialidadeEnum)),
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        medicos.append(medico)
    session.add_all(medicos)
    await session.commit()


async def create_consultas(session: AsyncSession, num: int):
    consultas = []
    pacientes_ids = (await session.scalars(select(Pacientes.id))).all()
    medicos_ids = (await session.scalars(select(Medicos.id))).all()

    for _ in range(num):
        consulta = Consultas(
            paciente_id=choice(pacientes_ids),
            profissional_id=choice(medicos_ids),
            data=fake.date_time_between(start_date='-1y', end_date='now'),
            tipo_consulta=choice(list(TipoConsultaEnum)).value,
            created_at=datetime.now(),
        )
        consultas.append(consulta)
    session.add_all(consultas)
    await session.commit()


async def create_transacoes_financeiras(session: AsyncSession, num: int):
    transacoes = []
    pacientes_ids = (await session.scalars(select(Pacientes.id))).all()

    for _ in range(num):
        transacao = TransacoesFinanceiras(
            paciente_id=choice(pacientes_ids),
            tipo_transacao=choice(list(TipoTransacaoEnum)),
            valor=str(randint(100, 10000)),  # valor como string
            data=fake.date_time_between(start_date='-2y', end_date='now'),
            created_at=datetime.now(),
        )
        transacoes.append(transacao)
    session.add_all(transacoes)
    await session.commit()


async def create_prontuarios(session: AsyncSession, num: int):
    prontuarios = []
    pacientes_ids = (await session.scalars(select(Pacientes.id))).all()

    for _ in range(num):
        prontuario = Prontuarios(
            paciente_id=choice(pacientes_ids),
            observacoes=generate_prontuario_observacao(),
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        prontuarios.append(prontuario)
    session.add_all(prontuarios)
    await session.commit()


async def create_diagnosticos(session: AsyncSession, num: int):
    diagnosticos = []
    consultas_ids = (await session.scalars(select(Consultas.id))).all()

    for _ in range(num):
        diagnostico = Diagnosticos(
            consulta_id=choice(consultas_ids),
            conteudo=generate_diagnostico_text(),
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        diagnosticos.append(diagnostico)
    session.add_all(diagnosticos)
    await session.commit()


async def create_prescricoes(session: AsyncSession, num: int):
    prescricoes = []
    consultas_ids = (await session.scalars(select(Consultas.id))).all()

    for _ in range(num):
        prescricao = Prescricoes(
            consulta_id=choice(consultas_ids),
            conteudo=generate_prescricao_text(),
            created_at=datetime.now(),
        )
        prescricoes.append(prescricao)
    session.add_all(prescricoes)
    await session.commit()


async def create_medicamentos(session: AsyncSession, num: int):
    medicamentos = []
    for _ in range(num):
        nome, laboratorio = choice(MEDICAMENTOS_LABORATORIOS)
        medicamento = Medicamentos(
            nome=nome,
            laboratorio=laboratorio,
            validade=fake.future_date(end_date='+2y'),
            quantidade=randint(10, 500),
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        medicamentos.append(medicamento)
    session.add_all(medicamentos)
    await session.commit()


async def create_recursos_hospitalares(session: AsyncSession, num: int):
    recursos = []
    for _ in range(num):
        nome, marca = choice(EQUIPAMENTOS_RECURSOS)
        recurso = RecursosHospitalares(
            nome=nome,
            marca=marca,
            status=choice(list(StatusEnum)),
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        recursos.append(recurso)
    session.add_all(recursos)
    await session.commit()


async def populate_all(n: int = 100) -> None:
    async with LocalAsyncSession() as session:
        await create_pacientes(session, n)
        await create_medicos(session, n)
        await create_consultas(session, n)
        await create_diagnosticos(session, n)
        await create_prescricoes(session, n)
        await create_prontuarios(session, n)
        await create_transacoes_financeiras(session, n)
        await create_medicamentos(session, n)
        await create_recursos_hospitalares(session, n)


if __name__ == "__main__":
    import asyncio

    asyncio.run(populate_all(100))
