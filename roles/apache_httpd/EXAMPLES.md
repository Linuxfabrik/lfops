# Ansible Role linuxfabrik.lfops.apache_httpd - Config Examples, Tips & Tricks

## HTTP/2

HTTP/2 is supported only over an encrypted connection. The website must be served over a secure TLS connection and accessed through https:// in the browser. Therefore, all Apache servers in the chain must be enabled for TLS before HTTP/2 is used.

* For Proxy servers, use Let's Encrypt certificates.
* For App servers, use self-signed certificates.


## vHosts

### Minimal App vHost with PHP-FPM

A minimal working "app" vHost definition for a PHP-FPM application, located under http://test:
```yaml
apache_httpd__conf_server_admin: 'webmaster@example.com'
apache_httpd__mods__host_var:
  - filename: 'cgi'
    enabled: true
    state: 'present'
  - filename: 'proxy_fcgi'
    enabled: true
    state: 'present'
apache_httpd__vhosts__host_var:
  - template: 'app'
    virtualhost_port: 80
    authz_document_root: |-
        Require all granted
    conf_directory_index: 'index.php'
    conf_server_name: 'test'
```

### Reverse Proxy

```yaml
apache_httpd__mods__host_var:
  - filename: 'deflate'
    enabled: true
    state: 'present'
    template: 'deflate'
  - filename: 'proxy_http'
    enabled: true
    state: 'present'
    template: 'proxy_http'
  - filename: 'filter'
    enabled: true
    state: 'present'
    template: 'filter'
apache_httpd__vhosts__host_var:
  - template: 'proxy'
    allowed_http_methods:
      - 'GET'
      - 'OPTIONS'
      - 'POST'
      - 'PUT'
    conf_custom_log: 'logs/www.example.com-access.log linuxfabrikio'
    conf_directory_index: 'index.php'
    conf_proxy_error_override: 'Off'
    conf_proxy_preserve_host: 'On'
    conf_server_name: 'www.example.com'
    raw: !unsafe |-
      RequestHeader set X-Forwarded-Proto "https"
      # ssl_module
      SSLEngine on
      SSLCertificateFile      /etc/pki/tls/certs/www.example.com.crt
      SSLCertificateKeyFile   /etc/pki/tls/private/www.example.com.key
      SSLCertificateChainFile /etc/pki/tls/certs/www.example.com-fullchain.crt
      # proxy_module and other
      <Proxy *>
          Require all granted
      </Proxy>
      RewriteRule ^/(.*) http://webserver/$1 [proxy,last]
      ProxyPassReverse / http://webserver/
      ProxyPassReverse / http://www.example.com/
```

### Redirect vHost

```yaml
apache_httpd__vhosts__host_var:
  - template: 'redirect'
    virtualhost_port: 80
    conf_server_name: 'www.example.com'
```


### A non-hardened standard Apache vHost

This is an Apache configuration that is close to the RHEL default configuration, without any CIS remediations.

```yaml
apache_httpd__conf__host_var:
  - filename: 'expires'
    enabled: false
    state: 'present'
    template: 'expires'
  - filename: 'headers'
    enabled: false
    state: 'present'
    template: 'headers'
  - filename: 'mod_security'
    enabled: false
    state: 'present'
    template: 'mod_security'
apache_httpd__conf_add_default_charset: 'Off'
apache_httpd__conf_enable_send_file: 'Off'
apache_httpd__conf_limit_request_body: 1073741824
apache_httpd__conf_max_keep_alive_requests: 100
apache_httpd__conf_timeout: 60
apache_httpd__conf_trace_enable: 'On'
apache_httpd__mods__host_var:
  - filename: 'cgid'
    enabled: true
    state: 'present'
    template: 'cgid'
  - filename: 'deflate'
    enabled: true
    state: 'present'
    template: 'deflate'
  - filename: 'filter'
    enabled: true
    state: 'present'
    template: 'filter'
  - filename: 'http2'
    enabled: true
    state: 'present'
    template: 'http2'
  - filename: 'proxy_http'
    enabled: true
    state: 'present'
    template: 'proxy_http'
  - filename: 'proxy_wstunnel'
    enabled: true
    state: 'present'
    template: 'proxy_wstunnel'
apache_httpd__vhosts__host_var:
  - template: 'proxy'
    virtualhost_port: 443
    allowed_http_methods:
      - '.*'
    conf_proxy_timeout: 60
    conf_server_name: 'www.example.com'
    conf_timeout: 60
    raw: !unsafe |-
      RequestHeader set X-Forwarded-Proto "https"
      # ssl_module
      SSLEngine on
      SSLCertificateFile      /etc/pki/tls/certs/www.example.com.crt
      SSLCertificateKeyFile   /etc/pki/tls/private/www.example.com.key
      SSLCertificateChainFile /etc/pki/tls/certs/www.example.com-fullchain.crt
      # proxy_module and other
      <Proxy *>
          Require all granted
      </Proxy>
      RewriteRule ^/(.*) http://webserver/$1 [proxy,last]
      ProxyPassReverse / http://webserver/
      ProxyPassReverse / http://www.example.com/
```


## `raw` Variable

A list of best practise Apache Configs and config snippets at your free disposal for the `raw` variable (which is inserted just before the closing `VirtualHost` directive). Unsorted. Use them as a starting point.

To implement a multiline `raw` statement, do this:

```yaml
raw: !unsafe |-
  # my config here...
```

To pass `{%Y-...` to `raw`-values, do this:
```yaml
raw: !unsafe |-
    LogFormat "%h %u [%{%Y-%m-%d %H:%M:%S}t.%{usec_frac}t] \"%r\" %>s %b" mylog
```



### mod_rewrite

Redirect from port 80 to port 443, including one exception:

```
RewriteCond %{SERVER_PORT} 80
RewriteCond %{REQUEST_URI} !^/\.well\-known/acme\-challenge/
RewriteRule ^(.*)$ https://%{HTTP_HOST}$1 [redirect=301,last]
```

Block IP addresses and ranges:

```
RewriteCond %{REMOTE_ADDR} ^10\.0\.0\.1 [OR]
RewriteCond %{REMOTE_ADDR} ^10\.32\.64\.250
RewriteRule ^ - [nocase,forbidden,last]
```

Block referrer links:

```
RewriteCond %{HTTP_REFERER} ^http(?:s)?://(?:.*)?\.(?:cc|eu|ru)(?:/.*)?$ [nocase,OR]
RewriteCond %{HTTP_REFERER} ^http(?:s)?://(?:.*\.)?(?:example1.com|example2.com)(?:/.*)?$ [nocase]
RewriteRule ^ - [nocase,forbidden,last]
```

Block requests with empty HTTP_USER_AGENT String:

```
RewriteCond %{HTTP_USER_AGENT} ^(?:\s|-)*$
RewriteRule ^ - [nocase,forbidden,last]
```

Block hotlinking to files:

```
RewriteCond %{HTTP_REFERER} !^$
RewriteCond %{HTTP_REFERER} !^http(?:s)?://(?:.*\.)?example\.net(?:/.*)?$ [nocase]
RewriteRule \.(?:jpe?g|gif|png|svg|webp|zip|rar|pdf)$ - [nocase,forbidden,last]
```


### HTTP Basic Authentication

CIS: You do not want to use this - it does not meet current security standards for protecting the login credentials and protecting the authenticated session.

```
<Location />
    AuthType Basic
    AuthName "Restricted Area"
    AuthBasicProvider file
    AuthUserFile /etc/httpd/.htpasswd
    Require user linuxfabrik-user
</Location>
```

Basic Auth for everything except one location:

```
<Location />
    AuthType Basic
    AuthName "Restricted Area"
    AuthBasicProvider file
    AuthUserFile /etc/httpd/.htpasswd
    Require expr %{REQUEST_URI} =~ m#^/except-this-url/.*#
    Require user linuxfabrik-user
</Location>
```


### Require directive examples

```
Require all denied
Require all granted

# complete subnet
Require ip 10.80

# a single IP
Require ip 192.168.109.7
Require local
Require user linuxfabrik-user
Require forward-dns host.example.com
```


### Security related HTTP headers

```
# Headers sorted by Category and Header Name
# https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers

# Caching
# https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Cache-Control

# Caching: Maybe disable browser's cache validation due to cache poisoning attacks
#Header unset ETag

# The Cache-Control header is defined as part of HTTP/1.1 specifications and supersedes previous headers (e.g. Expires).
# The maximum amount of time a resource is considered fresh, relative to the time of the request.
# Caching: holds instructions for caching in both requests and responses
#Header set Cache-Control: "max-age=0, no-cache, no-store, must-revalidate"
# the .+ at the start of the regex ensures that files named ".png", or ".gif", for example, are not matched
<FilesMatch ".+\.(css|flv|gif|html?|ico|jpe?g|js|png|svg|swf|ttf|txt|woff2?)$">
   Header set Cache-Control "max-age=864000, public"
</FilesMatch>

# Security related Header: CSP allows to control resources the user agent is allowed to
# load for a given page (helps guard against cross-site scripting attacks). Always use
# "default-src 'none'", especially for APIs.
# https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy

# Sample Safe Policy - start using this:
Header set Content-Security-Policy: "\
    default-src 'none'; \
    base-uri 'none'; \
    block-all-mixed-content; \
    child-src 'none'; \
    connect-src 'none'; \
    font-src 'none'; \
    form-action 'none'; \
    frame-ancestors 'none'; \
    frame-src 'none'; \
    img-src 'none'; \
    manifest-src 'none'; \
    media-src 'none'; \
    object-src 'none'; \
    prefetch-src 'none'; \
    require-trusted-types-for 'script'; \
    sandbox; \
    script-src 'none'; \
    style-src 'none'; \
    worker-src 'none'; \
    "

# A Report-Only Policy (for Browser Console)
#Header set Content-Security-Policy-Report-Only: "\
#    default-src 'none'; \
#    base-uri 'none'; \
#    block-all-mixed-content; \
#    child-src 'none'; \
#    connect-src 'none'; \
#    font-src 'none'; \
#    form-action 'none'; \
#    frame-ancestors 'none'; \
#    frame-src 'none'; \
#    img-src 'none'; \
#    manifest-src 'none'; \
#    media-src 'none'; \
#    object-src 'none'; \
#    prefetch-src 'none'; \
#    require-trusted-types-for 'script'; \
#    sandbox; \
#    script-src 'none'; \
#    style-src 'none'; \
#    worker-src 'none'; \
#    "

# A real-life example for docs.linuxfabrik.ch
#Header set Content-Security-Policy: " \
#    default-src 'self'; \
#    base-uri 'none'; \
#    child-src 'none'; \
#    connect-src 'self' https://analytics.linuxfabrik.ch; \
#    font-src 'self' https://use.fontawesome.com; \
#    form-action 'self'; \
#    frame-ancestors 'none'; \
#    frame-src 'none'; \
#    img-src 'self' https://analytics.linuxfabrik.ch https://img.shields.io; \
#    manifest-src 'none'; \
#    media-src 'none'; \
#    object-src 'none'; \
#    prefetch-src 'none'; \
#    sandbox allow-same-origin allow-forms allow-scripts; \
#    script-src 'self' 'unsafe-eval' 'unsafe-inline' https://analytics.linuxfabrik.ch https://use.fontawesome.com; \
#    style-src 'self' 'unsafe-inline' https://use.fontawesome.com; \
#    worker-src 'none'; \
#    "
# Also set this if CSP directives uses any "unsafe" values.
#Header set X-XSS-Protection: "1; mode=block"

# https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Access-Control-Allow-Origin
# Security Header: indicates whether the response can be shared with requesting code from the given origin
Header set Access-Control-Allow-Origin "https://test.linuxfabrik.ch"
#  the response should also include a Vary response header with the value Origin — to indicate to browsers that server responses can differ based on the value of the Origin request header.
Header set Vary "Origin"

# Security Header: lets sites opt in to reporting and/or enforcement of Certificate Transparency requirements, to prevent the use of misissued certificates from going unnoticed
Header set Expect-CT: "max-age=86400, enforce"
# Security Header: allows a site to control which features and APIs can be used in the browser
Header set Permissions-Policy: "accelerometer=(), camera=(), geolocation=(), gyroscope=(), magnetometer=(), microphone=(), payment=(), usb=()"
# Security Header: controls how much referrer information (sent via the Referer header) should be included with requests
Header set Referrer-Policy: "strict-origin-when-cross-origin"
# Security Header: stops a browser from trying to MIME-sniff the content type and forces it to stick with the declared content-type
Header set X-Content-Type-Options: "nosniff"
# Security Header: tells the browser whether you want to allow your site to be framed or not. "frame-ancestors" in CSP is used instead.
#Header set X-Frame-Options: "SAMEORIGIN"
# Security Header: feature of Internet Explorer, Chrome and Safari that stops pages from loading when they detect reflected cross-site scripting (XSS) attacks
# Note: Most major browsers have dropped / deprecated support for this header in 2020.

# User-Agent Detection: Use for websites without Responsive Web Design, or
# where the addition of a DEFLATE filter depends on the User-Agent.
#Header append Vary: "User-Agent"

# Proxy: may also needs changes to the backend web application
RequestHeader set X-Forwarded-Proto "https"
```


### SSL/TLS settings

```
SSLEngine on
SSLCertificateFile      {{ apache_httpd__openssl_certificate_path }}/localhost.pem
SSLCertificateKeyFile   {{ apache_httpd__openssl_privatekey_path }}/localhost.key
SSLCertificateChainFile {{ apache_httpd__openssl_chain_path }}/chain.pem
```


### mod_qos / Quality of Service

[mod_qos](http://mod-qos.sourceforge.net/index.html): If you decide to use HTTP/2, you should only use the request level control directives ("QS_Loc\*") as mod_qos works for the hypertext transfer protocol version 1.0 and 1.1 (RFC1945/RFC2616) only. If not using HTTP/2, you can use the full feature set of mod_qos, like this:

```
<IfModule qos_module>
    BrowserMatch "(curl|rclone|rsync|wget)" QS_Cond=tools

    # Defines the maximum allowed number of concurrent TCP connections for this virtual host.
    QS_SrvMaxConn                          100

    # Defines the maximum number of connections per source IP address for this virtual host.
    QS_SrvMaxConnPerIP                     1

    # Defines the number of concurrent requests for the specified request pattern (path and query).
    QS_LocRequestLimitMatch       "^.*$"   100

    # Only enforced for requests whose QS_Cond variable matches the specified condition:
    BrowserMatch "(curl|rclone|rsync|wget)" QS_Cond=tools
    QS_CondLocRequestLimitMatch   "^.*$"   1    tools

    # limits the download bandwidth when accessing MP4 files to 1 megabyte/sec
    # and does not allow more then 1 client to download such file type in
    # parallel:
    QS_LocKBytesPerSecLimitMatch \.mp4     1
    QS_LocRequestLimitMatch      \.mp4     1

    # Throttles the download bandwidth for the specified request pattern (path and query, in KBytes/sec).
    # If you want to throttle to 10 Mbit/sec (should be the default minimum), you have to provide "1250"
    # (multiply the data transfer rate value by 125).
    QS_LocKBytesPerSecLimitMatch  "^.*$"   1250
</IfModule>
```


### Proxy Passing Rules

BTW, using mod_rewrite is much more flexible than ProxyPass. This is an example of a reverse proxy passing incoming requests to a backend server.

```
# proxy_module and other
<Proxy *>
    Require all granted
</Proxy>
SSLProxyEngine On
SSLProxyCheckPeerCN Off
SSLProxyCheckPeerExpire On
RewriteRule ^/(.*) https://backend/$1 [proxy,last]
ProxyPassReverse / https://backend/
```

Load Balancing:

```yaml
apache_httpd__mods__host_var:
  - filename: 'lbmethod_byrequests'
    enabled: true
    state: 'present'
    template: 'lbmethod_byrequests'
  - filename: 'proxy_balancer'
    enabled: true
    state: 'present'
    template: 'proxy_balancer'
apache_httpd__vhosts__host_var:
  - template: 'proxy'
    raw: !unsafe |-
      <Proxy "balancer://mycluster">
          BalancerMember "http://srv10.example.com:80" route=1
          BalancerMember "http://srv11.example.com:80" route=2
          ProxySet lbmethod=byrequests
          ProxySet stickysession=ROUTEID
      </Proxy>
      RewriteRule      ^/(.*) balancer://mycluster/$1 [proxy,last]
      ProxyPassReverse / balancer://mycluster
```


### mod_maxminddb, GeoIP-Blocking

As a starting point. Have a look at https://docs.linuxfabrik.ch for details.

```
# GeoIP-Blocking
MaxMindDBEnable On
MaxMindDBFile COUNTRY_DB /usr/share/GeoIP/GeoLite2-Country.mmdb
MaxMindDBEnv MM_COUNTRY_CODE COUNTRY_DB/country/iso_code

# Deny all, but allow some specific countries, ordered alphabetically
SetEnvIf MM_COUNTRY_CODE AT AllowCountry
SetEnvIf MM_COUNTRY_CODE CH AllowCountry
SetEnvIf MM_COUNTRY_CODE DE AllowCountry
<Proxy *>
    <RequireAny>
        Require env AllowCountry
        # list of IP's in an external file, containing lines like
        # Require ip 10.1
        Include /etc/GeoIP-Whitelist.conf
    </RequireAny>
</Proxy>
```


### mod_security + OWASP CRS Rule Set

Will be installed on reverse proxy servers only.

As a starting point. Replace ``<MYVHOST>`` with your ``conf_server_name`` or FQDN.

```
<IfModule security2_module>

    LogFormat "%h %{GEOIP_COUNTRY_CODE}e %u [%{%Y-%m-%d %H:%M:%S}t.%{usec_frac}t] \"%r\" %>s %b \
    \"%{Referer}i\" \"%{User-Agent}i\" \"%{Content-Type}i\" %{remote}p %v %A %p %R \
    %{BALANCER_WORKER_ROUTE}e %X \"%{cookie}n\" %{UNIQUE_ID}e %{SSL_PROTOCOL}x %{SSL_CIPHER}x \
    %I %O %{ratio}n%% %D %{ModSecTimeIn}e %{ApplicationTime}e %{ModSecTimeOut}e \
    %{ModSecAnomalyScoreInPLs}e %{ModSecAnomalyScoreOutPLs}e \
    %{ModSecAnomalyScoreIn}e %{ModSecAnomalyScoreOut}e" extended

    LogFormat "[%{%Y-%m-%d %H:%M:%S}t.%{usec_frac}t] %{UNIQUE_ID}e %D \
    PerfModSecInbound: %{TX.perf_modsecinbound}M \
    PerfAppl: %{TX.perf_application}M \
    PerfModSecOutbound: %{TX.perf_modsecoutbound}M \
    TS-Phase1: %{TX.ModSecTimestamp1start}M-%{TX.ModSecTimestamp1end}M \
    TS-Phase2: %{TX.ModSecTimestamp2start}M-%{TX.ModSecTimestamp2end}M \
    TS-Phase3: %{TX.ModSecTimestamp3start}M-%{TX.ModSecTimestamp3end}M \
    TS-Phase4: %{TX.ModSecTimestamp4start}M-%{TX.ModSecTimestamp4end}M \
    TS-Phase5: %{TX.ModSecTimestamp5start}M-%{TX.ModSecTimestamp5end}M \
    Perf-Phase1: %{PERF_PHASE1}M \
    Perf-Phase2: %{PERF_PHASE2}M \
    Perf-Phase3: %{PERF_PHASE3}M \
    Perf-Phase4: %{PERF_PHASE4}M \
    Perf-Phase5: %{PERF_PHASE5}M \
    Perf-ReadingStorage: %{PERF_SREAD}M \
    Perf-WritingStorage: %{PERF_SWRITE}M \
    Perf-GarbageCollection: %{PERF_GC}M \
    Perf-ModSecLogging: %{PERF_LOGGING}M \
    Perf-ModSecCombined: %{PERF_COMBINED}M" perflog

    conf_error_logFormat "[%{cu}t] [%-m:%-l] %-a %-L %M"
    conf_log_level debug

    conf_error_log logs/modsec-<MYVHOST>-error.log
    conf_custom_log  logs/modsec-<MYVHOST>-access.log extended
    conf_custom_log  logs/modsec-<MYVHOST>-perf.log perflog env=write_perflog


    # == ModSec Base Configuration

    SecRuleEngine                 On

    SecRequestBodyAccess          On
    SecRequestBodyLimit           10000000
    SecRequestBodyNoFilesLimit    64000

    SecResponseBodyAccess         On
    SecResponseBodyLimit          10000000

    SecTmpDir                     /tmp/
    SecUploadDir                  /tmp/

    SecDebugLog                   logs/modsec-<MYVHOST>-debug.log
    SecDebugconf_log_level              0

    SecAuditEngine                RelevantOnly
    SecAuditLogRelevantStatus     "^(?:5|4(?!04))"
    SecAuditLogParts              ABEFHIJKZ

    SecAuditLogType               Concurrent
    SecAuditLog                   logs/modsec-<MYVHOST>-audit.log
    SecAuditLogStorageDir         logs/audit/

    SecDefaultAction              "phase:2,pass,log,tag:'Local Lab Service'"


    # == ModSec Rule ID Namespace Definition
    # Service-specific before Core Rule Set: 10000 -  49999
    # Service-specific after Core Rule Set:  50000 -  79999
    # Locally shared rules:                  80000 -  99999
    #  - Performance:                        90000 -  90199
    # Recommended ModSec Rules (few):       200000 - 200010
    # OWASP Core Rule Set:                  900000 - 999999


    # === ModSec timestamps at the start of each phase (ids: 90000 - 90009)

    SecAction "id:90000,phase:1,nolog,pass,setvar:TX.ModSecTimestamp1start=%{DURATION}"
    SecAction "id:90001,phase:2,nolog,pass,setvar:TX.ModSecTimestamp2start=%{DURATION}"
    SecAction "id:90002,phase:3,nolog,pass,setvar:TX.ModSecTimestamp3start=%{DURATION}"
    SecAction "id:90003,phase:4,nolog,pass,setvar:TX.ModSecTimestamp4start=%{DURATION}"
    SecAction "id:90004,phase:5,nolog,pass,setvar:TX.ModSecTimestamp5start=%{DURATION}"

    # SecRule REQUEST_FILENAME "@beginsWith /" \
    #    "id:90005,phase:5,t:none,nolog,noauditlog,pass,setenv:write_perflog"


    # === ModSec Recommended Rules (in modsec src package) (ids: 200000-200010)

    SecRule REQUEST_HEADERS:Content-Type "(?:application(?:/soap\+|/)|text/)xml" \
      "id:200000,phase:1,t:none,t:lowercase,pass,nolog,ctl:requestBodyProcessor=XML"

    SecRule REQUEST_HEADERS:Content-Type "application/json" \
      "id:200001,phase:1,t:none,t:lowercase,pass,nolog,ctl:requestBodyProcessor=JSON"

    SecRule REQBODY_ERROR "!@eq 0" \
      "id:200002,phase:2,t:none,deny,status:400,log,msg:'Failed to parse request body.',\
    logdata:'%{reqbody_error_msg}',severity:2"

    SecRule MULTIPART_STRICT_ERROR "!@eq 0" \
    "id:200003,phase:2,t:none,log,deny,status:403, \
    msg:'Multipart request body failed strict validation: \
    PE %{REQBODY_PROCESSOR_ERROR}, \
    BQ %{MULTIPART_BOUNDARY_QUOTED}, \
    BW %{MULTIPART_BOUNDARY_WHITESPACE}, \
    DB %{MULTIPART_DATA_BEFORE}, \
    DA %{MULTIPART_DATA_AFTER}, \
    HF %{MULTIPART_HEADER_FOLDING}, \
    LF %{MULTIPART_LF_LINE}, \
    SM %{MULTIPART_MISSING_SEMICOLON}, \
    IQ %{MULTIPART_INVALID_QUOTING}, \
    IP %{MULTIPART_INVALID_PART}, \
    IH %{MULTIPART_INVALID_HEADER_FOLDING}, \
    FL %{MULTIPART_FILE_LIMIT_EXCEEDED}'"

    SecRule TX:/^MSC_/ "!@streq 0" \
      "id:200005,phase:2,t:none,deny,status:500,\
      msg:'ModSecurity internal error flagged: %{MATCHED_VAR_NAME}'"


    # === ModSec Core Rule Set Base Configuration (ids: 900000-900999)

    Include    modsecurity.d/crs/crs-setup.conf

    SecAction "id:900110,phase:1,pass,nolog,\
      setvar:tx.inbound_anomaly_score_threshold=5,\
      setvar:tx.outbound_anomaly_score_threshold=4"

    SecAction "id:900000,phase:1,pass,nolog,\
      setvar:tx.paranoia_level=1"


    # === ModSec Core Rule Set: Runtime Exclusion Rules (ids: 10000-49999)

    # ...


    # === ModSecurity Core Rule Set Inclusion

    Include    modsecurity.d/crs/rules/*.conf


    # === ModSec Core Rule Set: Startup Time Rules Exclusions

    # Disables 403 status code after login into the application
    SecRuleRemoveById 920420


    # === ModSec timestamps at the end of each phase (ids: 90010 - 90019)

    SecAction "id:90010,phase:1,pass,nolog,setvar:TX.ModSecTimestamp1end=%{DURATION}"
    SecAction "id:90011,phase:2,pass,nolog,setvar:TX.ModSecTimestamp2end=%{DURATION}"
    SecAction "id:90012,phase:3,pass,nolog,setvar:TX.ModSecTimestamp3end=%{DURATION}"
    SecAction "id:90013,phase:4,pass,nolog,setvar:TX.ModSecTimestamp4end=%{DURATION}"
    SecAction "id:90014,phase:5,pass,nolog,setvar:TX.ModSecTimestamp5end=%{DURATION}"


    # === ModSec performance calculations and variable export (ids: 90100 - 90199)

    SecAction "id:90100,phase:5,pass,nolog,\
      setvar:TX.perf_modsecinbound=%{PERF_PHASE1},\
      setvar:TX.perf_modsecinbound=+%{PERF_PHASE2},\
      setvar:TX.perf_application=%{TX.ModSecTimestamp3start},\
      setvar:TX.perf_application=-%{TX.ModSecTimestamp2end},\
      setvar:TX.perf_modsecoutbound=%{PERF_PHASE3},\
      setvar:TX.perf_modsecoutbound=+%{PERF_PHASE4},\
      setenv:ModSecTimeIn=%{TX.perf_modsecinbound},\
      setenv:ApplicationTime=%{TX.perf_application},\
      setenv:ModSecTimeOut=%{TX.perf_modsecoutbound},\
      setenv:ModSecAnomalyScoreInPLs=%{tx.anomaly_score_pl1}-%{tx.anomaly_score_pl2}-%{tx.anomaly_score_pl3}-%{tx.anomaly_score_pl4},\
      setenv:ModSecAnomalyScoreOutPLs=%{tx.outbound_anomaly_score_pl1}-%{tx.outbound_anomaly_score_pl2}-%{tx.outbound_anomaly_score_pl3}-%{tx.outbound_anomaly_score_pl4},\
      setenv:ModSecAnomalyScoreIn=%{TX.anomaly_score},\
      setenv:ModSecAnomalyScoreOut=%{TX.outbound_anomaly_score}"
</IfModule>
```

### Matomo Realtime Tracking

```
# Matomo Realtime Logging
LogFormat "%v %h %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-agent}i\"" matomo
CustomLog "||/usr/local/sbin/import_logs.py \
--debug --enable-http-errors --enable-http-redirects --enable-bots \
--url=https://analytics.example.com --output=/var/log/matomo.log --recorders=1 \
--recorder-max-payload-size=1 --log-format-name=common_complete --token-auth=2ac48e93-2ca7-4df3-9e7c-c81b36d0a474 \
-" matomo
```

### GELF Realtime Tracking

```
# GELF Realtime Logging
CustomLog "|/usr/bin/nc --udp graylog.example.com 12201" gelf
```
