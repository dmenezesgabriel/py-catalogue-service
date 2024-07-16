postgres_catalogue_credentials = {
  username = {
    value = "catalogue_app"
    type  = "String"
  }
  password = {
    value = "123abc"
    type  = "SecureString"
  }
  host = {
    value = "postgres-catalogue-dev"
    type  = "String"
  }
  dbname = {
    value = "catalogue"
    type  = "String"
  }
  database_url = {
    value = "postgresql://catalogue_app:123abc@postgres-catalogue-test:5432/catalogue"
    type  = "SecureString"
  }
}
