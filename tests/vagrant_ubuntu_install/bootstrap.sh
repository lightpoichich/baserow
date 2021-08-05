#!/usr/bin/env bash
set -euox pipefail

apt-get update
apt-get install git -y

REPO_URL=$1
BRANCH_NAME=$2

# Setup a test user who represents the actual user following the guide
USERNAME=test_user
# Let this test user sudo without a password so we don't need to try and enter it interactively during the doc script test
echo %$USERNAME ALL=NOPASSWD:ALL > /etc/sudoers.d/$USERNAME
chmod 0440 /etc/sudoers.d/$USERNAME
useradd -m -s /bin/bash -U $USERNAME 
usermod -aG sudo $USERNAME  

cd /home/$USERNAME/
git clone -b $BRANCH_NAME $REPO_URL download_tutorial_repo
cp download_tutorial_repo/docs/guides/installation/install-on-ubuntu.md install-on-ubuntu.md

# Process the guide to only extract the bash we want
sed -n '/## HTTPS \/ SSL Support/q;p' install-on-ubuntu.md | # We don't want to setup https or do any upgrade scripts which follow
sed -n '/^```bash$/,/^```$/p' | # Extract bash code from markdown code blocks
sed '/^```/ d' | # Get rid of the backticks left in by the previous sed
sed 's/^\$ //' | # Get rid of the bash command $ prefixes
sed 's/^sudo passwd baserow/echo -e "yourpassword\nyourpassword" | sudo passwd baserow/' | # Enter a password non interactively
sed "s/git clone --branch master/git clone --branch $BRANCH_NAME/g" | # Checkout the same branch inside the test
sed 's/https:\\\/\\\/api.domain.com/http:\\\/\\\/api.baserow.vagrant.test/g' | # Fixup the sed commands for the URL env vars
sed 's/https:\\\/\\\/baserow.domain.com/http:\\\/\\\/baserow.vagrant.test/g' |
sed 's/https:\\\/\\\/media.domain.com/http:\\\/\\\/media.baserow.vagrant.test/g' |
sed 's/api.domain.com/api.baserow.vagrant.test/g' | # Fixup the sed commands for the ngnix config
sed 's/baserow.domain.com/baserow.vagrant.test/g' |
sed 's/media.domain.com/media.baserow.vagrant.test/g' > install-on-ubuntu.sh

# Prepend with some bash settings so we can see the output and it will fail if something
# crashes.
# We dont set -u here due to problems with it using an old virtualenv and PS1 not being
# set. See https://stackoverflow.com/questions/42997258/virtualenv-activate-script-wont-run-in-bash-script-with-set-euo
echo -e "set -eox pipefail\n$(cat install-on-ubuntu.sh)" > install-on-ubuntu.sh

chown $USERNAME install-on-ubuntu.sh
su $USERNAME -c "bash /home/$USERNAME/install-on-ubuntu.sh"
