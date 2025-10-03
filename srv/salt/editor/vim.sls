# Example state file to ensure the 'vim' package is installed
vim_package:
  pkg.installed:
    - name: vim

# State to manage the user's .vimrc file
vim_config:
  file.managed:
    - name: /home/tech/.vimrc
    - source: salt://editor/vimrc
    - user: tech
    - group: tech
    - mode: 644
    - require:
      - pkg: vim_package

