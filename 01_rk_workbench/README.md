# R-K Workbench

R-K Workbench is a pre-built docker image that contains examples and documentation that will help you build your own RK-Models. It is an extension of the [ml-workspace](https://github.com/ml-tooling/ml-workspace) build.

## Getting Started:

### Step 1: Login to Docker

``` sh
docker login --username=<username_here> cloud.canister.io:5000
```

### Step 2: Run image

``` sh
docker run -d \
    -p 8080:8080 \
    --name "ml-workspace" \
    -v "${PWD}:/workspace" \
    --env AUTHENTICATE_VIA_JUPYTER="mytoken" \
    --shm-size 512m \
    --restart always \
    cloud.canister.io:5000/andorsk/rkworkbench:latest
```

### Step 3:  Go to the browser

Open up your browser and go to localhost:8080. Put "mytoken" into authentication.

## What's Included?

1. A full development workspace for all your model building of RK-Toolkits
2. Examples to review so you can build your own RK-Models

## Help me find things!

1. [Documentation]()
2. [RK Toolkit API]()
3. [User Guide]()
4. [Examples]()

## Contributions and Licensing

