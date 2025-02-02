#!/usr/bin/env python
import os
import json
import time
import random
import datetime
import openai
from flask import Flask, request, jsonify

# Optional: For Python code formatting (if needed)
try:
    import black
except ImportError:
    black = None

# Initialize Flask application
app = Flask(__name__)

# Set your OpenAI API key securely from the environment
openai.api_key = os.getenv("OPENAI_API_KEY", "YOUR_API_KEY_HERE")

# =============================================================================
# Web3 & Coding Tool Functions
# =============================================================================

def generate_solidity_code(problem: str) -> str:
    """
    Generate a Solidity smart contract based on a natural language description.
    This function calls the OpenAI API with a specialized prompt.
    """
    prompt = (
        f"Generate a complete Solidity smart contract that fulfills the following description:\n"
        f"{problem}\n\n"
        "Provide only the Solidity code without any extra explanation."
    )
    try:
        response = openai.ChatCompletion.create(
            model="o3-mini",
            messages=[
                {"role": "system", "content": "You are an expert Solidity smart contract generator."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300,
            temperature=0.2
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error generating Solidity code: {str(e)}"

def explain_solidity_code(code: str) -> str:
    """
    Explain the given Solidity code snippet in detail.
    """
    prompt = (
        f"Explain in detail what the following Solidity smart contract does, including its purpose and key functions:\n"
        f"{code}\n\n"
        "Provide a clear and concise explanation."
    )
    try:
        response = openai.ChatCompletion.create(
            model="o3-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant specialized in explaining Solidity code."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=250,
            temperature=0.2
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error explaining code: {str(e)}"

def refactor_solidity_code(code: str) -> str:
    """
    Refactor the provided Solidity code for clarity and efficiency.
    """
    prompt = (
        f"Refactor the following Solidity smart contract to improve clarity, efficiency, and security. "
        f"Only return the refactored Solidity code:\n{code}\n"
    )
    try:
        response = openai.ChatCompletion.create(
            model="o3-mini",
            messages=[
                {"role": "system", "content": "You are an expert Solidity developer skilled in code refactoring."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300,
            temperature=0.2
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error refactoring code: {str(e)}"

def analyze_contract(code: str) -> dict:
    """
    Analyze the Solidity contract for potential vulnerabilities.
    This is a simulated analysis.
    """
    vulnerabilities = [
        "Reentrancy vulnerability detected",
        "No obvious vulnerabilities",
        "Potential overflow risk in arithmetic operations",
        "Unchecked external call risk",
        "Ensure proper access control on state-changing functions"
    ]
    analysis = {
        "summary": random.choice(vulnerabilities),
        "details": "This is a simulated vulnerability analysis. For production use, integrate a proper Solidity linter and analysis tool."
    }
    return analysis

def generate_web3_dapp(description: str) -> str:
    """
    Generate skeleton code for a Web3 decentralized application (dApp) using JavaScript and web3.js.
    """
    prompt = (
        f"Generate a complete JavaScript code snippet that creates a basic decentralized application (dApp) "
        f"using web3.js. The dApp should interact with a smart contract based on the following description:\n"
        f"{description}\n\n"
        "Provide only the JavaScript code."
    )
    try:
        response = openai.ChatCompletion.create(
            model="o3-mini",
            messages=[
                {"role": "system", "content": "You are an expert developer for Web3 applications using JavaScript and web3.js."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300,
            temperature=0.2
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error generating dApp code: {str(e)}"

def simulate_deploy_contract(code: str) -> dict:
    """
    Simulate deploying a Solidity contract.
    Returns a dummy contract address and deployment timestamp.
    """
    dummy_address = "0x" + "".join(random.choices("0123456789abcdef", k=40))
    return {
        "contract_address": dummy_address,
        "deployed_at": datetime.datetime.now().isoformat()
    }

def simulate_contract_interaction(contract_address: str, function_name: str, params: dict) -> dict:
    """
    Simulate interacting with a deployed smart contract.
    Returns a dummy result based on the function call.
    """
    dummy_result = {
        "contract_address": contract_address,
        "function_called": function_name,
        "parameters": params,
        "result": random.choice(["Success", "Error", "No Change"])
    }
    return dummy_result

def format_code(code: str) -> str:
    """
    Format the provided code using a code formatter.
    For Python code, uses Black if available; for Solidity, a dummy formatter is applied.
    """
    # Here, we check if the code appears to be Python (contains "def " or "import ")
    if "def " in code or "import " in code:
        if black:
            try:
                return black.format_file_contents(code, fast=True, mode=black.FileMode())
            except Exception as e:
                return f"Error formatting code: {str(e)}"
        else:
            return "Black is not installed. Please install it to format Python code."
    else:
        # For Solidity (or others), perform a simple indentation fix as a dummy formatter.
        lines = code.splitlines()
        formatted = "\n".join(line.strip() for line in lines if line.strip() != "")
        return formatted

def lint_code(code: str) -> str:
    """
    Simulate linting the provided code and return any warnings.
    This dummy implementation always returns that no issues were found.
    """
    return "No linting issues found."

# =============================================================================
# Function Calling Specifications
# =============================================================================

function_definitions = [
    {
        "name": "generate_solidity_code",
        "description": "Generate a complete Solidity smart contract based on a description.",
        "parameters": {
            "type": "object",
            "properties": {
                "problem": {"type": "string", "description": "Description of the smart contract requirements."}
            },
            "required": ["problem"]
        }
    },
    {
        "name": "explain_solidity_code",
        "description": "Provide a detailed explanation of the given Solidity code.",
        "parameters": {
            "type": "object",
            "properties": {
                "code": {"type": "string", "description": "Solidity code to explain."}
            },
            "required": ["code"]
        }
    },
    {
        "name": "refactor_solidity_code",
        "description": "Refactor the given Solidity code for clarity, efficiency, and security.",
        "parameters": {
            "type": "object",
            "properties": {
                "code": {"type": "string", "description": "Solidity code to refactor."}
            },
            "required": ["code"]
        }
    },
    {
        "name": "analyze_contract",
        "description": "Analyze the given Solidity contract code for potential vulnerabilities.",
        "parameters": {
            "type": "object",
            "properties": {
                "code": {"type": "string", "description": "Solidity code of the contract to analyze."}
            },
            "required": ["code"]
        }
    },
    {
        "name": "generate_web3_dapp",
        "description": "Generate skeleton code for a Web3 decentralized application using JavaScript and web3.js.",
        "parameters": {
            "type": "object",
            "properties": {
                "description": {"type": "string", "description": "Description of the dApp requirements."}
            },
            "required": ["description"]
        }
    },
    {
        "name": "simulate_deploy_contract",
        "description": "Simulate the deployment of a Solidity contract and return a dummy contract address.",
        "parameters": {
            "type": "object",
            "properties": {
                "code": {"type": "string", "description": "The Solidity contract code to deploy."}
            },
            "required": ["code"]
        }
    },
    {
        "name": "simulate_contract_interaction",
        "description": "Simulate interacting with a deployed smart contract.",
        "parameters": {
            "type": "object",
            "properties": {
                "contract_address": {"type": "string", "description": "The address of the deployed contract."},
                "function_name": {"type": "string", "description": "The contract function to call."},
                "params": {"type": "object", "description": "Parameters for the function call."}
            },
            "required": ["contract_address", "function_name", "params"]
        }
    },
    {
        "name": "format_code",
        "description": "Format the provided code for better readability.",
        "parameters": {
            "type": "object",
            "properties": {
                "code": {"type": "string", "description": "The code to format."}
            },
            "required": ["code"]
        }
    },
    {
        "name": "lint_code",
        "description": "Lint the provided code and return any warnings or issues.",
        "parameters": {
            "type": "object",
            "properties": {
                "code": {"type": "string", "description": "The code to lint."}
            },
            "required": ["code"]
        }
    }
]

# Mapping of function names to local implementations.
function_map = {
    "generate_solidity_code": generate_solidity_code,
    "explain_solidity_code": explain_solidity_code,
    "refactor_solidity_code": refactor_solidity_code,
    "analyze_contract": analyze_contract,
    "generate_web3_dapp": generate_web3_dapp,
    "simulate_deploy_contract": simulate_deploy_contract,
    "simulate_contract_interaction": simulate_contract_interaction,
    "format_code": format_code,
    "lint_code": lint_code,
}

# =============================================================================
# Flask Endpoint: /api/chat
#
# This endpoint accepts a JSON payload with:
#   - "messages": a list of conversation messages.
#   - "reasoning_effort": (optional) "low", "medium", or "high".
#
# The endpoint sends the conversation to the OpenAI ChatCompletion API
# using the o3-mini model with function calling enabled.
# If the response includes a function call, the corresponding tool is executed,
# and its result is returned.
# =============================================================================

@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json()
    messages = data.get("messages", [])
    reasoning_effort = data.get("reasoning_effort", "medium")
    
    try:
        response = openai.ChatCompletion.create(
            model="o3-mini",
            messages=messages,
            functions=function_definitions,
            function_call="auto",
            max_tokens=300,
            provider_options={"reasoningEffort": reasoning_effort}
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    message = response.choices[0].message

    # If the model returns a function call, execute the corresponding tool.
    if message.get("function_call"):
        func_call = message["function_call"]
        func_name = func_call.get("name")
        arguments_str = func_call.get("arguments", "{}")
        try:
            arguments = json.loads(arguments_str)
        except Exception as e:
            arguments = {}
        if func_name in function_map:
            result = function_map[func_name](**arguments)
            message["content"] = json.dumps(result)
        else:
            message["content"] = f"Error: Function '{func_name}' not implemented."
    
    return jsonify(message)

# =============================================================================
# Main block to run the Flask server.
# =============================================================================
if __name__ == "__main__":
    # The server listens on port 5000 on all interfaces.
    app.run(host="0.0.0.0", port=5000)
