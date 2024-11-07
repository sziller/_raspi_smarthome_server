#!/bin/bash
# Script to set up the initial branches for a Git repository.
# It creates and pushes the following branches (by default):
# - development
# - staging
# - production
# you can extend this by modifying 'branches' below.
# This script assumes it is being run from the root of an initialized Git repository.
# the initial branch listed will be checked out once script finishes.

# Run the script by... (assuming it's called 'stp_git-branches.sh')
# ... making it executable:
# chmod +x stp_git-branches.sh
# ... and actually running it: 
# ./stp_git-branches.sh

set -e  # Exit immediately if a command exits with a non-zero status
dmn="brs"
proj="parent Git repository"
default_branch_name="main"  # Set to "main" or "master" as preferred default branch name only if no branches exist
branches=("development" "staging" "production")  # Define branches to create: first one will be activated at script-end

# Confirm the script is running under bash
if [ -z "$BASH_VERSION" ]; then
  echo "[$dmn]: ERROR - This script requires bash to run."
  exit 1
fi

# Welcome messages
echo "[$dmn]: >>> Welcome to Sziller's Git branch setup manager!"
echo "[$dmn]: START - Setting up branches for $proj"

# Verify that we are in a Git repository
if [[ ! -d .git || ! -e .git/HEAD ]]; then
  echo "[$dmn]: ERROR - This script must be run in the root of a Git repository."
  echo "[$dmn]: DEBUG - .git directory not found. Exiting."
  exit 1
else
  echo "[$dmn]: DEBUG - .git directory found. Continuing..."
fi

# Determine the default branch (main or master)
default_branch=""
if git show-ref --verify --quiet refs/heads/main; then
  default_branch="main"
elif git show-ref --verify --quiet refs/heads/master; then
  default_branch="master"
else
  echo "[$dmn]: INFO - No 'main' or 'master' branch found. Creating an initial commit on 'main'."
  default_branch="$default_branch_name"
  
  # Create a README file for the initial commit if no tracked files exist
  if [[ -z $(git ls-files) ]]; then
    echo "# Initial Commit" > README.md
    echo "**WARNING**: Initial branch called: < '$default_branch_name' > created by setup script." >> README.md
    git add README.md
  fi

  # Make the initial commit and create the main branch
  git commit -m "Initial commit" || echo "[$dmn]: INFO - Initial commit already exists."
  git branch -M "$default_branch_name"  # Ensure the branch is named as per default_branch_name
fi

# Check if a remote exists
remote=$(git remote | head -n 1)  # Gets the first remote name, if it exists

# Function to create and push a branch if it doesn't exist
create_and_push_branch() {
  branch=$1
  if git show-ref --verify --quiet refs/heads/$branch; then
    echo "[$dmn]: INFO  - Branch '$branch' already exists locally."
  else
    echo "[$dmn]: CREATING - Branch '$branch' based on '$default_branch'"
    git checkout -b $branch $default_branch
    if [[ -n "$remote" ]]; then
      git push -u "$remote" $branch
      echo "[$dmn]: PUSHED - Branch '$branch' to remote '$remote'."
    else
      echo "[$dmn]: INFO  - No remote found. Branch '$branch' created locally only."
    fi
  fi
}

# Start from the default branch (main or master)
echo "[$dmn]: SWITCHING - Checking out '$default_branch' branch"
git checkout $default_branch

# Loop through branches and create each one
for branch in "${branches[@]}"; do
  create_and_push_branch "$branch"
done

# Switch to development branch at the end
first_branch="${branches[0]}"
echo "[$dmn]: SWITCHING - Checking out '$first_branch' branch"
git checkout "$first_branch"

echo "[$dmn]: COMPLETED - All branches created. Currently on '$first_branch'."

