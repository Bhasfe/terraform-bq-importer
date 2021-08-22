
resource "google_bigquery_dataset" "dataset_2" {
    dataset_id    = "dataset_2"
}
            
resource "google_bigquery_table" "dim_attribute_request" {
dataset_id = google_bigquery_dataset.dataset_2.dataset_id
table_id   = "dim_attribute_request"
schema = file("../gcp-project/schemas/dataset_2/tables/table_example_2.json")
}
            