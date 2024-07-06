{
  "mainImports": "github.com/gofiber/storage/postgres/v3",
  "dependenciesLink": "go get github.com/gofiber/storage/postgres/v3",
  "appConfig": "store := postgres.New(postgres.Config{\\n\\tDB:\\tdbPool,\\n\\tTable:\\t\\\"fiber_storage\\\",\\n\\tReset:\\tfalse\\n})",
  "reference": "https://docs.gofiber.io/storage/postgres/",
  "description": "PostgreSQL storage for Fiber that provides a simple way to store data in PostgreSQL."
}

| Variable name | Purpose                                       |
| ------------- | --------------------------------------------- |
| projectName   | project name                                  |
| mainImports   | imports in main file                          |
| appConfig     | app config in main file before the app is run |
| dependencies  | dependencies used by poetry                   |
| readme        | readme documentation variable                 |
