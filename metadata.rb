name 'pet_cookbook'
maintainer 'The Authors'
maintainer_email 'you@example.com'
license 'All Rights Reserved'
description 'Installs/Configures pet_cookbook'
long_description 'Installs/Configures pet_cookbook'
version '0.1.0'
chef_version '>= 12.1' if respond_to?(:chef_version)
issues_url 'https://github.com/pdv1703/Registration_card_GUI'
source_url 'https://github.com/pdv1703/Registration_card_GUI'
supports 'centos7.3'

depends 'mariadb', '~> 1.5.3'
depends 'swap', '~> 2.1.0'
