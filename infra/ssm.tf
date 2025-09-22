data "aws_ssm_parameter" "omdb" {
    name = "/FilmFinder/omdbAPIkey"
}