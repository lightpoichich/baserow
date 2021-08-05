#!/usr/bin/env bash
set -euo pipefail

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

su - $USERNAME

cd ~
git clone -b $BRANCH_NAME $REPO_URL download_tutorial_repo 
cp download_tutorial_repo/docs/guides/installation/install-on-ubuntu.md install-on-ubuntu.md
# Process the guide to only extract the bash we want
sed -n '/## Install & Configure Supervisor/q;p' install-on-ubuntu.md | # There are upgrade bash scripts in the conclusion we dont want to run here
sed -n '/^```bash$/,/^```$/p' | # Extract bash code from markdown code blocks
sed '/^```/ d' | # Get rid of the backticks left in by the previous sed
sed 's/^\$ //' | 
sed 's/^sudo passwd baserow/echo -e "yourpassword\nyourpassword" | sudo passwd baserow/' > install-on-ubuntu.sh

# We dont set -u here due to problems with it using an old virtualenv and PS1 not being
# set. See https://stackoverflow.com/questions/42997258/virtualenv-activate-script-wont-run-in-bash-script-with-set-euo
echo -e "set -eox pipefail\n$(cat install-on-ubuntu.sh)" > install-on-ubuntu.sh

bash install-on-ubuntu.sh
