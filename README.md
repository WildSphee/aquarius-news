# **Aquarius Newsletter**
*Revolutionize Your Newsletter Creation and Distribution with Intelligent Multi-agent Systems (MAS)*

Welcome to the Aquarius! This project leverages a network of agents to dynamically create and distribute newsletters via SMTP or messaging platforms. Target is to provide automatic updated information about the latest news in a certain industry / trend.

**Target Users**:
- Tech or business users that are interested in a specific domain
- Tech leads who need to keep up to speed on rapid tech development landscape
- Hobbyists who wants to learn about a certain topic in depth

## Table of Contents
- [**Aquarius Newsletter**](#aquarius-newsletter)
  - [Table of Contents](#table-of-contents)
  - [Value Proposition](#value-proposition)
    - [Overview](#overview)
    - [Key Value Propositions](#key-value-propositions)
  - [Introduction](#introduction)
  - [Features](#features)
  - [Architecture](#architecture)
  - [Installation](#installation)
    - [Prerequisites](#prerequisites)
    - [Steps](#steps)
  - [Contribution](#contribution)
    - [Linting](#linting)
    - [Testing](#testing)

## Value Proposition
### Overview

Aquarius is a groundbreaking platform that harnesses the power of Multiagent Systems (MAS) and advanced Language Learning Models (LLMs) to streamline the creation and distribution of highly personalized newsletters. Designed to cater to dynamic content needs, Aquarius leverages intelligent agents to automate and optimize every step of the newsletter process, from content generation to delivery.

### Key Value Propositions
1. **Intelligent Content Generation**: Generate engaging, relevant content tailored to your audience using advanced language models.
2. **Personalization at Scale**: Customize content for each recipient based on their preferences and behavior.
3. **Automated Workflow**: Automate the entire newsletter creation and distribution process to save time and reduce errors.
4. **Scalability and Flexibility**: Easily handle growing demands and integrate new features with a modular architecture.
5. **Secure and Confidential**: Ensure the security and confidentiality of your data with robust protocols.
6. **Comprehensive Analytics**: Gain insights into audience engagement with detailed analytics to optimize your content strategy.



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

- Python 3.10+
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

at the root, create a file called: "OAI_CONFIG_LIST", format:
```python
[
    {
        "model": "Your OpenAI Service Deployment Model Name",
        "api_key": "Your OpenAI Service API Key",
        "base_url": "Your OpenAI Service Endpoint",
        "api_type": "azure / OpenAI",
        "api_version": "Your OpenAI Service version, eg 2023-12-01-preview"
    },
    {
        "model": "Your OpenAI Service Deployment Model Name",
        "api_key": "Your OpenAI Service API Key",
        "base_url": "Your OpenAI Service Endpoint",
        "api_type": "azure / OpenAI",
        "api_version": "Your OpenAI Service version, eg 2023-12-01-preview"
    }
]
```
.env schema
```bash
TEMP_OUTPUT_DIR=work_dir

# Google SMTP
FROM_GMAIL=something@gmail.com
TO_GMAIL=something@gmail.com
SMTP_PASSWORD=

# Reddit Scraper
USER_AGENT=python:YourProject:v1.0 (by /u/someUser)
CLIENT_ID=
SCRAPER_SECRET=
```

## Contribution
We welcome all contributions to this repository!

### Linting
Linting is the process of analyzing code to identify potential errors, enforce coding standards, and improve code quality. It helps catch bugs early, ensures code consistency, and enhances readability.
This repository uses **Ruff** and **mypy** for linting. All PRs must be linted before being approved.

To check for linting issues without applying fixes:
```bash
sh scripts/lint.sh <optional filepath>
```
To lint and automatically apply fixes:
```bash
sh scripts/lint.sh --in-place <optional filepath>
```

### Testing
This repository uses `pytest` for testing. We use `monkeypatch` from pytest for patching in our tests to ensure robust and reliable testing.
To run all tests:
```bash
pytest
```
To run a specific test file or function, for example:
```bash
pytest tests/tools/test_arxiv.py::test_fetch_arxiv_articles
```
By following these guidelines, we ensure that our code remains clean, consistent, and well-tested. Thank you for your contributions!