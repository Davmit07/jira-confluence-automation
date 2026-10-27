# Vehicle Shop API

The initial API scaffold exposes a local health check only. It does not connect to
Jira, PostgreSQL, a browser runner, or other external services.

From `work/module03-task`, install dependencies and start the API:

```sh
npm --prefix apps/api install
npm --prefix apps/api start
```

The server listens only on `127.0.0.1:3000`. To change the port, set `PORT` to an
integer from 1 through 65535. The host is intentionally fixed to loopback.

Check the endpoint:

```sh
curl -i http://127.0.0.1:3000/health
```

Expected response: HTTP `200` with `{"status":"ok"}`.

Run the isolated endpoint test:

```sh
npm --prefix apps/api test
```
