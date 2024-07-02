# Multiagent System (MAS) LLM Newsletter

Welcome to the Aquarius! This project leverages a network of agents to dynamically create and distribute newsletters via SMTP or messaging platforms. Target is to provide automatic updated information about the latest news in a certain industry / trend.

**Target Users**:
- Tech or business users that are interested in a specific domain
- Tech leads who need to keep up to speed on rapid tech development landscape
- Hobbyists who wants to learn about a certain topic in depth


## Table of Contents
- [Multiagent System (MAS) LLM Newsletter](#multiagent-system-mas-llm-newsletter)
  - [Table of Contents](#table-of-contents)
  - [Introduction](#introduction)
  - [Features](#features)
  - [Architecture](#architecture)
  - [Installation](#installation)
    - [Prerequisites](#prerequisites)
    - [Steps](#steps)

## Introduction

This project aims to create a dynamic newsletter system using a Multiagent System (MAS) and Language Models (LLMs). Each agent in the system performs specific tasks such as content generation, personalization, and distribution. The newsletters can be sent through various channels including SMTP and messaging platforms.

## Features

- **Dynamic Content Generation**: Utilize LLMs to generate personalized content for each recipient.
- **Multiagent Coordination**: Agents collaborate to gather data, create content, and distribute newsletters.
- **Flexible Delivery**: Support for sending newsletters via SMTP and various messaging platforms.
- **Scalability**: Easily add more agents to handle increasing load or additional tasks.
- **Extensibility**: Modular design allows for easy integration of new agents and features.

## Architecture

The system consists of the following main components:

1. **Content Agents**: Generate content based on predefined templates and user data.
2. **Personalization Agents**: Customize content for individual recipients.
3. **Distribution Agents**: Handle the sending of newsletters through SMTP or messaging platforms.
4. **Coordinator Agent**: Manages the workflow and communication between agents.

![Architecture Diagram](docs/architecture.png)

## Installation

### Prerequisites

- Python 3.8+
- pip (Python package installer)

### Steps

1. **Clone the repository**:
    ```sh
    git clone https://github.com/WildSphee/aquarius-news.git
    cd mas-newsletter
    ```

2. **Install dependencies (Linux)**:
    ```sh
    python -m .venv
    source .venv/bin/activate
    pip install poetry
    poetry install
    poetry update
    ```

3. **Set up configuration**:

at the root, create a file called: "AOAI_CONFIG_LIST", format:
```python
[
    {
        "model": "Your Azure OpenAI Service Deployment Model Name",
        "api_key": "Your Azure OpenAI Service API Key",
        "base_url": "Your Azure OpenAI Service Endpoint",
        "api_type": "azure",
        "api_version": "Your Azure OpenAI Service version, eg 2023-12-01-preview"
    },
    {
        "model": "Your Azure OpenAI Service Deployment Model Name",
        "api_key": "Your Azure OpenAI Service API Key",
        "base_url": "Your Azure OpenAI Service Endpoint",
        "api_type": "azure",
        "api_version": "Your Azure OpenAI Service version, eg 2023-12-01-preview"
    }
]
