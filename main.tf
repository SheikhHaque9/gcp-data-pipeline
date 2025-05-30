terraform {
  required_providers {
    google = {
        source = "hashicorp/google"
        version = "6.8.0"
    }
  }
}

provider "google" {
    project = var.project_id
    region  = var.region
    #zone = var.zone
}

resource "google_project_service" "required" {
    for_each = toset([
        "cloudfunctions.googleapis.com",
        "pubsub.googleapis.com",
        "sqladmin.googleapis.com",
        "compute.googleapis.com",
        "cloudscheduler.googleapis.com"
    ])
    service = each.value
}

resource "google_pubsub_topic" "bike_topic" {
    name = "bike_ingestion"
}

resource "google_storage_bucket" "function_bucket" {
    name     = "${var.project_id}-function-bucket"
    location = var.region
    force_destroy = true
}

resource "google_storage_bucket_object" "function_zip" {
    name = "ingest_bike_data.zip"
    bucket = google_storage_bucket.function_bucket.name
    source = "cloud_functions/ingest_bike_data.zip"
}

resource "google_cloudfunctions_function" "ingest_bike_data" {
    name = "ingest-bike-data"
    runtime = "python310"
    entry_point = "main"
    source_archive_bucket = google_storage_bucket.function_bucket.name
    source_archive_object = google_storage_bucket_object.function_zip.name
    #trigger_http = google_pubsub_topic.bike_topic.name
    available_memory_mb = 256

    event_trigger {
      event_type = "providers/cloud.pubsub/eventTypes/topic.publish"
      resource   = google_pubsub_topic.bike_topic.id
  }

    environment_variables = {
        TFL_API_KEY = var.tfl_api_key
    }
}


resource "google_cloud_scheduler_job" "trigger" {
  name     = "trigger-bike"
  schedule = "0 * * * *"
  time_zone = "UTC"

  pubsub_target {
    topic_name = google_pubsub_topic.bike_topic.id
    data       = base64encode("start")
  }
}

resource "google_sql_database_instance" "db" {
  name = "bike-instance"
  region = var.region
  database_version = "POSTGRES_14"

  settings {
    tier = "db-f1-micro"
  }
}

resource "google_sql_database" "bike_db" {
  name     = "bike"
  instance = google_sql_database_instance.db.name
}

resource "google_compute_instance" "streamlit" {
  name         = "streamlit-server"
  machine_type = "e2-micro"
  zone         = var.zone

  boot_disk {
    initialize_params {
      image = "debian-cloud/debian-11"
    }
  }

  metadata_startup_script = file("streamlit_app/startup.sh")

  network_interface {
    network = "default"
    access_config {}
  }

  tags = ["http-server"]
}

resource "google_project_service" "cloudbuild" {
  project = "data-project-mh"
  service = "cloudbuild.googleapis.com"
  disable_on_destroy = false
}

resource "google_project_service" "artifactregistry" {
  project = "data-project-mh"
  service = "artifactregistry.googleapis.com"
  disable_on_destroy = false
}

