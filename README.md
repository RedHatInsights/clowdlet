# clowdlet
Generate Podman Quadlet files from your ClowdApp.

## Developer setup
This project is managed by `uv`. Install all dependencies and run the application with following command:

    $ uv run clowdlet -f ./examples/clowdapp.yaml --env-file=./examples/custom.env -o /tmp

This command reads example `ClowdApp` template (`-f`), renders default and customized (`--env-file`) env variables, and generates Podman Quadlet file structure in the output directory (`-o`).
