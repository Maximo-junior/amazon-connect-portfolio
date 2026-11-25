import json
import os
import boto3
from botocore.config import Config
from botocore.exceptions import ClientError

boto_cfg = Config(connect_timeout=2, read_timeout=5, retries={"max_attempts": 1})
bedrock = boto3.client("bedrock-runtime", region_name="us-east-1", config=boto_cfg)

MODEL_ID = os.environ.get("MODEL_ID", "us.amazon.nova-micro-v1:0")
GUARDRAIL_ID = os.environ.get("GUARDRAIL_ID", "")
GUARDRAIL_VERSION = os.environ.get("GUARDRAIL_VERSION", "3")

FILAS = {
    "AGENDAMENTO": "Ares_Fila_Agendamento",
    "RESULTADOS": "Ares_Fila_Resultados_Exames",
    "FINANCEIRO": "Ares_Fila_Financeiro_Convenios",
    "PRIORITARIO": "Ares_Fila_Atendimento_Prioritario",
}

FILAS_ARN = {
    "AGENDAMENTO": "arn:aws:connect:us-east-1:723799951581:instance/197bf6a0-b3da-4325-adb6-4c9ec90c56e5/queue/372d5f9e-7ac8-4e3c-9961-2a1fc4259f7a",
    "RESULTADOS": "arn:aws:connect:us-east-1:723799951581:instance/197bf6a0-b3da-4325-adb6-4c9ec90c56e5/queue/9d27b9a1-6204-4616-97c3-64de57e556fc",
    "FINANCEIRO": "arn:aws:connect:us-east-1:723799951581:instance/197bf6a0-b3da-4325-adb6-4c9ec90c56e5/queue/b3eb308f-70b9-4e3f-9a8d-e22f1b6be856",
    "PRIORITARIO": "arn:aws:connect:us-east-1:723799951581:instance/197bf6a0-b3da-4325-adb6-4c9ec90c56e5/queue/0fa7847c-0d20-4d31-9d7a-7c612d22a15b",
}

SINAIS_ALERTA_CLINICO = [
    "dor no peito", "falta de ar", "desmaio", "desmaiando",
    "sangramento", "infarto", "avc", "remedio", "remédio",
    "medicamento", "dosagem", "o que eu tenho", "diagnostico", "diagnóstico"
]


def classificar_fallback_local(mensagem: str) -> dict:
    msg = mensagem.lower()
    if any(p in msg for p in ["agendar", "marcar", "consulta", "remarcar", "cancelar", "cardiologista"]):
        return {
            "intencao": "AGENDAMENTO",
            "fila_destino": FILAS["AGENDAMENTO"],
            "fila_arn": FILAS_ARN["AGENDAMENTO"],
            "urgencia": "BAIXA",
            "guardrail_acionado": "false",
            "resumo_ia": f"Pedido de agendamento: {mensagem[:90]}",
            "resposta_bot": "Entendi! Vou encaminhar voce para nossa equipe de agendamento."
        }
    if any(p in msg for p in ["exame", "laudo", "resultado", "hemograma", "ressonancia"]):
        return {
            "intencao": "RESULTADOS",
            "fila_destino": FILAS["RESULTADOS"],
            "fila_arn": FILAS_ARN["RESULTADOS"],
            "urgencia": "BAIXA",
            "guardrail_acionado": "false",
            "resumo_ia": f"Consulta de resultado de exame: {mensagem[:90]}",
            "resposta_bot": "Certo! Vou transferir voce para o setor de resultados de exames."
        }
    if any(p in msg for p in ["boleto", "fatura", "pagamento", "convenio", "convênio", "reembolso"]):
        return {
            "intencao": "FINANCEIRO",
            "fila_destino": FILAS["FINANCEIRO"],
            "fila_arn": FILAS_ARN["FINANCEIRO"],
            "urgencia": "BAIXA",
            "guardrail_acionado": "false",
            "resumo_ia": f"Assunto financeiro: {mensagem[:90]}",
            "resposta_bot": "Vou transferir seu atendimento para o setor financeiro da Ares Saude."
        }
    return {
        "intencao": "PRIORITARIO",
        "fila_destino": FILAS["PRIORITARIO"],
        "fila_arn": FILAS_ARN["PRIORITARIO"],
        "urgencia": "MEDIA",
        "guardrail_acionado": "false",
        "resumo_ia": f"Solicitacao encaminhada para triagem humana: {mensagem[:90]}",
        "resposta_bot": "Vou transferir voce agora para nossa equipe de atendimento."
    }


def lambda_handler(event, context):
    params = event.get("Details", {}).get("Parameters", event)
    mensagem = str(params.get("mensagem", "")).strip()
    nome_paciente = str(params.get("nome_paciente", "Paciente")).strip()

    if not mensagem:
        return {
            "intencao": "PRIORITARIO",
            "fila_destino": FILAS["PRIORITARIO"],
            "fila_arn": FILAS_ARN["PRIORITARIO"],
            "urgencia": "MEDIA",
            "guardrail_acionado": "false",
            "resumo_ia": "Paciente iniciou contato sem texto detalhado.",
            "resposta_bot": "Vou transferir voce para nossa equipe de atendimento."
        }

    msg_lower = mensagem.lower()
    if any(termo in msg_lower for termo in SINAIS_ALERTA_CLINICO):
        return {
            "intencao": "PRIORITARIO",
            "fila_destino": FILAS["PRIORITARIO"],
            "fila_arn": FILAS_ARN["PRIORITARIO"],
            "urgencia": "ALTA",
            "guardrail_acionado": "true",
            "resumo_ia": "Alerta clinico detectado (emergencia ou pedido de diagnostico/medicacao). Encaminhado com prioridade.",
            "resposta_bot": (
                "Por seguranca clinica, nao realizo diagnosticos nem indico medicamentos. "
                "Se for uma emergencia medica, ligue imediatamente para o SAMU 192 ou procure um pronto-socorro. "
                "Estou transferindo voce agora com prioridade para nossa equipe da Ares Saude."
            )
        }

    system_prompt = (
        "Classifique a mensagem do paciente da Ares Saude em: AGENDAMENTO, RESULTADOS, FINANCEIRO ou PRIORITARIO. "
        'Responda SOMENTE JSON: {"intencao":"...","urgencia":"BAIXA|MEDIA|ALTA","resumo_ia":"1 frase","resposta_bot":"1 frase empatica"}.'
    )

    kwargs = {
        "modelId": MODEL_ID,
        "system": [{"text": system_prompt}],
        "messages": [{"role": "user", "content": [{"text": f"Paciente: {nome_paciente}. Pedido: {mensagem}"}]}],
        "inferenceConfig": {"maxTokens": 150, "temperature": 0.1},
    }
    if GUARDRAIL_ID:
        kwargs["guardrailConfig"] = {
            "guardrailIdentifier": GUARDRAIL_ID,
            "guardrailVersion": GUARDRAIL_VERSION,
        }

    try:
        resp = bedrock.converse(**kwargs)
    except Exception as err:
        print(f"Fallback acionado ({type(err).__name__}): {err}")
        return classificar_fallback_local(mensagem)

    if resp.get("stopReason") == "guardrail_intervened":
        texto_bloqueio = resp["output"]["message"]["content"][0]["text"]
        return {
            "intencao": "PRIORITARIO",
            "fila_destino": FILAS["PRIORITARIO"],
            "fila_arn": FILAS_ARN["PRIORITARIO"],
            "urgencia": "ALTA",
            "guardrail_acionado": "true",
            "resumo_ia": "Guardrail Bedrock acionado na resposta. Transferido para equipe humana.",
            "resposta_bot": texto_bloqueio
        }

    raw_text = resp["output"]["message"]["content"][0]["text"].strip()
    raw_text = raw_text.removeprefix("```json").removeprefix("```").removesuffix("```").strip()

    try:
        dados = json.loads(raw_text)
    except json.JSONDecodeError:
        return classificar_fallback_local(mensagem)

    intencao = dados.get("intencao", "PRIORITARIO").upper()
    if intencao not in FILAS:
        intencao = "PRIORITARIO"

    return {
        "intencao": intencao,
        "fila_destino": FILAS[intencao],
        "fila_arn": FILAS_ARN[intencao],
        "urgencia": dados.get("urgencia", "BAIXA"),
        "guardrail_acionado": "false",
        "resumo_ia": dados.get("resumo_ia", ""),
        "resposta_bot": dados.get("resposta_bot", "")
    }
