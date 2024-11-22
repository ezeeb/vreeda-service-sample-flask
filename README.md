## Install Dependencies

- [nodejs](https://nodejs.org/)
- [yarn](https://yarnpkg.com/): `$ npm install --global yarn`
- [docker](https://www.docker.com/products/docker-desktop/)
- [python](https://www.python.org/)


And then install dependencies for the frontend with yarn:

```bash
$ yarn install
```

And then install dependencies for the backend:

```bash
$ cd api
$ ./install.sh
```

## Configuration

You have to create a `api/.env` with the following entries

```
FLASK_ENV=development
FLASK_SECRET_KEY=<create this with openssl rand -hex 32>
HOST_URL="https://localhost:3000"
AZURE_AD_B2C_CLIENT_ID=<ask for client id at vreeda>
AZURE_AD_B2C_CLIENT_SECRET=<ask for client secret at vreeda>
AZURE_AD_B2C_TENANT_NAME="vreedaid"
AZURE_AD_B2C_PRIMARY_USER_FLOW="B2C_1A_VREELI_SERVICE_SIGNIN_PROD"
VREEDA_API_BASEURL="https://client-rest.api.vreeda.com"
MONGODB_URI="mongodb://root:example@localhost:27017/vreeda?authSource=admin"
API_REFRESH_TOKENS_JOB_KEY=your-secure-key
```

## Getting Started With Development

First, start the backend development server:

```bash
$ cd api
$ ./start.sh
```

Then, run the frontend development server in parallel:

```bash
yarn start
```

Open [https://localhost:3000](https://localhost:3000) with your browser to see the result.

This project uses [Flask](https://flask.palletsprojects.com/en/stable/) for the backend and [React](https://react.dev/) in combination with [React Material UI](https://mui.com/material-ui/getting-started/) for the frontend.

You can start editing the frontend by modifying `src/pages/Home.tsx`. The page auto-updates as you edit the file.

You can extend the backend logic in the `api` folder and subfolders. The backend auto-updates as you edit files. 

The backend contains the basic functionality to implement a vreeda service:

- authentication and authorization based on vreeda id management in `/api/routes/auth`
- user configuration and device access token management in `/api/routes/user`
- basic VREEDA api client in `/api/routes/vreeda`
- externally triggered background jobs in `/api/routes/jobs` 

## Learn More

To learn more about the VREEDA platform, take a look at the following resources:

- [VREEDA API Documentation](https://api.vreeda.com/)
