# Script that redoes task 0 (sets up your web servers for the deployment of web_static)
# Configures a web server for deployment of web_static.
exec { '/usr/bin/env apt -y update' : }

package { 'nginx':
  ensure   => 'present',
  provider => 'apt'
} ->

file { '/data':
  ensure  => 'directory'
} ->

file { '/data/web_static':
  ensure => 'directory'
} ->

file { '/data/web_static/releases':
  ensure => 'directory'
} ->

file { '/data/web_static/releases/test':
  ensure => 'directory'
} ->

file { '/data/web_static/shared':
  ensure => 'directory'
} ->

file { '/data/web_static/releases/test/index.html':
  ensure  => 'present',
  content => "Alx School Puppet\n"
} ->

file { '/data/web_static/current':
  ensure => 'link',
  target => '/data/web_static/releases/test'
} ->

exec { 'chown -R ubuntu:ubuntu /data/':
  path => '/usr/bin/:/usr/local/bin/:/bin/'
}

file { '/var/www':
  ensure => 'directory'
} ->

file { '/var/www/html':
  ensure => 'directory'
} ->

file { '/var/www/html/index.html':
  ensure  => 'present',
  content => "Alx School Nginx\n"
} ->

file { '/var/www/html/404.html':
  ensure  => 'present',
  content => "Ceci n'est pas une page\n"
} ->

file { '/etc/nginx/sites-available/default':
  ensure  => present,
  mode    => '0644',
  content =>
"server {
	listen 80 default_server;
	listen [::]:80 default_server;
	server_name _;
	index index.html index.htm;
	error_page 404 /404.html;
	add_header X-Served-By \$hostname;
	location / {
		root /var/www/html/;
		try_files \$uri \$uri/ =404;
	}
	location /hbnb_static/ {
		alias /data/web_static/current/;
	}
	if (\$request_filename ~ redirect_me){
		rewrite ^ https://github.com/Mouadnait permanent;
	}
	location = /404.html {
		root /var/www/error/;
		internal;
	}
}",
  require => [
    Package['nginx'],
    File['/var/www/html/index.html'],
    File['/var/www/error/404.html'],
    Exec['change-data-owner']
  ],
} ->

exec { 'enable-site':
  command => "ln -sf '/etc/nginx/sites-available/default' '/etc/nginx/sites-enabled/default'",
  path    => '/usr/bin:/usr/sbin:/bin',
  require => File['/etc/nginx/sites-available/default'],
}

exec { 'start-nginx':
  command => 'sudo service nginx restart',
  path    => '/usr/bin:/usr/sbin:/bin',
  require => [
    Exec['enable-site'],
    Package['nginx'],
    File['/data/web_static/releases/test/index.html'],
  ],
}

Exec['start-nginx']
