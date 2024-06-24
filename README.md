# Elation Shared API Schema

This repo contains a collection of OpenAPI schema that are shared across Elation OpenAPI specs.

Schemas should only be added here when the structure is considered extremely stable and unlikely to change ( Creating a
new Timezone or the US getting a 51st state ). If a schema is likely to change, it should be kept in the repo that uses
it.

# Contributing

## Pull Requests Reviewers
Drop the PR request in `#team_developer_api_guild` on slack

## Structure

Schemas are stored in the `schemas` directory. Each schema should be stored in its own file.

## File Name Convention

```
[name].schema.[json|yaml]
```

