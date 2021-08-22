
resource "google_bigquery_dataset" "dataset_1" {
    dataset_id    = "dataset_1"
}
            
resource "google_bigquery_table" "dim_attribute_vdsm" {
dataset_id = google_bigquery_dataset.dataset_1.dataset_id
table_id   = "dim_attribute_vdsm"
schema = file("../dsm-terraform/schemas/dataset_1/tables/table_example_1.json")
}
            