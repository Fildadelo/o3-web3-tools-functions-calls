# OpenAI o3-mini Web3 & Coding Tool Server

This project provides a comprehensive local HTTP API server that leverages OpenAI’s o3‑mini model for Web3 and coding tasks. The server exposes a range of tools specifically designed for smart contract and Web3 development as well as general code generation and analysis. These tools include:

- **generate_solidity_code:** Generate a complete Solidity smart contract from a natural language description.
- **explain_solidity_code:** Provide a detailed explanation of a given Solidity code snippet.
- **refactor_solidity_code:** Refactor Solidity code for improved clarity, efficiency, and security.
- **analyze_contract:** Simulate an analysis of a Solidity contract to detect potential vulnerabilities.
- **generate_web3_dapp:** Generate a skeleton code for a Web3 decentralized application (dApp) using JavaScript (web3.js).
- **simulate_deploy_contract:** Simulate deploying a smart contract and return a dummy contract address.
- **simulate_contract_interaction:** Simulate calling a function on a deployed smart contract.
- **format_code:** Format code for better readability.
- **lint_code:** Lint code to report any potential issues (dummy implementation).

## Features

- **Advanced Reasoning:** Uses the o3‑mini model to maximize coding and Web3 reasoning capabilities.
- **Function Calling:** Supports rich function calling, executing local Python functions based on API responses.
- **Full Integration:** Designed for integration with local MCP servers or other development environments.
- **Adjustable Reasoning Effort:** Specify reasoning effort levels (`low`, `medium`, or `high`) to balance speed and depth.
- **Web3 & Code Focused:** Specifically targeted at smart contract generation, dApp code generation, and other coding-related tasks.

## Requirements

- Python 3.8 or later
- [Flask](https://flask.palletsprojects.com/) – Install with `pip install flask`
- [openai](https://pypi.org/project/openai/) – Install with `pip install openai`
- [Click](https://click.palletsprojects.com/) and [Rich](https://rich.readthedocs.io/) (if you wish to extend the CLI further)
- (Optional) [Black](https://pypi.org/project/black/) – For code formatting (`pip install black`)

## Setup

1. **Obtain an OpenAI API Key:**  
   Sign up at [OpenAI](https://platform.openai.com/) and generate your API key. Set the key as an environment variable:
   - On Unix/Linux/macOS:
     ```bash
     export OPENAI_API_KEY="your_openai_api_key_here"
     ```
   - On Windows:
     ```cmd
     set OPENAI_API_KEY=your_openai_api_key_here
     ```

2. **Download the Code:**  
   Clone this repository or download the `o3_tool_server.py` script.

3. **Install Dependencies:**
   bash
   pip install flask openai black

Usage
Run the Server:
Start the server by running:

bash
Copier
python o3_tool_server.py
The server will listen on port 5000.

Making API Requests:
Send a POST request to the /api/chat endpoint with a JSON payload. For example, using curl:

bash
Copier
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
        "messages": [
          {"role": "system", "content": "You are a helpful assistant specialized in Web3 and coding tasks."},
          {"role": "user", "content": "Generate a Solidity contract for a token with a fixed supply of 1,000,000 tokens."}
        ],
        "reasoning_effort": "high"
      }'
The API uses function calling: if the model returns a directive (e.g. to generate Solidity code), the corresponding local tool function will be executed and its output returned.

Integration:
This server can be integrated with your local MCP servers or any other local service that requires Web3/coding assistance.

Extending the Tools
You can extend the functionality by adding new tool functions. To do this:

Write a new Python function that implements the desired functionality.
Add a corresponding entry to the function_definitions list with a detailed description and parameter schema.
Map the new function in the function_map dictionary.
Troubleshooting
API Errors:
Check that your OPENAI_API_KEY is set correctly and that your account has access to the o3‑mini model.
Port Conflicts:
If port 5000 is already in use, modify the app.run() parameters in the script.
Missing Dependencies:
Ensure all required packages are installed. For code formatting features, verify that Black is installed.
License
This project is provided for educational and development purposes. Please refer to the LICENSE file for details.

References
OpenAI o3-mini Official Page
OpenAI API Documentation
Flask Documentation
Black Documentation

