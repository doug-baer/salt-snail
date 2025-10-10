# /srv/pillar/top.sls
base:
  '*':
    - root_user        # loads /srv/pillar/root_user.sls for all minions
