#!/bin/sh

set -e

ME=$(basename $0)
SENDMAIL_CONFIG_FILE="/etc/mail/sendmail.mc"

entrypoint_log() {
    if [ -z "${ENTRYPOINT_QUIET_LOGS:-}" ]; then
        echo "$ME: $@"
    fi
}

replace_or_add(){
    FILE=$1
    LINE_REGEX=$2
    SUBST=$3

    if grep -q "$LINE_REGEX" "$FILE"; then
        # Replace the line
        sed -i "s/$LINE_REGEX/$SUBST/" "$FILE"
    else
        # Add the line
        echo "$SUBST" >> "$FILE"
    fi

}

entrypoint_log "EMAIL_SERVER_ADDR is $EMAIL_SERVER_ADDR"
entrypoint_log "EMAIL_SENDER_HOSTNAME is $EMAIL_SENDER_HOSTNAME"

entrypoint_log "Set local domain name..."
echo "$(hostname -i) $(hostname) $(hostname).localhost" >> /etc/hosts

entrypoint_log "Altering sendmail config..."
replace_or_add $SENDMAIL_CONFIG_FILE "^define(\`SMART_HOST'.*"          "define(\`SMART_HOST', \`${EMAIL_SERVER_ADDR}')dnl"
replace_or_add $SENDMAIL_CONFIG_FILE "^define(\`RELAY_MAILER'.*"        "define(\`RELAY_MAILER',\`esmtp')dnl"
replace_or_add $SENDMAIL_CONFIG_FILE "^define(\`RELAY_MAILER_ARGS'.*"   "define(\`RELAY_MAILER_ARGS', \`TCP \$h 587')dnl"

entrypoint_log "Compiling the new sendmail config..."
cd /etc/mail
make

entrypoint_log "Reloading sendmail..."
service sendmail restart

entrypoint_log "Configuring PHP application..."
sed -i "s/.*mail.force_extra_parameters.*/mail.force_extra_parameters = -f${EMAIL_SENDER_HOSTNAME}/g" /usr/local/etc/php/php.ini

entrypoint_log "sendmail configured."
exit 0
