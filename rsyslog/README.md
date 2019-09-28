This works a bit weirdly, but should be alright:

- if you only set `log_default: True`, it will forward all logs to a remote server (defaults are just placeholders, a proper IP and port can be set via the `remote_syslog_server_ip` and `remote_syslog_server_port` variables)
- if you only set `log_custom: True`, it will create a custom configuration in /etc/rsyslog.d/90-log-custom-file.conf that will forward the defined facility (configurable via the `log_custom_facility` variable)
- if you set both `log_default: True` and `log_custom: True`, it will create a configuration for both the custom log file and remote logging for all system files; since the global config for log forwarding supersedes just sending a single facility to a remote syslog server, that line will be omitted from /etc/rsyslog.d/90-log-custom-file.conf
