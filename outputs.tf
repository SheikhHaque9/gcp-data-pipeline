output "streamlit_app_ip" {
  value = google_compute_instance.streamlit.network_interface[0].access_config[0].nat_ip
}
