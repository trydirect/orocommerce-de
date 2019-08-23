FROM ubuntu:18.04

ENV APP_VERSION=1.6.39
# Let the container know that there is no tty
ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update -y -qq; apt-get install --no-install-recommends -y -qq build-essential \
    sudo php-dev libmcrypt-dev php-pear supervisor curl cron nodejs software-properties-common; \
    LC_ALL=C.UTF-8 add-apt-repository ppa:ondrej/php -y; apt-get update -y -qq; \
    apt-get install --no-install-recommends -y php7.2-apcu php7.2-bcmath php7.2-cli php7.2-mbstring php-tidy \
    php7.2-curl php7.2-fpm php7.2-gd php7.2-intl php7.2-mysql php7.2-soap \
    php7.2-xml php7.2-zip php7.2-imagick libfreetype6-dev libmcrypt-dev libpng-dev \
    && apt-get clean; apt-get autoclean; apt-get autoremove -y -qq; \
    groupadd -r -g 2000 orocommerce; useradd -r -u 2000 -g 2000 -m -c "app account" -d /home/orocommerce -s /bin/bash orocommerce;

RUN pecl channel-update pecl.php.net && pecl install mcrypt-1.0.2
RUN curl -o /usr/src/app.tar.gz -L https://github.com/oroinc/orocommerce-application/releases/download/${APP_VERSION}/orocommerce-application-${APP_VERSION}.tar.gz
ADD ./configs/php/cli/php.ini /etc/php/7.2/cli/php.ini
ADD ./configs/php/fpm/php.ini /etc/php/7.2/fpm/php.ini
RUN echo "extension=mcrypt.so" >> /etc/php/7.2/fpm/php.ini
RUN echo "extension=mcrypt.so" >> /etc/php/7.2/cli/php.ini
ADD ./configs/php/www.conf /etc/php/7.2/fpm/pool.d/www.conf
ADD configs/supervisord/orocommerce.conf /etc/supervisor/conf.d/orocommerce.conf

RUN curl -sS https://getcomposer.org/installer | php && mv composer.phar /usr/local/bin/composer
USER orocommerce
ENV HOME /home/orocommerce
WORKDIR /home/orocommerce
RUN chown -R orocommerce:orocommerce .
RUN tar -xzf /usr/src/app.tar.gz && mv orocommerce-application ./src
WORKDIR /home/orocommerce/src
ADD ./configs/orocommerce/composer.json .
RUN composer install

USER root
RUN touch /var/log/php7.2-fpm.log && mkdir -p /run/php/
RUN chown orocommerce.orocommerce /var/log/php7.2-fpm.log && chown orocommerce. /run/php
