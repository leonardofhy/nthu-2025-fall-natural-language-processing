import matplotlib.pyplot as plt
import numpy as np

# Data from the experiments table
steps = ['Exp 0', 'Exp 1', 'Exp 2', 'Exp 3', 'Final']
cv_scores = [0.3642, 0.3797, 0.4026, 0.4218, 0.4228]
improvements = [0, 0.0155, 0.0229, 0.0192, 0.0010]

# Baseline reference
baseline_cv = 0.4195

# Colors
colors = ['#ff6b6b', '#4ecdc4', '#45b7d1', '#96ceb4', '#dda0dd']

# Create figure
fig, ax = plt.subplots(figsize=(10, 6))

# Bar chart
bars = ax.bar(steps, cv_scores, color=colors, edgecolor='black', linewidth=1.2)

# Baseline reference line
ax.axhline(y=baseline_cv, color='#e74c3c', linestyle='--', linewidth=2, label=f'BERT Baseline (CV: {baseline_cv})')

# Add value labels on bars
for bar, score, imp in zip(bars, cv_scores, improvements):
    height = bar.get_height()
    ax.annotate(f'{score:.4f}',
                xy=(bar.get_x() + bar.get_width() / 2, height),
                xytext=(0, 3),
                textcoords="offset points",
                ha='center', va='bottom', fontsize=10, fontweight='bold')
    if imp > 0:
        ax.annotate(f'+{imp:.4f}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 18),
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=9, color='green')

# Labels and title
ax.set_ylabel('CV Spearman Correlation', fontsize=12, fontweight='bold')
ax.set_xlabel('Experiment', fontsize=12, fontweight='bold')
ax.set_title('Progressive Performance Improvements', fontsize=14, fontweight='bold')

# Y-axis limits
ax.set_ylim(0.35, 0.44)

# Legend
ax.legend(loc='lower right', fontsize=10)

# Grid
ax.yaxis.grid(True, linestyle='--', alpha=0.7)
ax.set_axisbelow(True)

# Tight layout
plt.tight_layout()

# Save
plt.savefig('/home/leonardo298/Workspace/nthu-2025-fall-natural-language-processing/final/overleaf_latex/images/ablation_chart.png', dpi=150, bbox_inches='tight')
plt.close()

print("Ablation chart saved successfully!")
