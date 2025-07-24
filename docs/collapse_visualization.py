#!/usr/bin/env python3
"""
生成Collapse理论核心概念的可视化图表
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Circle, Rectangle
import seaborn as sns

# 设置字体和样式
plt.rcParams['font.sans-serif'] = ['DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False
sns.set_theme(style="whitegrid")

def create_core_concept_diagram():
    """创建核心概念示意图"""
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # 1. 传统搜索 vs Collapse方法
    ax1 = axes[0, 0]
    ax1.set_xlim(0, 10)
    ax1.set_ylim(0, 10)
    ax1.axis('off')
    ax1.set_title('Traditional Search vs Natural Collapse', fontsize=14, fontweight='bold')
    
    # 传统方法：遍历所有可能
    for i in range(4):
        for j in range(4):
            rect = Rectangle((i*0.8+0.5, j*0.8+5), 0.6, 0.6, 
                           facecolor='lightcoral', edgecolor='darkred', alpha=0.7)
            ax1.add_patch(rect)
            if i == 2 and j == 2:
                rect.set_facecolor('darkred')
                ax1.text(i*0.8+0.8, j*0.8+5.3, '*', fontsize=20, color='yellow', ha='center')
    
    ax1.text(2, 8.5, 'Traditional: Search 2^n possibilities', ha='center', fontsize=12)
    ax1.text(2, 4, 'Complexity: O(n×W)', ha='center', fontsize=10, style='italic')
    
    # Collapse方法：自然路径
    points = np.array([[5, 2], [6, 3], [7, 5], [8, 7], [9, 8]])
    for i in range(len(points)-1):
        ax1.arrow(points[i,0], points[i,1], 
                 points[i+1,0]-points[i,0], points[i+1,1]-points[i,1],
                 head_width=0.3, head_length=0.2, fc='forestgreen', ec='forestgreen')
    
    # 添加张力场示意
    for i, (x, y) in enumerate(points):
        circle = Circle((x, y), 0.3*(5-i)/5 + 0.2, color='lightgreen', alpha=0.5)
        ax1.add_patch(circle)
        ax1.text(x, y, f'{i+1}', ha='center', va='center', fontweight='bold')
    
    ax1.text(7, 1.5, 'Collapse: Follow natural path', ha='center', fontsize=12)
    ax1.text(7, 0.5, 'Complexity: O(n log n)', ha='center', fontsize=10, style='italic')
    
    # 2. φ-trace编码示意
    ax2 = axes[0, 1]
    ax2.set_xlim(0, 10)
    ax2.set_ylim(0, 10)
    ax2.axis('off')
    ax2.set_title('Fibonacci Encoding (φ-trace)', fontsize=14, fontweight='bold')
    
    # 显示数字到Fibonacci编码的转换
    examples = [
        (5, [1, 0, 0, 1], "5 = F₄ + F₁"),
        (13, [1, 0, 0, 0, 0, 1], "13 = F₆ + F₁"),
        (21, [1, 0, 0, 0, 0, 0, 1], "21 = F₇")
    ]
    
    y_pos = 8
    for num, encoding, formula in examples:
        # 显示数字
        ax2.text(1, y_pos, f'{num} →', fontsize=12, ha='right')
        
        # 显示编码
        for i, bit in enumerate(encoding):
            color = 'darkgreen' if bit == 1 else 'lightgray'
            rect = Rectangle((2+i*0.6, y_pos-0.3), 0.5, 0.6, 
                           facecolor=color, edgecolor='black')
            ax2.add_patch(rect)
            ax2.text(2+i*0.6+0.25, y_pos, str(bit), ha='center', va='center', 
                    color='white' if bit == 1 else 'black', fontweight='bold')
        
        # 显示公式
        ax2.text(2+(len(encoding)+0.5)*0.6, y_pos, formula, fontsize=10, va='center')
        
        y_pos -= 2.5
    
    ax2.text(5, 1.5, 'No consecutive 1s → Unique representation', 
            ha='center', fontsize=11, style='italic', color='darkblue')
    
    # 3. 张力场可视化
    ax3 = axes[1, 0]
    ax3.set_title('Collapse Tension Field', fontsize=14, fontweight='bold')
    
    # 创建张力场热图
    x = np.linspace(0, 10, 100)
    y = np.linspace(0, 10, 100)
    X, Y = np.meshgrid(x, y)
    
    # 模拟张力场：距离越近张力越大
    Z = np.zeros_like(X)
    centers = [(2, 8), (5, 6), (8, 3)]  # 高价值物品位置
    for cx, cy in centers:
        dist = np.sqrt((X - cx)**2 + (Y - cy)**2)
        Z += 1 / (dist**0.5 + 0.1)  # ζ = 1/|φ-trace|^0.5
    
    contour = ax3.contourf(X, Y, Z, levels=20, cmap='YlOrRd')
    ax3.contour(X, Y, Z, levels=10, colors='black', alpha=0.3, linewidths=0.5)
    
    # 标记物品位置
    for i, (cx, cy) in enumerate(centers):
        ax3.plot(cx, cy, 'b*', markersize=15)
        ax3.text(cx+0.3, cy+0.3, f'Item {i+1}', fontsize=9, fontweight='bold')
    
    # 绘制Collapse路径
    path_x = [1, 2, 5, 8, 9]
    path_y = [9, 8, 6, 3, 1]
    ax3.plot(path_x, path_y, 'b-', linewidth=3, alpha=0.8)
    ax3.plot(path_x, path_y, 'bo', markersize=8)
    
    ax3.set_xlabel('Space')
    ax3.set_ylabel('Value Density')
    ax3.text(5, -0.5, 'Path follows maximum gradient', ha='center', fontsize=10, style='italic')
    
    # 4. 性能对比
    ax4 = axes[1, 1]
    ax4.set_title('Performance Comparison', fontsize=14, fontweight='bold')
    
    # 数据
    sizes = np.array([50, 100, 200, 500, 1000, 2000])
    dp_times = sizes**2 * 0.00001  # O(n²)模拟
    collapse_times = sizes * np.log2(sizes) * 0.000001  # O(n log n)模拟
    
    ax4.plot(sizes, dp_times, 'r-o', label='Dynamic Programming O(n×W)', linewidth=2)
    ax4.plot(sizes, collapse_times, 'g-o', label='Collapse Method O(n log n)', linewidth=2)
    
    ax4.set_xlabel('Problem Size (n)')
    ax4.set_ylabel('Time (seconds)')
    ax4.set_yscale('log')
    ax4.legend()
    ax4.grid(True, alpha=0.3)
    
    # 添加加速比文字
    speedup = dp_times[-1] / collapse_times[-1]
    ax4.text(1500, 0.001, f'{speedup:.0f}x faster', fontsize=12, 
            bbox=dict(boxstyle="round,pad=0.3", facecolor="yellow", alpha=0.7))
    
    plt.tight_layout()
    plt.savefig('collapse_core_concepts.png', dpi=300, bbox_inches='tight')
    plt.show()

def create_philosophy_diagram():
    """创建哲学意义示意图"""
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # 标题
    ax.text(5, 9.5, 'From Computation to Natural Process', 
            fontsize=16, fontweight='bold', ha='center')
    
    # 左侧：传统计算观
    left_box = FancyBboxPatch((0.5, 3), 4, 5, 
                             boxstyle="round,pad=0.1",
                             facecolor='lightcoral', 
                             edgecolor='darkred',
                             linewidth=2)
    ax.add_patch(left_box)
    
    ax.text(2.5, 7, 'Traditional View', fontsize=14, ha='center', fontweight='bold')
    ax.text(2.5, 6.3, '• Exhaustive search', fontsize=11, ha='center')
    ax.text(2.5, 5.8, '• Discrete states', fontsize=11, ha='center')
    ax.text(2.5, 5.3, '• Symbolic manipulation', fontsize=11, ha='center')
    ax.text(2.5, 4.8, '• Algorithm finds solution', fontsize=11, ha='center')
    ax.text(2.5, 4.3, '• Computation = Calculation', fontsize=11, ha='center')
    ax.text(2.5, 3.5, 'Complexity: NP-Complete', fontsize=10, ha='center', style='italic')
    
    # 右侧：Collapse观
    right_box = FancyBboxPatch((5.5, 3), 4, 5,
                              boxstyle="round,pad=0.1",
                              facecolor='lightgreen',
                              edgecolor='darkgreen',
                              linewidth=2)
    ax.add_patch(right_box)
    
    ax.text(7.5, 7, 'Collapse View', fontsize=14, ha='center', fontweight='bold')
    ax.text(7.5, 6.3, '• Natural selection', fontsize=11, ha='center')
    ax.text(7.5, 5.8, '• Continuous field', fontsize=11, ha='center')
    ax.text(7.5, 5.3, '• Physical process', fontsize=11, ha='center')
    ax.text(7.5, 4.8, '• Solution emerges', fontsize=11, ha='center')
    ax.text(7.5, 4.3, '• Computation = Physics', fontsize=11, ha='center')
    ax.text(7.5, 3.5, 'Complexity: O(n log n)', fontsize=10, ha='center', style='italic')
    
    # 中间箭头
    ax.arrow(4.5, 5.5, 1, 0, head_width=0.3, head_length=0.2, 
            fc='blue', ec='blue', linewidth=3)
    ax.text(5, 6, 'Paradigm\nShift', ha='center', va='bottom', fontsize=11, fontweight='bold')
    
    # 底部说明
    ax.text(5, 2, 'Key Insight: NP-Complete reflects collapse path complexity,\nnot search difficulty',
            ha='center', fontsize=12, style='italic',
            bbox=dict(boxstyle="round,pad=0.5", facecolor="lightyellow"))
    
    # 数学公式
    ax.text(5, 0.5, r'$\zeta_i = \frac{1}{|\phi\text{-}trace_i|^{0.5}}$', 
            fontsize=14, ha='center',
            bbox=dict(boxstyle="round,pad=0.3", facecolor="white", edgecolor="black"))
    
    plt.savefig('collapse_philosophy.png', dpi=300, bbox_inches='tight')
    plt.show()

def main():
    """生成所有配图"""
    print("Generating core concept diagrams...")
    create_core_concept_diagram()
    
    print("Generating philosophy diagram...")
    create_philosophy_diagram()
    
    print("All diagrams generated successfully!")

if __name__ == "__main__":
    main()