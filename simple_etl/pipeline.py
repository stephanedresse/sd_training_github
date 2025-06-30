from openhexa.sdk import pipeline, current_run

@pipeline(
    "Calculatrice Pipeline",
    inputs={
        "input_1": {"type": "number", "min": 1, "max": 10, "required": True},
        "input_2": {"type": "number", "min": 1, "max": 10, "required": True},
        "operation": {"type": "choice", "choices": ["addition", "soustraction", "multiplication"], "required": True},
    },
)
def calculatrice_pipeline(input_1: int, input_2: int, operation: str):
    result = calcul(input_1, input_2, operation)
    afficher_resultat(result)

@calculatrice_pipeline.task
def calcul(a: int, b: int, op: str) -> float:
    if op == "addition":
        res = a + b
    elif op == "soustraction":
        res = a - b
    elif op == "multiplication":
        res = a * b
    else:
        raise ValueError(f"Opération inconnue : {op}")
    current_run.log_info(f"Résultat de {op} entre {a} et {b} = {res}")
    return res

@calculatrice_pipeline.task
def afficher_resultat(result: float):
    current_run.log_info(f"Le résultat final est : {result}")

if __name__ == "__main__":
    calculatrice_pipeline()