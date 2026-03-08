#!/bin/bash
# ================================
# Braava M6 Eval — End Session
# ================================

echo "Enter commit message:"
read COMMIT_MSG

git add .
git commit -m "$COMMIT_MSG"
git push

echo "Pushed to GitHub."
deactivate
echo "Virtual environment deactivated. Session complete."