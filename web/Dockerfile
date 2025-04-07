FROM node:18.17.0

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm install

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
