import boto3

dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
table = dynamodb.Table("AR_TB_Pacientes")


def lambda_handler(event, context):
    params = event.get("Details", {}).get("Parameters", event)
    paciente_id = str(params.get("paciente_id", "")).strip()

    if not paciente_id:
        return {
            "encontrado": "false",
            "mensagem": "ID do paciente nao informado."
        }

    resp = table.get_item(Key={"paciente_id": paciente_id})
    item = resp.get("Item")

    if not item:
        return {
            "encontrado": "false",
            "paciente_id": paciente_id,
            "mensagem": "Paciente nao localizado na base."
        }

    return {
        "encontrado": "true",
        "paciente_id": item["paciente_id"],
        "nome_paciente": item["nome"],
        "convenio": item["convenio"],
        "ultimo_exame": item["ultimo_exame"],
        "pendencia_financeira": item["pendencia_financeira"]
    }