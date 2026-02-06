# =========================
# pipeline.py final
# =========================
import os
import papermill as pm
from openhexa.sdk import pipeline, parameter, workspace, current_run

# =========================
# Pipeline OpenHEXA
# =========================
@pipeline("ou_by_district_multi")
@parameter("districts", name="Districts", type=str, required=True)
def run_pipeline(districts):
    """
    Exécute le notebook sierra_leone.ipynb pour une ou plusieurs districts.
    Chaque district génère un CSV de sortie.
    """

    notebook_in = f"{workspace.code_path}/sierra_leone.ipynb"
    notebook_out = f"{workspace.files_path}/sierra_leone_run.ipynb"

    # Lancer le notebook via Papermill avec les paramètres
    pm.execute_notebook(
        notebook_in,
        notebook_out,
        parameters={"districts": districts}
    )

    # Déclarer le notebook exécuté comme output OpenHEXA
    current_run.add_file_output(notebook_out)


# =========================
# Wrapper local pour debug / test
# =========================
def run_pipeline_local(districts):
    """
    Version locale pour tester le pipeline en dehors d'OpenHEXA.
    """

    # Chemin vers le notebook en local
    notebook_in = os.path.join(os.path.dirname(__file__), "sierra_leone.ipynb")
    notebook_out = os.path.join(os.path.dirname(__file__), "../03_output/sierra_leone_run.ipynb")

    # Créer le dossier output s'il n'existe pas
    os.makedirs(os.path.dirname(notebook_out), exist_ok=True)

    # Lancer le notebook via Papermill
    pm.execute_notebook(
        notebook_in,
        notebook_out,
        parameters={"districts": districts}
    )

    print(f"Notebook exécuté, fichier généré : {notebook_out}")

# =========================
# Execution locale
# =========================
if __name__ == "__main__":
    # Liste de districts à tester en local
    districts_test = "Bonthe, Kambia, Bo, Koinadugu, Port Loko, Pujehun, Tonkolili"
    run_pipeline_local(districts_test)