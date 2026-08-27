#!/bin/bash

echo "=========================================="
echo "GitHub Upload Script"
echo "=========================================="
echo ""
echo "Repository: network-anomaly-detection"
echo "GitHub: omsoni2795-hash"
echo ""

# Check if remote already exists
if git remote | grep -q "origin"; then
    echo "Removing existing remote..."
    git remote remove origin
fi

# Add remote
echo "Adding GitHub remote..."
git remote add origin https://github.com/omsoni2795-hash/network-anomaly-detection.git

# Rename branch to main
echo "Renaming branch to main..."
git branch -M main

echo ""
echo "=========================================="
echo "Ready to Push!"
echo "=========================================="
echo ""
echo "When prompted:"
echo "  Username: omsoni2795-hash"
echo "  Password: Use your GitHub Personal Access Token"
echo ""
echo "Don't have a token? Get one at:"
echo "https://github.com/settings/tokens/new"
echo ""
echo "Required scope: repo (full control)"
echo ""
read -p "Press Enter to continue..."

# Push to GitHub
echo ""
echo "Pushing to GitHub..."
git push -u origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "=========================================="
    echo "SUCCESS!"
    echo "=========================================="
    echo ""
    echo "Your repository is now live at:"
    echo "https://github.com/omsoni2795-hash/network-anomaly-detection"
    echo ""
else
    echo ""
    echo "=========================================="
    echo "Push failed. Common fixes:"
    echo "=========================================="
    echo ""
    echo "1. Make sure you created the repository on GitHub first"
    echo "   https://github.com/new"
    echo ""
    echo "2. Use a Personal Access Token (not password)"
    echo "   https://github.com/settings/tokens/new"
    echo ""
    echo "3. Token must have 'repo' scope enabled"
    echo ""
fi
