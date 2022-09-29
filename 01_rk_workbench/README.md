# R-K Workbench

R-K Workbench is a pre-built docker image that contains examples and documentation that will help you build your own RK-Models. It is an extension of the [ml-workspace](https://github.com/ml-tooling/ml-workspace) build.

## Getting Started:


### Step 1: Run image

``` sh
docker run -d \
    -p 8080:8080 \
    --name "rk-workspace" \
    -v "${PWD}:/workspace" \
    --env AUTHENTICATE_VIA_JUPYTER="mytoken" \
    --shm-size 512m \
    --restart always \
    and0rsk/rk_workspace:latest
```

### Step 2:  Go to the browser

Open up your browser and go to localhost:8080. Put "mytoken" into authentication.

## What's Included?

1. A full development workspace for all your model building of RK-Toolkits
2. Examples to review so you can build your own RK-Models

## Help me find things!

1. [Documentation](https://github.com/andorsk/rk_toolkit/tree/documentation/01_rk_workbench/Documentation.md)
2. [User Guide](https://docs.docker.com/get-started/overview)
3. [Examples](https://github.com/animikhroy/rk_toolkit_pipeline_diagrams/tree/main/02_notebooks/rk_general_applications)

## Contributions and Licensing

[Creative Commons Licensing](https://creativecommons.org/licenses/by-nc/4.0/)
