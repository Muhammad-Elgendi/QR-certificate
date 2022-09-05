FROM nginx:1.19.0-alpine

RUN mkdir -p /usr/src/app/public
RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d/
