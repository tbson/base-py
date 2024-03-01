# BASE PROJECT

## Minimum dependencies
Only use really needed one

*Dependencies*

- `antd`: All in one enterprise UI kit
- `axios`: For HTTP request. We can use `fetch` but most of us familiar with axios
- `date-fns`: For Ant Design date picker and date/time utilities
- `ramda`: general-purpose tookit, currently use for cloning objects only
- `react`: No comment,
- `react-dom`: No comment,
- `react-router-dom`: For routing on client side,
- `recoil`: Store global state the React way,
- `ttag`: For multiple language

*Dev Dependencies*
- `@vitejs/plugin-react`: Vite plugin for react development,
- `vitest`: For unit testing,
- `ttag-cli`: CLI for ttag use for generating, updating, exporting gettext files
- `vite`: Frontend tooling, fast build and hot reloading

## Features

- JSDoc support
- Build in dashboard
- Use React hooks for most of taks
- Recoil help to deal with global state if needed.
- Multiple language support. `PoEdit` and `fmakemessages`/`fdumpmessages` do all managing tasks.
- Ready for customizing theme (Ant Design)
- Unit test support
- Abstract away HTTP request operations

# Install

**Step 1**: Prepare configuration files:

```
cp docker/conf.d/default.conf.default docker/conf.d/default.conf
cp docker/.env.default docker/.env
```

**Step 2**: Add `basecode.test` domain to `hosts` file (`/etc/hosts` on Mac/Linux) by append this line at file's bottom:

```
127.0.0.1       basecode.test
```

**Step 3**: Install root CA at `docker/ssl/localca.pem`: [tutorial](https://support.securly.com/hc/en-us/articles/206058318-How-to-install-the-Securly-SSL-certificate-on-Mac-OSX-)


**Step 4**: Build docker

```
cd docker
./exec build
```

**Step 5**: Run one-time setup

```
./exec manage.py migrate
./exec manage.py collectstatic
./exec manage.py account_seeding_users
```

**Step 6**: Run backend and frontend server at separated terminal tab

```
./exec bserver
./exec fserver
```

Then visit:

API docs: `https://basecode.test/api/v1/docs`

Front end: `https://basecode.test`

Username/password: `admin@localhost`/`<SAMPLE_PASSWORD in .env>`

Django admin page: `https://basecode.test/admin`

Username/password: `admin@localhost`/`<SAMPLE_PASSWORD in .env>`


# Other utilities

Run unit test

```
./exec btest
```

Build translation for backend


```
./exec manage.py makemessages --all
```

Build translation for frontend


```
./exec fmakemessages
```

Apply translation for frontend


```
./exec fdumpmessages
```
