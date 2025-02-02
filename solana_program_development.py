#!/usr/bin/env python
"""
Solana Program Development CLI Tool
------------------------------------

This tool provides a full-featured CLI for developing Solana programs (in Rust)
using OpenAI’s o3-mini model. It supports the following functionalities:
  • Generate a complete Solana program from a natural language description.
  • Explain a given Solana program (Rust code).
  • Refactor a Solana program for clarity, efficiency, and security.
  • Format Solana code for improved readability.
  • Lint Solana code (dummy implementation).
  • Simulate deployment of a Solana program (returns a dummy program address).

Usage:
    python solana_program_development.py <command> [options]

For example, to generate a Solana program:
    python solana_program_development.py generate "Create a token contract with a fixed supply of 1,000,000 tokens."
"""

import os
import json
import random
import datetime
import asyncio
import openai
import click
from rich.console import Console

# Initialize Rich console for pretty printing
console = Console()

# Set OpenAI API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY", "YOUR_API_KEY_HERE")


# =============================================================================
# Async functions to call OpenAI's o3-mini for Solana program tasks
# =============================================================================

async def generate_solana_program(problem: str) -> str:
    """
    Generate a complete Solana program in Rust based on a natural language description.
    
    The generated program is expected to follow best practices, include comments,
    and be production-ready.
    """
    prompt = (
        f"Generate a complete Solana program in Rust that fulfills the following description:\n"
        f"{problem}\n\n"
        "Ensure that the code is well-structured, follows best practices, includes comments, "
        "and provides only the Rust code."
    )
    try:
        response = await openai.ChatCompletion.acreate(
            model="o3-mini",
            messages=[
                {"role": "system", "content": "You are an expert in Solana program development using Rust."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=400,
            temperature=0.2,
            provider_options={"reasoningEffort": "high"}
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error generating Solana program: {str(e)}"

async def explain_solana_program(code: str) -> str:
    """
    Provide a detailed explanation of the given Solana program (Rust code).
    """
    prompt = (
        f"Explain in detail the following Solana program written in Rust, including its purpose and key functions:\n\n"
        f"{code}\n\n"
        "Provide a clear and concise explanation."
    )
    try:
        response = await openai.ChatCompletion.acreate(
            model="o3-mini",
            messages=[
                {"role": "system", "content": "You are an expert in Solidity and Rust-based Solana programs."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300,
            temperature=0.2,
            provider_options={"reasoningEffort": "medium"}
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error explaining Solana program: {str(e)}"

async def refactor_solana_program(code: str) -> str:
    """
    Refactor the provided Solana program code (Rust) for improved clarity, efficiency, and security.
    """
    prompt = (
        f"Refactor the following Solana program in Rust for better clarity, efficiency, and security. "
        f"Return only the refactored code:\n\n{code}\n"
    )
    try:
        response = await openai.ChatCompletion.acreate(
            model="o3-mini",
            messages=[
                {"role": "system", "content": "You are a seasoned Rust developer specialized in Solana programs."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=400,
            temperature=0.2,
            provider_options={"reasoningEffort": "high"}
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error refactoring Solana program: {str(e)}"

async def format_solana_code(code: str) -> str:
    """
    Format the provided Solana code for improved readability.
    
    For Rust, we'll simulate formatting by stripping extra spaces.
    """
    try:
        # For demonstration, a simple reformat: remove extra whitespace.
        formatted_lines = [line.strip() for line in code.splitlines() if line.strip()]
        return "\n".join(formatted_lines)
    except Exception as e:
        return f"Error formatting code: {str(e)}"

async def lint_solana_code(code: str) -> str:
    """
    Lint the provided Solana code.
    
    This dummy implementation returns that no issues were found.
    """
    # In production, integrate a Rust linter (like Clippy) via subprocess if needed.
    return "No linting issues found."

def simulate_deploy_solana_program(code: str) -> dict:
    """
    Simulate the deployment of a Solana program.
    
    Returns a dummy deployment result with a fake program address and timestamp.
    """
    dummy_address = "SolanaProg_" + "".join(random.choices("0123456789ABCDEF", k=16))
    return {
        "program_address": dummy_address,
        "deployed_at": datetime.datetime.now().isoformat()
    }

# =============================================================================
# CLI commands using Click
# =============================================================================

@click.group()
def cli():
    """Solana Program Development CLI Tool"""
    pass

@cli.command()
@click.argument("description", nargs=-1)
def generate(description):
    """
    Generate a complete Solana program in Rust from a natural language description.
    
    Example: 
        python solana_program_development.py generate "Create a token program with fixed supply of 1,000,000 tokens."
    """
    desc = " ".join(description)
    console.print("[bold blue]Generating Solana program...[/bold blue]")
    result = asyncio.run(generate_solana_program(desc))
    console.print("[bold green]Generated Solana Program:[/bold green]")
    console.print(f"```rust\n{result}\n```")

@cli.command()
@click.argument("code", nargs=-1)
def explain(code):
    """
    Explain a given Solana program (Rust code) in detail.
    
    Example:
        python solana_program_development.py explain "pub fn process_instruction(...) { ... }"
    """
    code_str = " ".join(code)
    console.print("[bold blue]Explaining Solana program...[/bold blue]")
    result = asyncio.run(explain_solana_program(code_str))
    console.print("[bold green]Explanation:[/bold green]")
    console.print(result)

@cli.command()
@click.argument("code", nargs=-1)
def refactor(code):
    """
    Refactor the provided Solana program code for clarity and efficiency.
    
    Example:
        python solana_program_development.py refactor "pub fn old_code(...) { ... }"
    """
    code_str = " ".join(code)
    console.print("[bold blue]Refactoring Solana program...[/bold blue]")
    result = asyncio.run(refactor_solana_program(code_str))
    console.print("[bold green]Refactored Code:[/bold green]")
    console.print(f"```rust\n{result}\n```")

@cli.command()
@click.argument("code", nargs=-1)
def format_code(code):
    """
    Format the provided Solana code for readability.
    
    Example:
        python solana_program_development.py format_code "  pub fn main() { println!(\"Hello Solana\"); }  "
    """
    code_str = " ".join(code)
    console.print("[bold blue]Formatting code...[/bold blue]")
    result = asyncio.run(format_solana_code(code_str))
    console.print("[bold green]Formatted Code:[/bold green]")
    console.print(f"```rust\n{result}\n```")

@cli.command()
@click.argument("code", nargs=-1)
def lint(code):
    """
    Lint the provided Solana code and return warnings.
    
    Example:
        python solana_program_development.py lint "pub fn main() { ... }"
    """
    code_str = " ".join(code)
    console.print("[bold blue]Linting code...[/bold blue]")
    result = asyncio.run(lint_solana_code(code_str))
    console.print("[bold green]Linting Result:[/bold green]")
    console.print(result)

@cli.command()
@click.argument("code", nargs=-1)
def deploy(code):
    """
    Simulate deploying a Solana program and return a dummy deployment result.
    
    Example:
        python solana_program_development.py deploy "pub fn main() { ... }"
    """
    code_str = " ".join(code)
    console.print("[bold blue]Simulating deployment of the Solana program...[/bold blue]")
    result = simulate_deploy_solana_program(code_str)
    console.print("[bold green]Deployment Result:[/bold green]")
    console.print(json.dumps(result, indent=2))

if __name__ == "__main__":
    cli()
