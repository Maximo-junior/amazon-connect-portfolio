def lambda_handler(event, context):
    texto = event.get("inputTranscript", "")
    session_state = event.get("sessionState", {})
    session_attrs = session_state.get("sessionAttributes") or {}
    session_attrs["texto_digitado"] = texto
    intent = session_state.get("intent", {"name": "FallbackIntent"})
    intent["state"] = "Fulfilled"
    return {
        "sessionState": {
            "dialogAction": {"type": "Close"},
            "intent": intent,
            "sessionAttributes": session_attrs
        }
    }
