# Project-Scaffolder

An open source web application to assist developers of all levels of expertise ( spring initializr on steroids ).

* User friendly interface for ease of use.
* Automates and streamlines project initiation tasks.
* Recommends technologies based on user requirements.
* Provides fully configured repository with version control.

## Features

Select your desired development stack and jump right to coding your business logic, with your favourite dependencied already configured. And with an impressive README file auto generated for you specific development stack.

Can also auto create your github repo if you provide us a github api key.

## Contribution

As an open source project, community support is essential. The community can contribute with either dependencies and their configuration to a specific framework, or contribute with a whole new framework.

Contributions must follow a specific specification to comply with our backend.

### Framework

ALL IN J2 FORMAT

- Backend frameworks use a default endpoint for the user to ping and see if the application is running properly `localhost:<port>/health`
- Must include a readme file indicating all the used variables in the template and their purpose ( a description and reference variables are required ).
- A extensive readme file must be provided detailing how to run and how to install new dependencies.
- A Docker file must be provided.

### Dependency

ALL IN JSON FORMAT

* All variables that are used in the dependency and not found in the template or the readme file of the framework must be added.
* All dependencies that require additinal files or code must provide then as variables inside the J2 file.

## Team members

- [Youssef Ahmad Abdulghafar](https://github.com/greatyassoo)
- [Mostafa Hesham Allam](https://github.com/MainUseless)
- [Karim Amr Hamdy](https://github.com/Kemol001)
- [Fares Karim El Kholy](https://github.com/HunterElite0)
- [Youssef Hussein Wahba ](https://github.com/Youssef-Wahba)
