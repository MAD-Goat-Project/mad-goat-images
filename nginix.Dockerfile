FROM nginx:1.10.3-alpine

# Start Nginx when the container launches
CMD ["nginx", "-g", "daemon off;"]
