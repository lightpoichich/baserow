# Vagrant Baserow Ubuntu Install Test

This folder contains a vagrant file and bootstrap.sh which together will start up a 
local virtual machine with Baserow installed and working. To do this it extracts the 
bash from the install-on-ubuntu.md guide and runs it in a fresh new VM.

## How to run

1. Install virtualbox - https://www.virtualbox.org/wiki/Downloads
1. Install vagrant - https://www.vagrantup.com/downloads
1. `cd tests/vagrant_ubuntu_install`
1. `vagrant plugin install landrush`
1. On Ubuntu I had to follow the instructions in https://github.com/vagrant-landrush/landrush/blob/master/doc/Usage.adoc#visibility-on-the-host
   1. Also see https://gist.github.com/neuroticnerd/30b12648a933677ad2c4 for more 
      landrush dns tips.
1. `vagrant up`
   1. You might need to interactively enter your password for the landrush dns plugin to 
      successfully add local dns entries on your host for Baserow running inside the vm.
1. Wait a long time for everything to be provisioned
1. Once done visit [http://baserow.vagrant.test](http://baserow.vagrant.test) on your host machine to see the Baserow running inside 
   the vm.
1. Run `vagrant ssh` to ssh into the VM and make changes, inspect the logs, restart 
   services etc.