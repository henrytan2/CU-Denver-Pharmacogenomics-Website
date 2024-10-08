# Use the official Nginx image as the base image
FROM nginx:latest

# Copy custom configuration file
# (Uncomment the next line if you have a custom nginx.conf)
# COPY nginx.conf /etc/nginx/nginx.conf

# Copy custom content (if any)
# (Uncomment the next line if you have custom content to serve)
# COPY ./content /usr/share/nginx/html

# Expose port 80
EXPOSE 80

# Start Nginx when the container launches
CMD ["nginx", "-g", "daemon off;"]