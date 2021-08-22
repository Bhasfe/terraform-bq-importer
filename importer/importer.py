from google.cloud import bigquery
import subprocess
import argparse
import logging
import os
import sys
import pprint
import json
import io

def writeJsonSchema(project: str, dataset: str, folder_name: str, file_name: str, content: str) -> None:
    """Creates a json file contains the given BigQuery table schema"""

    with open(f'../{project}/schemas/{dataset}/{folder_name}/{file_name}.json', 'w', encoding='utf-8') as f:
        f.write(content)

def writeDatasetTf(project: str = None, dataset: str = None, table_name: str = None, content: str = None, type: str = None) -> None:
    """Creates a terraform file contains dataset, tables information"""

    if type == "dataset":
        with open(f'../{project}/datasets/{dataset}.tf', 'w', encoding='utf-8') as f:
            content = """
resource "google_bigquery_dataset" "%s" {
    dataset_id    = "%s"
}
            """%(dataset,dataset)

            f.write(content)

    if type == "table":
        with open(f'../{project}/datasets/{dataset}.tf', 'a', encoding='utf-8') as f:
            schema_path = f'../{project}/schemas/{dataset}/tables/{table_name}.json'

            content = """
resource "google_bigquery_table" "%s" {
dataset_id = google_bigquery_dataset.%s.dataset_id
table_id   = "%s"
schema = file("%s")
}
            """%(table_name, dataset, table_name, schema_path)

            f.write(content)

    elif type == "view":
        with open(f'../{project}/datasets/{dataset}.tf', 'a', encoding='utf-8') as f:
            schema_path = f'./schemas/{dataset}/views/{table_name}.sql'

            content = """
                resource "google_bigquery_table" "%s" {
                dataset_id = google_bigquery_dataset.%s.dataset_id
                table_id   = "%s"
                
                view {
                    query          = file("%s")
                    use_legacy_sql = false
                    }
                }
            """%(table_name, dataset, table_name, schema_path)

            f.write(content)
        
def generateTerraformImportCommand(type: str = None, dataset: str = None, table: str = None) -> str:
    """Generates terraform import expression"""
    
    if type == 'dataset':
        command = """terraform import module.datasets.google_bigquery_dataset.%s %s"""%(dataset,dataset)
    elif type == 'table':
        command = """terraform import module.datasets.google_bigquery_table.%s %s"""%(table, f'/{dataset}/{table}')

    return command

def runTerraformCommands(commands: list, project: str):
    """Runs the given terraform commands"""

    # Go to the project directory
    os.chdir(f'../{project}')
    
    for command in commands:
        process = subprocess.run(command.split())



if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

    # Get Arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--project', default=None, help='Project Name (default = None)')
    args = parser.parse_args()

    # Define Variables 
    project = args.project
    tf_commands = ['terraform init']

    logging.info(f"Parameters: {args}")
    
    # Path configurations
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)
    print(dname)

    # Create Project folder if not exist
    if not os.path.exists(f'../{project}'):
        os.mkdir(f'../{project}')
    if not os.path.exists(f'../{project}/schemas'):
        os.mkdir(f'../{project}/schemas')
    if not os.path.exists(f'../{project}/datasets'):
        os.mkdir(f'../{project}/datasets')

    # Construct a BigQuery client object.
    client = bigquery.Client()

    logging.info("Importing has been started...")

    # Get Datasets and tables
    client.project = project
    datasets = list(client.list_datasets())
    logging.info(f"There are {len(datasets)} datasets in the project {project}")

    if datasets:

        logging.info("Datasets in project {}:".format(project))
        for dataset in datasets:
            # Create Tf file
            writeDatasetTf(project, dataset= dataset.dataset_id, type = 'dataset')

            # Get terraform import command
            tf_commands.append(generateTerraformImportCommand(type="dataset", dataset=dataset.dataset_id))

            # Check schema folders if not exists create
            isDatasetFolderExists = os.path.exists(f'../{project}/schemas/{dataset.dataset_id}')
            if not isDatasetFolderExists:
                os.mkdir(f'../{project}/schemas/{dataset.dataset_id}')
                os.mkdir(f'../{project}/schemas/{dataset.dataset_id}/views')
                os.mkdir(f'../{project}/schemas/{dataset.dataset_id}/tables')

            logging.info("{}".format(dataset.dataset_id))

            # Get tables, and views in the given dataset
            tables = client.list_tables(dataset)
            for table in tables:
                logging.info("\t{}".format(table.table_id))

                if table.table_type == "VIEW":
                    writeJsonSchema(project, dataset.dataset_id, 'views', table.table_id, client.get_table(table).view_query)
                    writeDatasetTf(project=project, dataset=dataset.dataset_id, type="view", table_name=table.table_id)
                if table.table_type == "TABLE":
                    f = io.StringIO("")
                    schema = client.schema_to_json(client.get_table(table).schema, f)
                    writeJsonSchema(project, dataset.dataset_id, 'tables', table.table_id, f.getvalue())
                    writeDatasetTf(project=project, dataset=dataset.dataset_id, type="table", table_name=table.table_id)

                # Get terraform import command
                tf_commands.append(generateTerraformImportCommand(type="table", dataset=dataset.dataset_id, table=table.table_id))
                    
    else:
        logging.info("{} project does not contain any datasets.".format(project))
    
    logging.info(tf_commands)
    runTerraformCommands(tf_commands, project)
