data "aws_ssm_parameter" "omdb" {
  name            = "/film-finder/omdbApiKey"
  with_decryption = true
}
