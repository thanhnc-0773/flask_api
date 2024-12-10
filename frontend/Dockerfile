FROM node:20.11.0

# Set working directory
WORKDIR /app

# Copy package.json and lock files
COPY package.json package-lock.json ./

# Install dependencies
RUN npm ci

# Copy all frontend files
COPY . .

# Use development server for hot reload
CMD ["npm", "start"]

# Expose the port
EXPOSE 3000
