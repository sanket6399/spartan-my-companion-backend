# Spartan My Companion Backend

This repository contains the backend code for the Spartan My Companion project.

## Infrastructure

The `infrastructure` directory includes AWS SAM templates for managing serverless resources. 

### Key Files

- `template.yaml`: Contains the AWS SAM template for deployment.

## Lambda Functions

The `src/lambda` directory contains the source code for all the lambda functions used in this backend.

## Getting Started

To get started with this project, follow these steps:

### Prerequisites

- AWS CLI installed and configured
- SAM CLI installed

### Deployment

To deploy the backend to AWS:

1. Navigate to the project root directory.
2. Build the SAM application:
   ```bash
   sam build
   sam deploy --guided

### Contributing
Contributions are welcome! Please read our contributing guidelines in CONTRIBUTING.md before submitting pull requests.

### License
This project is licensed under the MIT License - see the LICENSE file for details.
You can customize the contents to match more closely with the specific technologies, dependencies, and setup instructions that your project requires.
