FROM node:18.17.0

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies and explicitly install axios
RUN npm install && \
    npm install axios && \
    ls -la node_modules/axios && \
    npm list axios

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
