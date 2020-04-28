<IfDefine !IS_DJANGOSTACK_LOADED>
      Define IS_DJANGOSTACK_LOADED
      WSGIDaemonProcess wsgi-djangostack   processes=2 threads=15    display-name=%{GROUP}
</IfDefine>

<Directory "/opt/bitnami/apps/django/django_projects/kaucu/kaucudjango">
    Options +MultiViews
    AllowOverride All
    <IfVersion >= 2.3>
        Require all granted
    </IfVersion>

    WSGIProcessGroup wsgi-djangostack

    WSGIApplicationGroup %{GLOBAL}
</Directory>

WSGIScriptAlias /kaucu '/opt/bitnami/apps/django/django_projects/kaucu/kaucudjango/wsgi.py'