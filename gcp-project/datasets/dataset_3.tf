
resource "google_bigquery_dataset" "dataset_3" {
    dataset_id    = "dataset_3"
}
            
                resource "google_bigquery_table" "dim_attribute_vdsm_authorized_view" {
                dataset_id = google_bigquery_dataset.dataset_3.dataset_id
                table_id   = "dim_attribute_vdsm_authorized_view"
                
                view {
                    query          = file("./schemas/dataset_3/views/view_example_1.json")
                    use_legacy_sql = false
                    }
                }
            