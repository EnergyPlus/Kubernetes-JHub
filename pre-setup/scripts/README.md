# ansible-conf-python-script
A simple script to generate Ansible configuration, depending on the target: Local using Vagrant, server, or cloud.

# **Warning** this script is under development

# Usage
Copy the folder `scripts` inside the folder from which Ansible is going to run. `cd` into the repository. Modify the `json` file to your requirements and run the script

    $ python jhub_env_deployment.py

Go back to the Ansible folder, and the files:
  - inventory
  - ansible.cfg
  - ssh.config

should be in the folder.
