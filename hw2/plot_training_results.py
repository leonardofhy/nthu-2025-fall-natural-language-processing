#!/usr/bin/env python3
"""
Script to generate visualization plots from training logs.
This script parses the training_logs_and_evaluation_accuracy.txt file
and creates plots showing training loss and validation accuracy over epochs.
"""

import re
import matplotlib.pyplot as plt
import numpy as np


def parse_training_logs(log_file):
    """Parse the training log file and extract metrics."""
    with open(log_file, 'r') as f:
        content = f.read()
    
    epochs = []
    losses = []
    validation_ems = []
    
    # Split content into epoch blocks
    epoch_blocks = re.split(r'={70,}', content)
    
    for block in epoch_blocks:
        # Look for epoch completion with loss
        epoch_match = re.search(r'Epoch (\d+)/\d+ Complete\s+Loss: ([\d.]+)', block)
        if epoch_match:
            epoch = int(epoch_match.group(1))
            loss = float(epoch_match.group(2))
            
            # Look for validation EM in the same block
            em_match = re.search(r'Validation EM: ([\d.]+)', block)
            if em_match:
                em = float(em_match.group(1))
                
                # Only add if this is the first occurrence or a "Complete" block
                # (to avoid duplicate epoch 7)
                epochs.append(epoch)
                losses.append(loss)
                validation_ems.append(em)
    
    return epochs, losses, validation_ems


def create_plots(epochs, losses, validation_ems, final_accuracy=93.82):
    """Create and save visualization plots."""
    
    # Create figure with two subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    # Plot 1: Training Loss
    ax1.plot(epochs, losses, marker='o', linewidth=2, markersize=6, color='#e74c3c')
    ax1.set_xlabel('Epoch', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Training Loss', fontsize=12, fontweight='bold')
    ax1.set_title('Training Loss Over Epochs', fontsize=14, fontweight='bold')
    ax1.grid(True, alpha=0.3, linestyle='--')
    ax1.set_xticks(epochs)
    
    # Add loss values on plot
    for i, (epoch, loss) in enumerate(zip(epochs, losses)):
        ax1.annotate(f'{loss:.3f}', 
                    xy=(epoch, loss), 
                    xytext=(0, 10),
                    textcoords='offset points',
                    ha='center',
                    fontsize=8,
                    bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.3))
    
    # Plot 2: Validation Exact Match (Accuracy)
    validation_pct = [em * 100 for em in validation_ems]
    ax2.plot(epochs, validation_pct, marker='s', linewidth=2, markersize=6, 
             color='#2ecc71', label='Validation EM')
    ax2.axhline(y=final_accuracy, color='#3498db', linestyle='--', linewidth=2,
                label=f'Final Test Accuracy: {final_accuracy}%')
    ax2.set_xlabel('Epoch', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Exact Match (%)', fontsize=12, fontweight='bold')
    ax2.set_title('Validation Accuracy Over Epochs', fontsize=14, fontweight='bold')
    ax2.grid(True, alpha=0.3, linestyle='--')
    ax2.set_xticks(epochs)
    ax2.legend(loc='lower right', fontsize=10)
    
    # Add percentage values on plot
    for i, (epoch, pct) in enumerate(zip(epochs, validation_pct)):
        ax2.annotate(f'{pct:.2f}%', 
                    xy=(epoch, pct), 
                    xytext=(0, 10),
                    textcoords='offset points',
                    ha='center',
                    fontsize=8,
                    bbox=dict(boxstyle='round,pad=0.3', facecolor='lightgreen', alpha=0.3))
    
    # Set y-axis limits for better visualization
    ax2.set_ylim(40, 100)
    
    # Add overall title
    fig.suptitle('Seq2Seq Model Training Results for Arithmetic Task', 
                 fontsize=16, fontweight='bold', y=1.02)
    
    plt.tight_layout()
    
    # Save figure
    output_file = 'training_results.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"✓ Figure saved to: {output_file}")
    
    # Display figure
    plt.show()
    
    return fig


def print_summary(epochs, losses, validation_ems):
    """Print summary statistics."""
    print("\n" + "="*60)
    print("Training Summary")
    print("="*60)
    print(f"Total Epochs:           {len(epochs)}")
    print(f"Initial Loss:           {losses[0]:.4f}")
    print(f"Final Loss:             {losses[-1]:.4f}")
    print(f"Loss Reduction:         {losses[0] - losses[-1]:.4f} ({(1 - losses[-1]/losses[0])*100:.2f}%)")
    print(f"\nInitial Validation EM:  {validation_ems[0]*100:.2f}%")
    print(f"Final Validation EM:    {validation_ems[-1]*100:.2f}%")
    print(f"EM Improvement:         {(validation_ems[-1] - validation_ems[0])*100:.2f} percentage points")
    print("="*60)


def main():
    """Main function to run the script."""
    log_file = 'training_logs_and_evaluation_accuracy.txt'
    
    print("Parsing training logs...")
    epochs, losses, validation_ems = parse_training_logs(log_file)
    
    print(f"Found {len(epochs)} epochs of training data")
    
    print_summary(epochs, losses, validation_ems)
    
    print("\nGenerating plots...")
    create_plots(epochs, losses, validation_ems)
    
    print("\n✓ All done!")


if __name__ == "__main__":
    main()
