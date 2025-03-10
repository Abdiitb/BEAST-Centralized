# Base Stage: Use Node.js for both development and production
FROM node:20.0.0 AS base

# Set the working directory
WORKDIR /frontend

# Copy package.json and package-lock.json for dependency installation
COPY package.json package-lock.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application code
COPY . .

# Build Stage: Create production assets
FROM base AS build
RUN npm run build

# Final Stage: Serve with NGINX for production or start the dev server
FROM nginx:alpine AS final

# Set environment variable to determine if running in dev or prod
ENV ENV_MODE=prod

# For production, copy the build output to NGINX's html directory
COPY --from=build /frontend/build /usr/share/nginx/html

# For development, keep Node.js runtime in the base image
COPY --from=base /frontend /frontend

# Install Node.js and npm in the final image if running in dev mode
RUN apk add --no-cache nodejs npm

# Expose port for both development (3000) and production (80)
EXPOSE 80 3000

# Command to switch between dev and prod mode
CMD ["sh", "-c", "if [ \"$ENV_MODE\" = \"dev\" ]; then cd /frontend && npm start; else nginx -g 'daemon off;'; fi"]
