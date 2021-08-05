# Vagrant Baserow Ubuntu Install Test

This folder contains a vagrant file and bootstrap.sh which together will start up a 
local virtual machine with Baserow installed and working. To do this it extracts the 
bash from the install-on-ubuntu.md guide and runs it in a fresh new VM.

## How to run

1. Install vagrant https://www.vagrantup.com/downloads
2. cd tests/vagrant_ubuntu_install
3. vagrant up
4. Wait a long time for everything to be provisioned
5. Once done visit localhost:3000 on your host machine to see the Baserow running inside 
   the vm.