#!/bin/bash
#
# trims autowhitelist

echo "DELETE FROM sa_txrep WHERE count=1" | mysql --user="<%=node['mailserver']['db_user']%>" --password="<%=node['mailserver']['db_pass']%>" <%=node['mailserver']['db_name']%>
