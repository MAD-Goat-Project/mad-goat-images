FROM nginx:1.13.1-alpine

# Start Nginx when the container launches
CMD ["nginx", "-g", "daemon off;"]
