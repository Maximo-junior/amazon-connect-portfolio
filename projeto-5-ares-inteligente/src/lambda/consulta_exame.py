"""
Função Serverless: AR_LF_ConsultaExame
Ecossistema Ares Saúde | Projeto 5: Ares Inteligente
Função: Simulação de microsserviço hospitalar para consulta de laudos de exames integrado ao Amazon Connect.
"""

import json
import logging

# Configuração de telemetria básica (equivalente ao CloudWatch Logs)
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Base simulada de exames hospitalares (Mock Database Ares)
MOCK_EXAMES_DB = {
    "ARES-702": {
        "statusExame": "FOUND",
        "pacienteNome": "Carlos Eduardo",
        "tipoExame": "Ressonancia Magnetica",
        "dataLiberacao": "2026-09-20",
        "situacaoLaudo": "Disponivel no portal do paciente"
    },
    "ARES-301": {
        "statusExame": "FOUND",
        "pacienteNome": "Mariana Souza",
        "tipoExame": "Hemograma Completo",
        "dataLiberacao": "2026-09-21",
        "situacaoLaudo": "Disponivel no portal do paciente"
    }
}


def lambda_handler(event, context):
    """
    Handler principal acionado pelo bloco 'Invoke AWS Lambda function' do Amazon Connect.

    Regra de Contrato do Amazon Connect:
    O retorno deve ser SEMPRE um dicionário plano (chave: valor) com strings.
    Valores aninhados (dicionários dentro de dicionários ou arrays) não são suportados
    pelo namespace $.External do Flow Designer.
    """
    logger.info(f"Evento recebido do Amazon Connect: {json.dumps(event)}")

    try:
        # Extração defensiva dos parâmetros passados pelo Amazon Connect
        details = event.get("Details", {})
        parameters = details.get("Parameters", {})
        id_paciente = parameters.get("idPaciente")

        # Validação de parâmetro de entrada
        if not id_paciente:
            logger.warning("Identificador do paciente não fornecido no evento.")
            return {
                "statusCode": "400",
                "statusExame": "ERROR",
                "mensagem": "Identificador de exame ausente"
            }

        # Consulta no banco de dados simulado
        exame = MOCK_EXAMES_DB.get(id_paciente)

        if exame:
            logger.info(f"Exame localizado com sucesso para: {id_paciente}")
            return {
                "statusCode": "200",
                "statusExame": exame["statusExame"],
                "pacienteNome": exame["pacienteNome"],
                "tipoExame": exame["tipoExame"],
                "dataLiberacao": exame["dataLiberacao"],
                "situacaoLaudo": exame["situacaoLaudo"]
            }
        else:
            logger.info(f"Nenhum exame localizado para: {id_paciente}")
            return {
                "statusCode": "404",
                "statusExame": "NOT_FOUND",
                "mensagem": "Nenhum laudo localizado para o identificador informado"
            }

    except Exception as e:
        logger.error(f"Erro inesperado durante a execução da Lambda: {str(e)}")
        return {
            "statusCode": "500",
            "statusExame": "ERROR",
            "mensagem": "Falha interna no microsservico hospitalar"
        }
