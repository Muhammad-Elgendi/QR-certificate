<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="https://github.com/Muhammad-Elgendi/QR-certificate">
    <img src="favicon.png" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">QR-certificate</h3>

  <p align="center">
    Simple django web application to manage certificates and their verifications with QR codes.
    <br />
    <a href="https://github.com/Muhammad-Elgendi/QR-certificate"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/Muhammad-Elgendi/QR-certificate">View Demo</a>
    ·
    <a href="https://github.com/Muhammad-Elgendi/QR-certificate/issues">Report Bug</a>
    ·
    <a href="https://github.com/Muhammad-Elgendi/QR-certificate/issues">Request Feature</a>
  </p>
</p>



<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary><h2 style="display: inline-block">Table of Contents</h2></summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgements">Acknowledgements</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project
Simple django web application to manage certificates and their verifications with QR codes.

### Built With

* [Django](https://www.djangoproject.com/)
* [Docker](https://www.docker.com/)


<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these simple steps.

### Prerequisites

Install docker engine and docker compose.
* Docker engine
  ```
  https://docs.docker.com/engine/install/
  ```
* Docker compose
  ```
  https://docs.docker.com/compose/install/
  ```
### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/Muhammad-Elgendi/QR-certificate.git
   ```
2. Go to qrcertificate directory
   ```sh
   cd qrcertificate
   ```
3. Create your own .env files by copying .env.example
   ```sh
   cp .env.example .env.dev
   cp .env.example .env.prod
   ```
4. Go to docker directory
   ```sh
   cd qrcertificate/docker
   ```
5. Create your own .env file for docker compose by copying .env.example
   ```sh
   cp .env.example .env
   ```
6. Create and start all the containers
   ```sh
   docker-compose up
   ```
7. Generate a new security key

8. Creating a New Administrator Account
    ```sh
   docker-compose exec web bash
   python manage.py createsuperuser
   ```
9. Fill out your credentials

10. Open a new browser tab and Visit localhost




<!-- Use Cases -->
## Use Cases

QR-certificate could be used for different use cases, here are some examples:

1. Verification of generated certificates
2. Export certificates in PDF

Additional screenshots, screencasts, and more resources will be soon.

<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request



<!-- LICENSE -->
## License

Distributed under the GPL-3.0 license. See `LICENSE` for more information.



<!-- CONTACT -->
## Contact

Muhammad Elgendi- [@gendidev](https://twitter.com/@gendidev)

Project Link: [https://github.com/Muhammad-Elgendi/QR-certificate](https://github.com/Muhammad-Elgendi/QR-certificate)
