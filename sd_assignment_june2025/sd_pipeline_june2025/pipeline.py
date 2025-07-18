import os
from datetime import datetime, timezone
from pathlib import Path

from openhexa.sdk import current_run, pipeline, workspace, parameter
import papermill as pm


def get_output_dir(subfolder="outputs_dhis2"):
    """
    Retourne le chemin vers le dossier d'outputs. Si workspace.files_path n'est pas disponible (exécution locale),
    on utilise un dossier local.
    """
    try:
        base_path = workspace.files_path
    except Exception:
        base_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "local_outputs")
    output_dir = os.path.join(base_path, subfolder)
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    print(f"Output directory: {output_dir}")
    current_run.log_info(f"Output directory: {output_dir}")
    
    return output_dir



@pipeline(name="Extraction DHIS2 avec Papermill", timeout=720)
@parameter("user_name", name="User name", type=str, default="Stephane", help="Nom de l'utilisateur")
@parameter("politesse_lvl", name="Niveau de politesse", type=str,
           choices=['rude', 'respectueux', 'frotte manche'], default='respectueux',
           help="Choix du niveau de politesse")
@parameter("data_element_list", name="Data Element List", type=str,
           choices=["DE_list_1", "DE_list_2"], default="DE_list_1",
           help="Choix de la liste des Data Elements")
def with_papermill(user_name, politesse_lvl, data_element_list):
    current_run.log_info("Pipeline started.")
    run_notebook(user_name, politesse_lvl, data_element_list)


@with_papermill.task
def run_notebook(user_name, politesse_lvl, data_element_list):
    # Message personnalisé
    message_de_politesse = {
        "rude": "Pas trop tôt, enfin qqn test cette pipeline!",
        "respectueux": "Merci d'avoir pris le temps de tester cette pipeline.",
        "frotte manche": "C'est vraiment génial que vous testiez cette pipeline, vous êtes vraiment exceptionnel !"
    }.get(politesse_lvl, "Merci.")

    current_run.log_info(f"Les paramètres choisis sont : {user_name}, {politesse_lvl}, {data_element_list}")

    # Chemins
    input_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "notebook_extraction_dhis2.ipynb")
    output_dir = get_output_dir()
    notebook_output_path = os.path.join(output_dir, f"simple_notebook_output_{datetime.now(timezone.utc).isoformat()}.ipynb")
    current_run.log_debug(f"Notebook input: {input_path}")
    current_run.log_debug(f"Notebook output: {notebook_output_path}")

    # Exécution du notebook avec Papermill
    try:
        current_run.log_info("Launching the notebook...")
        pm.execute_notebook(
            input_path=input_path,
            output_path=notebook_output_path,
            parameters={
                "user_name": user_name,
                "data_element_list": data_element_list,
                "politesse_lvl": politesse_lvl,
                "output_dir": output_dir,
            },
            request_save_on_cell_execute=False,
            progress_bar=False
        )
        current_run.log_info("Notebook executed successfully.")
    except Exception as e:
        current_run.log_error(f"Failed to execute notebook: {e}")
        raise

    # Recherche du fichier CSV produit par le notebook
    date_today = datetime.now().strftime("%Y-%m-%d")
    csv_filename = f"agg_df_{date_today}.csv"
    csv_output_path = os.path.join(output_dir, csv_filename)

    current_run.log_debug(f"Looking for CSV output at: {csv_output_path}")
    if os.path.exists(csv_output_path):
        current_run.log_info(f"Adding pipeline output file: {csv_output_path}")
        current_run.add_file_output(csv_output_path)
    else:
        current_run.log_warning(f"CSV output file not found at expected path: {csv_output_path}")

    current_run.log_info("Task done!")
    current_run.log_info("Pipeline finished.")
    current_run.log_info(message_de_politesse)


if __name__ == "__main__":
    with_papermill()


# Commande pour pousser vers OpenHexa

### openhexa pipelines run .
### openhexa pipelines push .