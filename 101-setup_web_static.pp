package { 'nginx':
  ensure => installed,
}

file { [
  '/data/web_static/releases/test',
  '/data/web_static/shared',
]:
  ensure => directory,
  owner  => 'ubuntu',
  group  => 'ubuntu',
  mode   => '0755',
}

file { '/data/web_static/releases/test/index.html':
  content => 'Test test 1, 2, 3',
  mode    => '0644',
  owner   => 'ubuntu',
  group   => 'ubuntu',
}

file { '/data/web_static/current':
  ensure => 'link',
  target => '/data/web_static/releases/test',
  owner  => 'ubuntu',
  group  => 'ubuntu',
  force  => true,
}

file { '/etc/nginx/sites-available/default':
  content => "
    server {
      listen 80 default_server;
      listen [::]:80 default_server;
      add_header X-Served-By $HOSTNAME;
      root   /var/www/html;
      index  index.html index.htm;

      location /hbnb_static {
        alias /data/web_static/current;
        index index.html index.htm;
      }

      location /redirect_me {
        return 301 http://my80stv.com;
      }

      error_page 404 /404.html;
      location /404 {
        root /var/www/html;
        internal;
      }
    }
  ",
  mode    => '0644',
  require => Package['nginx'],
}

service { 'nginx':
  ensure  => 'running',
  enable  => true,
  require => File['/etc/nginx/sites-available/default'],
}
