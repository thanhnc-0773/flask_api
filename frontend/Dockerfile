# Use Node.js 20.11.0 image
FROM node:20.11.0

# Set working directory
WORKDIR /app

# Copy package.json and lock files
COPY package.json package-lock.json ./

# Install dependencies
RUN npm ci

# Copy all frontend files
COPY . .

# Build the React app
RUN npm run build

# Install Serve to serve the built app
RUN npm install -g serve

# Command to run the app
CMD ["serve", "-s", "build"]

# Expose the port React app runs on
EXPOSE 3000
