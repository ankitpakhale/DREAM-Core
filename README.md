# DREAM – Dynamic Realization Engine for Achieving Milestones

**DREAM** is a powerful, AI-driven platform designed to help users achieve their personal milestones by generating customized life plans, routines, and habits. The system is divided into multiple components:

-   **DREAM-Core**: The scalable **backend** responsible for handling AI-driven content generation, validations, dynamic routing, and more.

-   **DREAM-UI**: The **frontend UI** that provides an interactive, user-friendly interface for users to engage with their personalized plans. You can find the frontend repository here: [DREAM-UI](https://github.com/ankitpakhale/DREAM-UI).


These components work together to offer a seamless, integrated **full-stack application** for personal goal achievement.

----------

## DREAM-Core – The Scalable Backend

**DREAM-Core** is the backend component of **DREAM** that handles all server-side operations. It is designed to interact with large language models (LLMs), like GroqAI, to generate personalized routines, habits, and dream life plans for users. **DREAM-Core** is built to scale and is equipped with dynamic routing, validation, and comprehensive logging.

## Features

-   **Dynamic Route Management**: Automatically loads and registers routes using the `RouteManager`.

-   **AI-Powered Content Generation**: Uses GroqAI to generate tailored life plans, routines, and habits based on user input.

-   **Flexible Configuration**: Easily configurable for various environments.

-   **Content Validation**: Ensures that generated content adheres to validation standards.

-   **Scalable Architecture**: Designed to handle increasing user load and evolving requirements.

-   **Custom Logging & Retry Mechanism**: Includes custom logging and a retry system to ensure reliability in case of failures.


## Project Structure

```
DREAM
├── app
│   ├── clients
│   │   ├── groqai_client.py
│   │   └── __init__.py
│   ├── config
│   │   ├── base_config.py
│   │   ├── general_config.py
│   │   ├── groqai_config.py
│   │   └── __init__.py
│   ├── framework
│   │   ├── fastapi_app.py
│   │   └── __init__.py
│   ├── main.py
│   ├── prompts
│   │   ├── __init__.py
│   │   ├── prompt_factory.py
│   │   └── prompt_map.py
│   ├── routes
│   │   ├── route_dream_life.py
│   │   ├── route_healthcheck.py
│   │   └── route_manager.py
│   ├── schema
│   │   ├── daily_habits_schema.json
│   │   ├── fears_and_motivation_schema.json
│   │   └── routine_schema.json
│   ├── services
│   │   ├── dream_life_generation_service.py
│   │   ├── generators
│   │   │   ├── base_generator.py
│   │   │   ├── daily_habit_generator.py
│   │   │   ├── fear_and_motivation_generator.py
│   │   │   ├── __init__.py
│   │   │   └── routine_generator.py
│   │   ├── __init__.py
│   │   └── validation_manager
│   │       ├── __init__.py
│   │       ├── schema_map.py
│   │       ├── strategy
│   │       │   ├── base_strategy.py
│   │       │   ├── daily_habit_generator_data.py
│   │       │   ├── fear_and_motivation_generator_data.py
│   │       │   ├── __init__.py
│   │       │   ├── routine_generator_data.py
│   │       │   └── user_form_data.py
│   │       └── validation_manager.py
│   └── utils
│       ├── constants.py
│       ├── id_generator.py
│       ├── __init__.py
│       ├── logging
│       │   ├── base.py
│       │   ├── filters.py
│       │   ├── formatters.py
│       │   ├── handlers.py
│       │   └── __init__.py
│       ├── response_manager
│       │   ├── __init__.py
│       │   └── response_manager.py
│       └── retry.py
├── CODEOWNERS
├── cookbook
│   └── version1
│       └── index.md
├── entrypoint.sh
├── LICENSE
├── postman_collection
│   └── collection.json
├── pyproject.toml
├── README.md
├── release
└── requirements.txt

```

## Setup

Follow these steps to set up **DREAM-Core** on your local environment.

### Prerequisites

-   Python 3.10+

-   GroqAI API credentials (needed for interacting with the LLM)

-   `pip` for installing Python dependencies


### Installation

1.  Clone the repository:

    ```bash
    git clone https://github.com/ankitpakhale/DREAM-Core.git
    cd DREAM-Core
    ```

2.  Create a virtual environment:

    ```bash
    python3 -m venv .venv
    source .venv/bin/activate  # On Windows: .venv\Scripts\activate

    ```

3.  Install dependencies:

    ```bash
    pip install -r requirements.txt

    ```

4.  Copy the example environment file to `.env`:

    ```bash
    cp .env_example .env

    ```

5.  Add your GroqAI API credentials and any necessary environment variables to the `.env` file.

6.  Start the backend server:

    ```bash
    ./entrypoint.sh

    ```


## Configuration

The backend configuration files are located in the `config/` directory:

-   **BaseConfig.py**: Contains general configuration settings for the backend.

-   **GeneralConfig.py**: General settings for the system.

-   **GroqAIConfig.py**: Settings for connecting to GroqAI, including API keys.


## API Endpoints

The backend exposes several important endpoints:

-   **/dreamlife**: Generates a personalized dream life plan.

-   **/healthcheck**: Ensures the backend server is running and functional.  

These routes are dynamically managed by the `RouteManager`.

## Validation

**DREAM-Core** includes a robust validation layer to ensure the integrity of generated content:

-   **ValidationManager**: Ensures that generated content adheres to the required format and structure.

-   **_validate method**: Used in the generator classes to verify the output from GroqAI.

-   **PydanticOutputParser**: Parses and validates responses from the LLM.


## Logging & Retry Mechanism

-   **custom_logging.py**: Provides logging for various backend events.

-   **retry_mechanism.py**: Implements retry logic for external requests to services like GroqAI in case of failure.


## Postman Collection

A **Postman collection** is available in the `postman_collection/` directory. This collection contains pre-configured API requests that you can import into Postman to test the backend API endpoints.

## Contributing

We welcome contributions to **DREAM-Core**! If you'd like to contribute, please follow these steps:

1.  Fork the repository.

2.  Create a new branch (`git checkout -b feature-branch`).

3.  Make your changes and commit them (`git commit -am 'Add new feature'`).

4.  Push to the branch (`git push origin feature-branch`).

5.  Open a pull request to contribute your changes.


## License

This project is licensed under a **custom, strictly restricted license**.

- **Use, copying, modification, distribution, and deployment are all prohibited.**
- This includes personal, educational, and commercial purposes.
- You may only view the code. No other actions are allowed.

See [LICENSE.md](./LICENSE.md) for full terms.
