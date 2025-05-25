# Frontend Dockerfile
FROM node:18

WORKDIR /app

# Install dependencies
COPY ui/package.json ui/package-lock.json* ./
RUN npm install

# Copy frontend code
COPY ui/ .

# Expose React default port
EXPOSE 3000

CMD ["npm", "start"]
