
# TODO: Uncomment the block below to add necessary IAM permissions to
# the service account IAM role.
#
# IMPORTANT: Role and policy changes will NOT be immediately available
# to services created from a feature branch (via the PR automation).
# They have to be merged to `main` or `develop` first.
#
# resource "aws_iam_role_policy" "service_role_policy" {
#   count = length(module.application[0].service_role_name) > 0  && !local.is_automation_workspace ? 1 : 0
#
#   name = "${module.application[0].service_role_name}-policy"
#   role = module.application[0].service_role_name
#
#   policy = jsonencode({
#     Version = "2012-10-17"
#     Statement = [
#       {
#         Sid = "ExampleStatementSid"
#         Action = [
#           "someservice:DoSomething"
#         ]
#         Effect = "Allow"
#         Resource = [
#           "arn:aws:some-resources"
#         ]
#       }
#     ]
#   })
# }
