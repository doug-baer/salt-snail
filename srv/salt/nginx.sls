# More complex state file example for a web service
network_utilities:
  pkg.installed:
    - pkgs:
      - rsync
      - curl

nginx_pkg:
  pkg.installed:
    - name: nginx

nginx_service:
  service.running:
    - name: nginx
    - enable: True
    - require:
      - pkg: nginx_pkg
