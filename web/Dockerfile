FROM node:18.17.0-alpine

WORKDIR /app

# Install build dependencies
RUN apk add --no-cache python3 make g++

# Copy package files
COPY package*.json ./

# Clean install dependencies with specific esbuild version
RUN rm -rf node_modules package-lock.json && \
    npm cache clean --force && \
    npm install esbuild@0.19.12 --save-dev && \
    npm install && \
    npm install vite@4.4.9 --save-dev

# Copy the rest of the application
COPY . .

# Expose the port
EXPOSE 5173

# Set environment variables
ENV HOST=0.0.0.0
ENV VITE_HOST=0.0.0.0
ENV NODE_ENV=development

# Start the development server
CMD ["npm", "run", "dev"]
