# Deploy a simple http-api in minikube using python and ansible
A simple HTTP-API. Serves on port 5001 when run via Docker. When deployed on minikube, use the service url printed in the console output. *http://127.0.01:minikubePort/path*

## System & Application Versions
```bash
OS Release & Terminal: WSL - Bash on Ubuntu on Windows. Ubuntu 16.04.6 LTS
python: 3.5.2
pip: 8.1.1
docker version on host: 20.10.2
docker version on minikube vm: 20.10.6
minikube version: v1.20.0
kubectl version: v1.18.8
ansible: 2.9.21
```

## Setup python :snake:
[Installing python](https://www.python.org/downloads/release/python-352/) - Follow this official guide on how to setup python based on your distribution. 

## Setup docker 🐳
[Installing docker](https://docs.docker.com/engine/install/) - Follow this official guide on how to setup docker based on your distribution. 

## Setup ansible
[Installing ansible](https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html) - Follow this official guide on how to setup docker based on your distribution. 

## Setup minikube ☸️
[Installing minikube](https://minikube.sigs.k8s.io/docs/start/#binary-download) - Follow this official guide on how to setup minikube cluster using binary.

## Setup kubectl
[Installing kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/) - By default, kubectl gets configured to access the kubernetes cluster control plane inside minikube when the minikube start command is executed. If not configured, then click on the given link to install kubectl.

Once minikube installation is complete, if you encounter any issues as below 
> **Exiting due to DRV_CP_ENDPOINT failed to get API Server URL: failed to parse ip for "localhost"**.  
> Then change localhost to IP in env DOCKER_HOST. For more details please refer the [github-minikube-issue#10306](https://github.com/kubernetes/minikube/issues/10306).

After fixing the issue, run the below command to start a single node minikube cluster.  
> ##### ***Please note that this part is taken care by ansible playbook. But if you'd like to setup manually, then run the command.***
```bash
$ minikube start --profile=minikube
# Output:
😄  minikube v1.20.0 on Ubuntu 16.04
✨  Automatically selected the docker driver
🐳  For improved Docker performance, enable the overlay Linux kernel module using 'modprobe overlay'
👍  Starting control plane node minikube in cluster minikube
🐳  Pulling base image ...
🔥  Creating docker container (CPUs=2, Memory=3888MB) ...
❗  Listening to 0.0.0.0 on external docker host 0.0.0.0. Please be advised
🐳  Preparing Kubernetes v1.20.2 on Docker 20.10.6 ...
    ▪ Generating certificates and keys ...
    ▪ Booting up control plane ...
    ▪ Configuring RBAC rules ...
🔎  Verifying Kubernetes components...
    ▪ Using image gcr.io/k8s-minikube/storage-provisioner:v5
🌟  Enabled addons: storage-provisioner, default-storageclass

❗  /usr/local/bin/kubectl is version 1.18.8, which may have incompatibilites with Kubernetes 1.20.2.
    ▪ Want kubectl v1.20.2? Try 'minikube kubectl -- get pods -A'
🏄  Done! kubectl is now configured to use "minikube" cluster and "default" namespace by default
```
The minikube components shall be seen by running the below commands.  
```bash
$ kubectl get nodes
$ kubectl pods -A
```

Once the installation is done, clone the repo as below.  
```bash
$ git clone https://github.com/vijaysundarv/cf_elink_http_api.git
```

## Deploy sequence :shipit:
> - Creates necessary config directories for playbook to validate.
> - Checks existing minikube status and starts a single node minikube cluster if none exists.
> - Switches docker environment to minikube.
> - Deletes old images of the application and rebuilds a new docker image.
> - Gets the minikube IP address to add it as an External IP to the application loadbalancer service.
> - Creates a Kubernetes Application Deployment for our Python HTTP-API.
> - Creates a Kubernetes LoadBalancer Service for our application.
> - Exposes the Application LoadBalancer service to the host via minikube tunnel.
> - Waits for minikube endpoint url to be published to the configuration file we created in step 1.
> - Tests the application endpoints response by accessing the published url via curl.
> - Prints information on how to access the application via curl.

### Time to DEPLOY :hammer_and_wrench:
```bash
$ cd http_api
# Update inventory file with correct details. Details on how to update inventory file shall be found in the link below this section.
# Run the below ansible playbook to deploy a simple Python HTTP-API.
$ ansible-playbook -i inventory http-api-deployment.yaml --extra-vars ansible_python_interpreter=/usr/bin/python3
# For better analysis, add -vvv to the above command for verbose output.
```

### [How to build your inventory](https://docs.ansible.com/ansible/latest/user_guide/intro_inventory.html#how-to-build-your-inventory) << click on the link

### Time to TEST :t-rex:
> **/** path returns "**Server Works!**".
```bash
# Copy the lines from playbook output and run it in your terminal to test it manually.

$ curl http://localhost:58729/
Server Works!

# Product endpoints returns product info
$ curl http://localhost:58729/product/Pixel
{
"productName": "Pixel",
"productModel": 5,
"productDescription": "A Good smart phone. Because I'm using it"
}
```

### Other helpful resources
> [What is Python?](https://www.python.org/)  
> [What is an Ansible-Playbook?](https://docs.ansible.com/ansible/latest/user_guide/playbooks.html)  
> [What is Docker?](https://docs.docker.com/get-started/)  
> [What is Kubernetes?](https://kubernetes.io/docs/tutorials/kubernetes-basics/)  
> [What is Minikube?](https://minikube.sigs.k8s.io/docs/start/)  
> [How to setup WSL?](https://fireship.io/lessons/windows-10-for-web-dev/) 

### Some more internals

- Playbook tasks to post mock data & validate
- Playbook tasks to delete mock data & validate
- Adding playbook output execution from test runs
- Publishing docker image to docker hub
 
