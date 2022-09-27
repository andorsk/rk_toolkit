## Getting Started

### Prerequisites

The workspace requires **Docker** to be installed on your machine ([📖 Installation Guide](https://docs.docker.com/install/#supported-platforms)).

### Start single instance

Deploying a single workspace instance is as simple as:

```bash
docker run -p 8080:8080 mltooling/ml-workspace:0.13.2
```

Voilà, that was easy! Now, Docker will pull the latest workspace image to your machine. This may take a few minutes, depending on your internet speed. Once the workspace is started, you can access it via http://localhost:8080.

> _If started on another machine or with a different port, make sure to use the machine's IP/DNS and/or the exposed port._
To deploy a single instance for productive usage, we recommend to apply at least the following options:

```bash
docker run -d \
    -p 8080:8080 \
    --name "ml-workspace" \
    -v "${PWD}:/workspace" \
    --env AUTHENTICATE_VIA_JUPYTER="mytoken" \
    --shm-size 512m \
    --restart always \
    mltooling/ml-workspace:0.13.2
```

This command runs the container in background (`-d`), mounts your current working directory into the `/workspace` folder (`-v`), secures the workspace via a provided token (`--env AUTHENTICATE_VIA_JUPYTER`), provides 512MB of shared memory (`--shm-size`) to prevent unexpected crashes, and keeps the container running even on system restarts (`--restart always`). You can find additional options for docker run [here](https://docs.docker.com/engine/reference/commandline/run/) and workspace configuration options in [the section below](#Configuration).

### Configuration Options

The workspace provides a variety of configuration options that can be used by setting environment variables (via docker run option: `--env`).

<details>
<summary>Configuration options (click to expand...)</summary>

<table>
    <tr>
        <th>Variable</th>
        <th>Description</th>
        <th>Default</th>
    </tr>
    <tr>
        <td>WORKSPACE_BASE_URL</td>
        <td>The base URL under which Jupyter and all other tools will be reachable from.</td>
        <td>/</td>
    </tr>
    <tr>
        <td>WORKSPACE_SSL_ENABLED</td>
        <td>Enable or disable SSL. When set to true, either certificate (cert.crt) must be mounted to <code>/resources/ssl</code> or, if not, the container generates self-signed certificate.</td>
        <td>false</td>
    </tr>
    <tr>
        <td>WORKSPACE_AUTH_USER</td>
        <td>Basic auth user name. To enable basic auth, both the user and password need to be set. We recommend to use the <code>AUTHENTICATE_VIA_JUPYTER</code> for securing the workspace.</td>
        <td></td>
    </tr>
    <tr>
        <td>WORKSPACE_AUTH_PASSWORD</td>
        <td>Basic auth user password. To enable basic auth, both the user and password need to be set. We recommend to use the <code>AUTHENTICATE_VIA_JUPYTER</code> for securing the workspace.</td>
        <td></td>
    </tr>
    <tr>
        <td>WORKSPACE_PORT</td>
        <td>Configures the main container-internal port of the workspace proxy. For most scenarios, this configuration should not be changed, and the port configuration via Docker should be used instead of the workspace should be accessible from a different port.</td>
        <td>8080</td>
    </tr>
    <tr>
        <td>CONFIG_BACKUP_ENABLED</td>
        <td>Automatically backup and restore user configuration to the persisted <code>/workspace</code> folder, such as the .ssh, .jupyter, or .gitconfig from the users home directory.</td>
        <td>true</td>
    </tr>
    <tr>
        <td>SHARED_LINKS_ENABLED</td>
        <td>Enable or disable the capability to share resources via external links. This is used to enable file sharing, access to workspace-internal ports, and easy command-based SSH setup. All shared links are protected via a token. However, there are certain risks since the token cannot be easily invalidated after sharing and does not expire.</td>
        <td>true</td>
    </tr>
    <tr>
        <td>INCLUDE_TUTORIALS</td>
        <td>If <code>true</code>, a selection of tutorial and introduction notebooks are added to the <code>/workspace</code> folder at container startup, but only if the folder is empty.</td>
        <td>true</td>
    </tr>
    <tr>
        <td>MAX_NUM_THREADS</td>
        <td>The number of threads used for computations when using various common libraries (MKL, OPENBLAS, OMP, NUMBA, ...). You can also use <code>auto</code> to let the workspace dynamically determine the number of threads based on available CPU resources. This configuration can be overwritten by the user from within the workspace. Generally, it is good to set it at or below the number of CPUs available to the workspace.</td>
        <td>auto</td>
    </tr>
    <tr>
        <td colspan="3"><b>Jupyter Configuration:</b></td>
    </tr>
    <tr>
        <td>SHUTDOWN_INACTIVE_KERNELS</td>
        <td>Automatically shutdown inactive kernels after a given timeout (to clean up memory or GPU resources). Value can be either a timeout in seconds or set to <code>true</code> with a default value of 48h.</td>
        <td>false</td>
    </tr>
    <tr>
        <td>AUTHENTICATE_VIA_JUPYTER</td>
        <td>If <code>true</code>, all HTTP requests will be authenticated against the Jupyter server, meaning that the authentication method configured with Jupyter will be used for all other tools as well. This can be deactivated with <code>false</code>. Any other value will activate this authentication and are applied as token via NotebookApp.token configuration of Jupyter.</td>
        <td>false</td>
    </tr>
    <tr>
        <td>NOTEBOOK_ARGS</td>
        <td>Add and overwrite Jupyter configuration options via command line args. Refer to <a href="https://jupyter-notebook.readthedocs.io/en/stable/config.html">this overview</a> for all options.</td>
        <td></td>
    </tr>
</table>

</details>

### Persist Data

To persist the data, you need to mount a volume into `/workspace` (via docker run option: `-v`).

<details>
<summary>Details (click to expand...)</summary>

The default work directory within the container is `/workspace`, which is also the root directory of the Jupyter instance. The `/workspace` directory is intended to be used for all the important work artifacts. Data within other directories of the server (e.g., `/root`) might get lost at container restarts.
</details>

### Enable Authentication

We strongly recommend enabling authentication via one of the following two options. For both options, the user will be required to authenticate for accessing any of the pre-installed tools.

> _The authentication only works for all tools accessed through the main workspace port (default: `8080`). This works for all preinstalled tools and the Access Ports feature. If you expose another port of the container, please make sure to secure it with authentication as well!_
<details>
<summary>Details (click to expand...)</summary>

#### Token-based Authentication via Jupyter (recommended)

Activate the token-based authentication based on the authentication implementation of Jupyter via the `AUTHENTICATE_VIA_JUPYTER` variable:

```bash
docker run -p 8080:8080 --env AUTHENTICATE_VIA_JUPYTER="mytoken" mltooling/ml-workspace:0.13.2
```

You can also use `<generated>` to let Jupyter generate a random token that is printed out on the container logs. A value of `true` will not set any token but activate that every request to any tool in the workspace will be checked with the Jupyter instance if the user is authenticated. This is used for tools like JupyterHub, which configures its own way of authentication.

#### Basic Authentication via Nginx

Activate the basic authentication via the `WORKSPACE_AUTH_USER` and `WORKSPACE_AUTH_PASSWORD` variable:

```bash
docker run -p 8080:8080 --env WORKSPACE_AUTH_USER="user" --env WORKSPACE_AUTH_PASSWORD="pwd" mltooling/ml-workspace:0.13.2
```

The basic authentication is configured via the nginx proxy and might be more performant compared to the other option since with `AUTHENTICATE_VIA_JUPYTER` every request to any tool in the workspace will check via the Jupyter instance if the user (based on the request cookies) is authenticated.

</details>

### Enable SSL/HTTPS

We recommend enabling SSL so that the workspace is accessible via HTTPS (encrypted communication). SSL encryption can be activated via the `WORKSPACE_SSL_ENABLED` variable. 

<details>
<summary>Details (click to expand...)</summary>

When set to `true`, either the `cert.crt` and `cert.key` file must be mounted to `/resources/ssl` or, if the certificate files do not exist, the container generates self-signed certificates. For example, if the `/path/with/certificate/files` on the local system contains a valid certificate for the host domain (`cert.crt` and `cert.key` file), it can be used from the workspace as shown below:

```bash
docker run \
    -p 8080:8080 \
    --env WORKSPACE_SSL_ENABLED="true" \
    -v /path/with/certificate/files:/resources/ssl:ro \
    mltooling/ml-workspace:0.13.2
```

If you want to host the workspace on a public domain, we recommend to use [Let's encrypt](https://letsencrypt.org/getting-started/) to get a trusted certificate for your domain.  To use the generated certificate (e.g., via [certbot](https://certbot.eff.org/) tool) for the workspace, the `privkey.pem` corresponds to the `cert.key` file and the `fullchain.pem` to the `cert.crt` file.

> _When you enable SSL support, you must access the workspace over `https://`, not over plain `http://`._
</details>

### Limit Memory & CPU

By default, the workspace container has no resource constraints and can use as much of a given resource as the host’s kernel scheduler allows. Docker provides ways to control how much memory, or CPU a container can use, by setting runtime configuration flags of the docker run command.

> _The workspace requires atleast 2 CPUs and 500MB to run stable and be usable._
<details>
<summary>Details (click to expand...)</summary>

For example, the following command restricts the workspace to only use a maximum of 8 CPUs, 16 GB of memory, and 1 GB of shared memory

```bash
docker run -p 8080:8080 --cpus=8 --memory=16g --shm-size=1G mltooling/ml-workspace:0.13.2
```

> 📖 _For more options and documentation on resource constraints, please refer to the [official docker guide](https://docs.docker.com/config/containers/resource_constraints/)._
</details>

### Enable Proxy

If a proxy is required, you can pass the proxy configuration via the `HTTP_PROXY`, `HTTPS_PROXY`, and `NO_PROXY` environment variables.

### Multi-user setup

The workspace is designed as a single-user development environment. For a multi-user setup, we recommend deploying [🧰 ML Hub](https://github.com/ml-tooling/ml-hub). ML Hub is based on JupyterHub with the task to spawn, manage, and proxy workspace instances for multiple users.

<details>
<summary>Deployment (click to expand...)</summary>

ML Hub makes it easy to set up a multi-user environment on a single server (via Docker) or a cluster (via Kubernetes) and supports a variety of usage scenarios & authentication providers. You can try out ML Hub via:

```bash
docker run -p 8080:8080 -v /var/run/docker.sock:/var/run/docker.sock mltooling/ml-hub:latest
```

For more information and documentation about ML Hub, please take a look at the [Github Site](https://github.com/ml-tooling/ml-hub).

</details>
