# GitHub Webhook Receiver

This project is built as part of the TechStaX developer assignment. It receives GitHub webhook events and stores them in MongoDB, then displays them on a simple UI that updates every 15 seconds.

## Features

- Receives GitHub events: `push`, `pull_request`, and `merge`
- Stores events in MongoDB
- UI built with HTML and JavaScript to auto-refresh and show latest events

## Tech Stack

- Python
- Flask
- MongoDB (Atlas)
- HTML, JavaScript

## MongoDB Schema

```json
{
  "message": "User pushed to branch on timestamp",
  "timestamp": ISODate
}
