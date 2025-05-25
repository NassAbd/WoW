FROM node:18

WORKDIR /app

COPY ui/package.json ui/package-lock.json* ./
RUN npm install

COPY ui/ .

EXPOSE 3000

CMD ["npm", "start"]
