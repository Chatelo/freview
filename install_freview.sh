#!/bin/bash
set -e

# FReview Installation Script
# This script installs FReview Flask project review tool

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Install uv if not present
install_uv() {
    if command_exists uv; then
        print_status "uv is already installed"
        return 0
    fi
    
    print_status "Installing uv package manager..."
    if curl -LsSf https://astral.sh/uv/install.sh | sh; then
        print_success "uv installed successfully"
        # Source the shell profile to make uv available
        export PATH="$HOME/.cargo/bin:$PATH"
        return 0
    else
        print_error "Failed to install uv"
        return 1
    fi
}

# Install FReview using uv
install_freview_uv() {
    print_status "Installing FReview using uv..."
    if uv tool install freview; then
        print_success "FReview installed successfully with uv"
        return 0
    else
        print_warning "Failed to install from PyPI with uv, trying from source..."
        if uv tool install git+https://github.com/Chatelo/freview.git; then
            print_success "FReview installed successfully from source"
            return 0
        else
            print_error "Failed to install FReview with uv"
            return 1
        fi
    fi
}

# Install FReview using pipx (fallback)
install_freview_pipx() {
    if ! command_exists pipx; then
        print_status "Installing pipx..."
        if command_exists pip; then
            pip install --user pipx
            pipx ensurepath
        elif command_exists pip3; then
            pip3 install --user pipx
            pipx ensurepath
        else
            print_error "Neither pip nor pip3 found. Cannot install pipx."
            return 1
        fi
    fi
    
    print_status "Installing FReview using pipx..."
    if pipx install freview; then
        print_success "FReview installed successfully with pipx"
        return 0
    else
        print_warning "Failed to install from PyPI with pipx, trying from source..."
        if pipx install git+https://github.com/Chatelo/freview.git; then
            print_success "FReview installed successfully from source"
            return 0
        else
            print_error "Failed to install FReview with pipx"
            return 1
        fi
    fi
}

# Install FReview using pip (last resort)
install_freview_pip() {
    print_status "Installing FReview using pip..."
    if command_exists pip; then
        PIP_CMD="pip"
    elif command_exists pip3; then
        PIP_CMD="pip3"
    else
        print_error "No pip command found"
        return 1
    fi
    
    if $PIP_CMD install --user freview; then
        print_success "FReview installed successfully with $PIP_CMD"
        return 0
    else
        print_warning "Failed to install from PyPI with $PIP_CMD, trying from source..."
        if $PIP_CMD install --user git+https://github.com/Chatelo/freview.git; then
            print_success "FReview installed successfully from source"
            return 0
        else
            print_error "Failed to install FReview with $PIP_CMD"
            return 1
        fi
    fi
}

# Verify installation
verify_installation() {
    print_status "Verifying installation..."
    
    # Give the shell time to refresh PATH
    sleep 1
    
    # Try to find freview in common locations
    FREVIEW_PATH=""
    for path in "$HOME/.local/bin/freview" "$HOME/.cargo/bin/freview" "/usr/local/bin/freview" "$(which freview 2>/dev/null)"; do
        if [[ -x "$path" ]]; then
            FREVIEW_PATH="$path"
            break
        fi
    done
    
    if [[ -n "$FREVIEW_PATH" ]]; then
        print_success "FReview found at: $FREVIEW_PATH"
        if VERSION_OUTPUT=$("$FREVIEW_PATH" --version 2>/dev/null); then
            print_success "Installation verified: $VERSION_OUTPUT"
            return 0
        else
            print_warning "FReview installed but --version failed. Trying alternative..."
            if VERSION_OUTPUT=$("$FREVIEW_PATH" version 2>/dev/null); then
                print_success "Installation verified: $VERSION_OUTPUT"
                return 0
            fi
        fi
    fi
    
    # Try with just 'freview' command
    if command_exists freview; then
        if VERSION_OUTPUT=$(freview --version 2>/dev/null); then
            print_success "Installation verified: $VERSION_OUTPUT"
            return 0
        elif VERSION_OUTPUT=$(freview version 2>/dev/null); then
            print_success "Installation verified: $VERSION_OUTPUT"
            return 0
        fi
    fi
    
    print_error "Installation verification failed. Please check your PATH and try running 'freview --version' manually."
    return 1
}

# Show usage instructions
show_usage() {
    echo
    print_success "🎉 FReview installation complete!"
    echo
    echo "Usage:"
    echo "  freview --version              # Check version"
    echo "  freview --help                 # Show help"
    echo "  freview review /path/to/flask  # Review a Flask project"
    echo "  freview init /path/to/flask    # Initialize config"
    echo
    echo "For more information, visit: https://github.com/Chatelo/freview"
    echo
    print_warning "Note: You may need to restart your terminal or run 'source ~/.bashrc' (or ~/.zshrc)"
    print_warning "if the 'freview' command is not immediately available."
}

# Main installation function
main() {
    echo
    echo "🔧 FReview Installation Script"
    echo "=============================="
    echo
    
    # Try installation methods in order of preference
    if install_uv && install_freview_uv; then
        if verify_installation; then
            show_usage
            exit 0
        fi
    fi
    
    print_warning "uv installation failed, trying pipx..."
    if install_freview_pipx; then
        if verify_installation; then
            show_usage
            exit 0
        fi
    fi
    
    print_warning "pipx installation failed, trying pip..."
    if install_freview_pip; then
        if verify_installation; then
            show_usage
            exit 0
        fi
    fi
    
    print_error "All installation methods failed. Please install manually:"
    echo "1. Install uv: curl -LsSf https://astral.sh/uv/install.sh | sh"
    echo "2. Install FReview: uv tool install freview"
    echo "3. Or use pip: pip install --user freview"
    echo
    echo "For help, visit: https://github.com/Chatelo/freview/issues"
    exit 1
}

# Run main function
main "$@"
