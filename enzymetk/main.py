#!/usr/bin/env python3
"""
EnzymeTK Environment Installer

A CLI tool for installing conda environments for various bioinformatics tools.
"""

import subprocess
import sys
from pathlib import Path
from typing import Optional
from os.path import dirname, join as joinpath

import typer

app = typer.Typer(
    name="enzymetk-install",
    help="Install conda environments for EnzymeTK tools",
    add_completion=False,
)

# Get the directory where this script is located
SCRIPT_DIR = Path(__file__).parent.resolve() #dirname(__file__)

#Path(__file__).parent.resolve()


def run_script(script_name: str, verbose: bool = True) -> int:
    """Run a shell script from the conda_envs directory."""
    script_path = Path(f'{SCRIPT_DIR}/{script_name}')
    
    if not script_path.exists():
        typer.secho(f"Error: Script {script_name} not found at {script_path}", fg=typer.colors.RED)
        raise typer.Exit(1)
    
    typer.secho(f"Running {script_name}...", fg=typer.colors.BLUE)
    
    try:
        result = subprocess.run(
            ["bash", str(script_path)],
            cwd=str(SCRIPT_DIR),
            check=True,
            capture_output=not verbose,
            text=True,
        )
        typer.secho(f"✓ {script_name} completed successfully", fg=typer.colors.GREEN)
        return 0
    except subprocess.CalledProcessError as e:
        typer.secho(f"✗ {script_name} failed with exit code {e.returncode}", fg=typer.colors.RED)
        if not verbose and e.stderr:
            typer.echo(e.stderr)
        raise typer.Exit(1)


@app.command()
def install_base(
    verbose: bool = typer.Option(True, "--verbose/--quiet", "-v/-q", help="Show command output"),
):
    """Install the base enzymetk environment.
    
    This is the main environment that works with most tools.
    Includes: fair-esm, scikit-learn, numpy, seaborn, pandas, biopython, etc.
    """
    run_script("base.sh", verbose)


@app.command()
def install_care(
    verbose: bool = typer.Option(True, "--verbose/--quiet", "-v/-q", help="Show command output"),
):
    """Install the CARE processing environment.
    
    Includes CARE_processing and CREEP environments for enzyme function prediction.
    """
    run_script("care.sh", verbose)


@app.command()
def install_clean(
    verbose: bool = typer.Option(True, "--verbose/--quiet", "-v/-q", help="Show command output"),
):
    """Install the CLEAN environment.
    
    Contrastive Learning for Enzyme Annotation.
    """
    run_script("clean.sh", verbose)


@app.command()
def install_clustalomega(
    verbose: bool = typer.Option(True, "--verbose/--quiet", "-v/-q", help="Show command output"),
):
    """Install Clustal Omega for multiple sequence alignment."""
    run_script("clustalomega.sh", verbose)


@app.command()
def install_diamond(
    verbose: bool = typer.Option(True, "--verbose/--quiet", "-v/-q", help="Show command output"),
):
    """Install Diamond for fast sequence alignment.
    
    A BLAST-compatible aligner for protein and translated DNA searches.
    """
    run_script("diamond.sh", verbose)


@app.command()
def install_docko(
    verbose: bool = typer.Option(True, "--verbose/--quiet", "-v/-q", help="Show command output"),
):
    """Install the Docko environment for molecular docking.
    
    Includes pdbfixer and chai-lab for protein-ligand docking.
    """
    run_script("docko.sh", verbose)


@app.command()
def install_fasttree(
    verbose: bool = typer.Option(True, "--verbose/--quiet", "-v/-q", help="Show command output"),
):
    """Install FastTree for phylogenetic tree construction.
    
    Approximately-maximum-likelihood phylogenetic trees from alignments.
    """
    run_script("fasttree.sh", verbose)


@app.command()
def install_foldseek(
    verbose: bool = typer.Option(True, "--verbose/--quiet", "-v/-q", help="Show command output"),
):
    """Install Foldseek for protein structure search.
    
    Fast and sensitive protein structure search. Also installs MMseqs2.
    """
    run_script("foldseek.sh", verbose)


@app.command()
def install_ligandmpnn(
    verbose: bool = typer.Option(True, "--verbose/--quiet", "-v/-q", help="Show command output"),
):
    """Install the LigandMPNN environment.
    
    For protein sequence design with ligand context.
    """
    run_script("ligandmpnn.sh", verbose)


@app.command()
def install_metagenomics(
    verbose: bool = typer.Option(True, "--verbose/--quiet", "-v/-q", help="Show command output"),
):
    """Install the metagenomics environment.
    
    Includes prokka, mmseqs2, Porechop, and sratoolkit for metagenomic analysis.
    """
    run_script("metagenomics.sh", verbose)


@app.command()
def install_proteinfer(
    verbose: bool = typer.Option(True, "--verbose/--quiet", "-v/-q", help="Show command output"),
):
    """Install the ProteInfer environment.
    
    Deep learning for protein function prediction.
    """
    run_script("proteinfer.sh", verbose)


@app.command()
def install_rfdiffusion(
    verbose: bool = typer.Option(True, "--verbose/--quiet", "-v/-q", help="Show command output"),
):
    """Install the RFdiffusion environment.
    
    Generative model for protein structure design.
    """
    run_script("rfdiffusion.sh", verbose)


@app.command()
def install_rxnfp(
    verbose: bool = typer.Option(True, "--verbose/--quiet", "-v/-q", help="Show command output"),
):
    """Install the RXNFP environment.
    
    Reaction fingerprints for chemical reaction analysis.
    """
    run_script("rxnfp.sh", verbose)


@app.command()
def install_unimol(
    verbose: bool = typer.Option(True, "--verbose/--quiet", "-v/-q", help="Show command output"),
):
    """Install the UniMol environment.
    
    Universal molecular representation learning.
    """
    run_script("unimol.sh", verbose)


@app.command()
def install_all(
    verbose: bool = typer.Option(True, "--verbose/--quiet", "-v/-q", help="Show command output"),
):
    """Install all available environments.
    
    This will install: base, clean, docko, foldseek, metagenomics, 
    proteinfer, rfdiffusion, and rxnfp environments.
    """
    run_script("install_all.sh", verbose)


@app.command()
def list_tools():
    """List all available tools that can be installed."""
    tools = [
        ("base", "Base enzymetk environment with common dependencies"),
        ("care", "CARE processing for enzyme function prediction"),
        ("clean", "CLEAN - Contrastive Learning for Enzyme Annotation"),
        ("clustalomega", "Clustal Omega for multiple sequence alignment"),
        ("diamond", "Diamond for fast sequence alignment"),
        ("docko", "Docko for molecular docking"),
        ("fasttree", "FastTree for phylogenetic tree construction"),
        ("foldseek", "Foldseek for protein structure search"),
        ("ligandmpnn", "LigandMPNN for protein sequence design"),
        ("metagenomics", "Metagenomics tools (prokka, mmseqs2, Porechop, sratoolkit)"),
        ("proteinfer", "ProteInfer for protein function prediction"),
        ("rfdiffusion", "RFdiffusion for protein structure design"),
        ("rxnfp", "RXNFP for reaction fingerprints"),
        ("unimol", "UniMol for molecular representation learning"),
        ("all", "Install all environments"),
    ]
    
    typer.secho("\nAvailable tools for installation:\n", fg=typer.colors.BLUE, bold=True)
    
    for name, description in tools:
        typer.echo(f"  {typer.style(name, fg=typer.colors.GREEN, bold=True):20} - {description}")
    
    typer.echo("\nUsage: python install.py <tool-name>")
    typer.echo("Example: python install.py base")
    typer.echo("         python install.py --help")


if __name__ == "__main__":
    app()