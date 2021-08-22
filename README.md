# terraform-bq-importer
![banner](https://user-images.githubusercontent.com/52164941/130363865-f30bad17-c54c-4fb3-9a61-2854bf189880.png)

## What is it about?
This is a project for implementing terraform to your existing BigQuery. We created a structure to manage our BigQuery with Terraform. If you have already BigQuery before, you need to import your projects, datasets and tables with all of their properties. So we wrote a Python script to import all of our structure in BigQuery according to Terraform structure which we decided. Let's see what we done.

## What to do before?
- Get Terraform. You can check [here](https://learn.hashicorp.com/tutorials/terraform/install-cli).
- You must have GOOGLE_APPLICATION_CREDENTIALS key. You can check [here](https://cloud.google.com/docs/authentication/getting-started) to get it.
- Declare the GOOGLE_APPLICATION_CREDENTIALS environment variable: 

  > export GOOGLE_APPLICATION_CREDENTIALS=path-to-your-key-json-file.json
 
- Firstly, look the terraform section.
    ```
    terraform-bq-projects
    └───gcp-project
        └───   providers.tf
    ```
    
    **gcp-project** is our project in BigQuery. <em>**Providers.tf**</em> is our bridge tf file between Terraform and BigQuery. 
    The following section in <em>**Providers.tf**</em> means see our folder (./datasets) that we will crate with <em>**importer.py**</em>

    ```
      module "datasets" {
        source = "./datasets"
      }
    ```

## How does it work?

After installation of terraform and create the folders needed, we can move on the importer section.
  ```
    terraform-bq-projects
    └───gcp-project
        └───   providers.tf
    └───importer
        └───   environment.yaml
        └───   importer.py
  ```

Create our conda environment : 
   ```
   conda create env -f=environment.yaml
   conda activate importer-env 
   ```
Now it will be enough to just run the script with your google project parameter : 
   ```
   python importer.py -p <your-project-name>
 ```

After run the script, we got all your project from BigQuery and created a structure to work with Terraform. Let's see our structure.
  
```
── gcp-project
│   ├── datasets
│   │   ├── dataset_1.tf
│   │   ├── dataset_2.tf
│   │   └── dataset_3.tf
│   ├── providers.tf
│   └── schemas
│       ├── dataset_1
│       │   ├── tables
│       │   │   └── table_example_1.json
│       │   └── views
│       ├── dataset_2
│       │   ├── tables
│       │   │   └── table_example_2.json
│       │   └── views
│       └── dataset_3
│           ├── tables
│           └── views
│               └── view_example_1.sql
└── importer
    ├── environment.yaml
    └── importer.py
```

## Explain structure

- **./datasets** folder is main side our project. There is a terraform file for each dataset. They contains tables and views in dataset with all of their properties. We give paths for tables schemas and views sql scripts. We have 3 datasets there and their names are: 
  - dataset_1
  - dataset_2
  - dataset_3 

- **./schemas** folder contains json files for tables and sql scripts for views. We got a folder for each dataset. There are folders named tables and views under the each dataset folder and we keep our json files there.

That's all. We import all of structure in your BigQuery. Let's run 
> terraform plan

Please give your feedback ❤️ 

Happy Coding!
