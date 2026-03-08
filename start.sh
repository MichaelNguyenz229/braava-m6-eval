#!/bin/bash
# ================================
# Braava M6 Eval — Start Session
# ================================

# Detect OS and activate correct venv path
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

echo "Virtual environment activated."
echo "Python: $(which python)"
echo "Ready to work. Run 'source done.sh' when finished."