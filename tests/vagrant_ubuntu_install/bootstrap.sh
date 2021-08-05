#!/usr/bin/env bash
set -euo pipefail

apt-get update
apt-get install git

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
sed -n '/## Conclusion/q;p' install-on-ubuntu.md | # There are upgrade bash scripts in the conclusion we dont want to run here
sed -n '/^```bash$/,/^```$/p' | # Extract bash code from markdown code blocks
sed '/^```/ d' | # Get rid of the backticks left in by the previous sed
sed 's/^\$ //' | 
sed 's/^sudo passwd baserow/echo "yourpassword" | sudo passwd baserow --stdin/' > install-on-ubuntu.sh

echo -e "set -euo pipefail\n$(cat install-on-ubuntu.sh)" > install-on-ubuntu.sh

bash install-on-ubuntu.sh
