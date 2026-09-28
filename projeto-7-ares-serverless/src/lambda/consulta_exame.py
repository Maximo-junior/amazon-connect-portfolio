import json
import logging

import boto3
from botocore.exceptions import ClientError


logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("AR_TB_Pacientes")


def lambda_handler(event, context):
    try:
        paciente_id = (
            event.get("Details", {})
            .get("Parameters", {})
            .get("PacienteId")
        )

        if not paciente_id:
            logger.warning("PacienteId não informado.")
            return {
                "status": "INVALID_INPUT"
            }

        paciente_id = str(paciente_id).strip()

        if not paciente_id:
            logger.warning("PacienteId vazio.")
            return {
                "status": "INVALID_INPUT"
            }

        response = table.get_item(
            Key={
                "PacienteId": paciente_id
            }
        )

        item = response.get("Item")

        if not item:
            logger.info("Paciente não encontrado.")
            return {
                "status": "NOT_FOUND",
                "paciente_id": paciente_id
            }

        logger.info("Consulta realizada com sucesso.")

        return {
            "status": "FOUND",
            "paciente_id": str(item.get("PacienteId", "")),
            "nome_paciente": str(item.get("nome_paciente", "")),
            "tipo_exame": str(item.get("tipo_exame", "")),
            "data_exame": str(item.get("data_exame", "")),
            "status_laudo": str(item.get("status_laudo", ""))
        }

    except ClientError as error:
        error_code = error.response.get("Error", {}).get("Code", "Unknown")
        logger.error("Erro do DynamoDB: %s", error_code)

        return {
            "status": "ERROR"
        }

    except Exception:
        logger.exception("Erro inesperado durante a consulta.")

        return {
            "status": "ERROR"
        }
