- Make sure to first install the CLI for GO
- After installing navigate to the root directory and run the app using ``go run main.go``
- If you need to install any extra dependencies use ``go get <dependency-url>``

## Template structure

### ./app

**Folder with business logic only**. This directory doesn't care about _what database driver you're using_ or _which caching solution your choose_ or any third-party things.

- `./app/controllers` folder for functional controllers (used in routes)
- `./app/models` folder for describe business models and methods of your project

### ./pkg

**Folder with project-specific functionality**. This directory contains all the project-specific code tailored only for your business use case, like _middleware_, _routes_ or _utils_.

- `./pkg/middleware` folder for add middleware (Fiber built-in and yours)
- `./pkg/routes` folder for describe routes of your project
- `./pkg/utils` folder with utility functions (server starter, error checker, etc)
