# Step 1: Use an official Node.js runtime as the base image
FROM node:18-alpine AS build

# Step 2: Set the working directory inside the container
WORKDIR /app

# Step 3: Copy the package.json and package-lock.json files first to install dependencies
COPY /pharmaco-frontend/package*.json /app

# Step 4: Install dependencies
RUN npm install --force

# Step 5: Copy the rest of the app's source code
COPY /pharmaco-frontend /app

# Step 6: Build the Vue app for production
RUN npm run build

# Step 7: Use a new lightweight image to serve the app
FROM node:18-alpine

# Install the 'serve' package globally to serve the built files
RUN npm install -g serve

# Set the working directory to hold the build files
WORKDIR /app

# Copy the build output from the previous stage to the current stage
COPY --from=build /app/dist /app

# Step 8: Expose the port on which the app will run
EXPOSE 30444

# Step 9: Command to run the app using 'serve'
CMD ["serve", "-s", "/app", "-l", "30444"]
