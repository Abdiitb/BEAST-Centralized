# Use official Nginx image
FROM nginx:alpine

# Copy custom Nginx configuration file
COPY nginx.conf /etc/nginx/nginx.conf

# Expose the port for Nginx
EXPOSE 80

# Set environment variable to determine if running in dev or prod
ENV ENV_MODE=prod

# If ENV_MODE is prod, run Nginx. If ENV_MODE is dev, stop the container by exiting.
CMD ["sh", "-c", "if [ \"$ENV_MODE\" = \"prod\" ]; then nginx -g 'daemon off;'; else exit 0; fi"]