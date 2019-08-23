FROM ubuntu:16.04

ENV APP_VERSION=1.6.39
# Let the container know that there is no tty
ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update -y -qq; apt-get install --no-install-recommends -y -qq build-essential \
    sudo php-dev libmcrypt-dev php-pear supervisor curl cron nodejs software-properties-common; \
    LC_ALL=C.UTF-8 add-apt-repository ppa:ondrej/php -y; apt-get update -y -qq; \
    apt-get install --no-install-recommends -y php7.1-apcu php7.1-bcmath php7.1-cli php7.1-mbstring php-tidy \
    php7.1-curl php7.1-fpm php7.1-gd php7.1-intl php7.1-mysql php7.1-soap php7.1-mcrypt \
    php7.1-xml php7.1-zip php7.1-imagick libfreetype6-dev libmcrypt-dev libpng-dev \
    && apt-get clean; apt-get autoclean; apt-get autoremove -y -qq; \
    groupadd -r -g 2000 orocommerce; useradd -r -u 2000 -g 2000 -m -c "app account" -d /home/orocommerce -s /bin/bash orocommerce;

RUN curl -o /usr/src/app.tar.gz -L https://github.com/oroinc/orocommerce-application/releases/download/${APP_VERSION}/orocommerce-application-${APP_VERSION}.tar.gz
ADD ./configs/php/cli/php.ini /etc/php/7.1/cli/php.ini
ADD ./configs/php/fpm/php.ini /etc/php/7.1/fpm/php.ini
ADD ./configs/php/www.conf /etc/php/7.1/fpm/pool.d/www.conf
ADD configs/supervisord/orocommerce.conf /etc/supervisor/conf.d/orocommerce.conf

RUN curl -sS https://getcomposer.org/installer | php && mv composer.phar /usr/local/bin/composer
USER orocommerce
ENV HOME /home/orocommerce
WORKDIR /home/orocommerce
RUN chown -R orocommerce:orocommerce .
RUN tar -xzf /usr/src/app.tar.gz && mv orocommerce-application ./src
WORKDIR /home/orocommerce/src
RUN composer install

USER root
RUN touch /var/log/php7.1-fpm.log && mkdir -p /run/php/
RUN chown orocommerce.orocommerce /var/log/php7.1-fpm.log && chown orocommerce. /run/php
