# rhelai-validation

## Running from a crc hypervisor node
Once the RHOSO + RHEL AI setup is complete, do the following:

1. Clone the repository
    ```
    git clone https://gitlab.cee.redhat.com/eng/openstack/team/ai-enablement/rhelai-validation.git
    cd rhelai-validation/
    ```
1. (Optional - see NOTE below) Create a credentials file for registry login using a token. You can generate one at [here](https://access.redhat.com/terms-based-registry/) after logging in.

    NOTE - If not providing registry credentials, you must disable model tests with `-e model_tests_enabled=false`

    creds.yaml
    ```
    model_download_registry_username: "|3c5aa7e0-9bb9...."
    model_download_registry_password: "eyJhbGciOiJSUzUxMiJ9...."
    ```
1. Set up and test your access to RHOSO
    ```
    oc cp openstackclient:.config/openstack/ ~/.config/openstack
    oc cp openstackclient:/etc/pki/ca-trust/extracted/pem/tls-ca-bundle.pem ./tls-ca-bundle.pem
    export OS_CLOUD=default
    openstack --os-cacert ./tls-ca-bundle.pem flavor list
    ```
1. Install Ansible dependencies
    ```
    ansible-galaxy install -r requirements.yaml
    ```
1. Run it (requires ansible-core>=2.15)
    ```
    JUNIT_OUTPUT_DIR=./ ansible-playbook -i inventory main.yaml -e @vars.yaml -e @creds.yaml -e '{"pci_devices":{"10de:20f1": 1}}'
    ```

## Running w/ test-operator

1. Confirm that your RHOSO deployment has test-operator running
    ```
    $ oc get deploy -n openstack-operators test-operator-controller-manager
    NAME                               READY   UP-TO-DATE   AVAILABLE   AGE
    test-operator-controller-manager   1/1     1            1           29d
    ```
1. Adjust the `pci_devices` variable in AnsibleTestCRD.yaml to match your hardware
1. Provide an SSH key to use for access to RHELAI VM
    ```
    oc create secret generic rhelai-vm-secret-key --from-file=ssh-privatekey=$HOME/.ssh/rhel-ai.pem
    ```
1. Launch the test container
    ```
    $ oc apply -f AnsibleTestCRD.yaml
    ```
