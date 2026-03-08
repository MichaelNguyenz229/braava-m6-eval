#!/bin/bash
# ================================
# Braava M6 Eval — Push to GitHub
# ================================

echo "Enter commit message:"
read COMMIT_MSG

git add .
git commit -m "$COMMIT_MSG"
git push

echo "Done. Pushed to GitHub."