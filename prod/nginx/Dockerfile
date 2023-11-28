# Production environment
FROM nginx:1.16.0-alpine
RUN rm /etc/nginx/conf.d/default.conf
COPY ./prod/nginx/nginx.conf.template /nginx.conf.template
COPY ./prod/nginx/entrypoint.sh /entrypoint.sh
EXPOSE 80

ENTRYPOINT [ "/entrypoint.sh" ]

CMD ["nginx", "-g", "daemon off;"]
