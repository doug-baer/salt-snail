# /srv/salt/top.sls - the "top" file that defines state for everyone
base:
  '*':
    - editor/vim
    - btop
    - malware_demo/snail
  'web*':
    - nginx

