job "debezium-potgresql-redis" {

  group "producer" {
    task "dbz-prod" {
 
  }

  group "source" {
    task "dbz-pgsql" {
 
  }

  group "debezium" {
    task "dbz-server" {
 
  }

  group "sink" {
    task "dbz-redis" {
 
  }

  group "consumer" {
    task "dbz-cons" {
 
  }

}
