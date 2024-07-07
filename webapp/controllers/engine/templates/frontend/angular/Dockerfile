FROM node:20.15.0-alpine AS build

WORKDIR /app

COPY package*.json ./

RUN npm install

COPY . .

RUN npm run build

FROM nginx:alpine 

# COPY nginx.conf /etc/nginx/nginx.conf

# replace `frontend-angular` with the actual name of your Angular application's build directory
COPY --from=build /app/dist/frontend-angular/browser /usr/share/nginx/html

EXPOSE 80

# Start the server
CMD ["nginx", "-g", "daemon off;"]
