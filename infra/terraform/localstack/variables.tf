# variables.tf
variable "postgres_catalogue_credentials" {
  description = "A map of database credentials"
  type = map(object({
    value = string
    type  = string
  }))
  default = {
    username = {
      value = "your_db_username"
      type  = "String"
    }
    password = {
      value = "your_db_password"
      type  = "SecureString"
    }
    host = {
      value = "your_db_host"
      type  = "String"
    }
    dbname = {
      value = "your_db_name"
      type  = "String"
    }
    database_url = {
      value = "your_database_url"
      type  = "SecureString"
    }
  }
}
