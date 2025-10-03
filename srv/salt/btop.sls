# Example state file to ensure that the btop package is installed
install_btop:
  pkg.installed:
    - name: btop
