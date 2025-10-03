# task to perform when a minion attaches to the master (triggered by the )
{% set minion_id = data.get('id', '') %}
{% set ts = data.get('_stamp', '') %}

notify_new_minion_{{ minion_id }}:
  local.http.query:
    # Run the HTTP call from a specific minion. Commonly, the master also runs a minion; use its ID here.
    - tgt: {{ minion_id }}
    - arg:
      - http://salt-logger.set.lab:5000/webhook
    - kwarg:
        method: POST
        header_dict:
          Content-Type: application/json
        data: |
          {"event":"recovery_minion_connected","minion_id":"{{ minion_id }}","timestamp":"{{ ts }}","source_master":"recovery-master.set.lab"}
        status: True
        decode: True
