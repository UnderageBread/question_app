import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.gridspec import GridSpec
import numpy as np
from matplotlib import font_manager
import warnings
from matplotlib import image as mpimg
from datetime import datetime
warnings.filterwarnings('ignore')

# plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'DejaVu Sans']
# plt.rcParams['axes.unicode_minus'] = False

def calculate_scores(responses):
    scores = {
        'module1': {},
        'module2': {},
        'module3': {}
    }
    
    score_map = {'A': 4, 'B': 3, 'C': 2, 'D': 1}
    
    m1_questions = {
        '学习专注力': [1, 2, 3],
        '作业细致能力': [4, 5, 6],
        '笔头作业能力': [7, 8, 9],
        '读写能力': [10, 11, 12],
        '理解记忆能力': [13, 14, 15],
        '感统发展': [16, 17, 18]
    }
    
    for dim, q_nums in m1_questions.items():
        dim_score = 0
        for q_num in q_nums:
            answer = responses['module1'].get(q_num)
            if q_num == 16:
                if isinstance(answer, list):
                    score_16 = 0
                    print('feafeawfaw awefawefe',score_16)
                    if 'A' in answer:
                        score_16 += 4
                    if 'B' in answer:
                        score_16 += 0
                    if 'C' in answer:
                        score_16 -= 1
                    if 'D' in answer:
                        score_16 -= 1
                    print('feafeawfaw',score_16)
                    dim_score += max(-100, score_16)
                else:
                    dim_score += score_map.get(answer, 0)
            else:
                dim_score += score_map.get(answer, 0)
        scores['module1'][dim] = dim_score
    
    m2_questions = {
        '家庭能量': [1, 2, 3],
        '师生能量': [4, 5, 6],
        '同伴能量': [7, 8, 9],
        '自我价值感': [10, 11, 12]
    }
    
    for dim, q_nums in m2_questions.items():
        dim_score = sum(score_map.get(responses['module2'].get(q, ''), 0) for q in q_nums)
        scores['module2'][dim] = dim_score
    
    m3_answers = [responses['module3'].get(i) for i in range(1, 13)]
    scores['module3'] = {
        '视觉': m3_answers.count('A'),
        '听觉': m3_answers.count('B'),
        '感觉': m3_answers.count('C')
    }
    
    return scores

def create_dashboard(scores, child_name="测试学生", report_date=None,name=''):
    if report_date is None:
        report_date = datetime.now().strftime('%Y年%m月%d日')
    
    fig = plt.figure(figsize=(14, 22))
    fig.patch.set_facecolor("#F8F9FA")
    
    fig.suptitle(f'学习提升潜力评测', 
                 fontsize=35, fontweight='bold', y=1.05, color='#2C3E50')
    
    fig.text(0.15, 1, f'学生姓名：{child_name}', 
             ha='left', fontsize=12, color='#34495E')
    fig.text(0.85, 1, f'日期：{report_date}', 
             ha='right', fontsize=12, color='#34495E')
    
    gs = GridSpec(7, 3, figure=fig, hspace=0.8, wspace=0.35,
                left=0.08, right=0.95, top=0.94, bottom=0.08)

    ax1 = fig.add_subplot(gs[0:2, :], projection='polar')
    dimensions = list(scores['module1'].keys())
    values = list(scores['module1'].values())
    max_score = 12

    angles = np.linspace(0, 2 * np.pi, len(dimensions), endpoint=False).tolist()
    values_plot = values + [values[0]]
    angles_plot = angles + [angles[0]]
    max_plot = [max_score] * len(angles_plot)

    ax1.plot(angles_plot, max_plot, 's--', linewidth=2.5, label='满分(12分)', 
            color='#3498DB', markersize=8, alpha=0.7)
    ax1.fill(angles_plot, max_plot, alpha=0.15, color='#3498DB')

    ax1.plot(angles_plot, values_plot, 'o-', linewidth=3, label='实际得分', 
            color='#E74C3C', markersize=10)
    ax1.fill(angles_plot, values_plot, alpha=0.35, color='#E74C3C')

    for angle, value, dim in zip(angles, values, dimensions):
        x = angle
        y = value
        color = '#2C3E50'
        
        ax1.text(x, y + 0.8, f'{value}', ha='center', va='center',
                fontsize=10, fontweight='bold', color=color,
                bbox=dict(boxstyle='round,pad=0.3', facecolor='white', 
                        edgecolor=color, alpha=0.8))
        
        if 0 <= value < 8:
            # ax1.plot(x, y + 1.8, marker='o', markersize=12, color='#E74C3C', 
            #         markeredgecolor='red', markeredgewidth=2)
            # ax1.text(x, y + 1.8, '！', ha='center', va='center',
            #         fontsize=20, fontweight='bold', color='white')
            ax1.text(x, y + 1.8, '！', ha='center', va='center',
                    fontsize=24, fontweight='bold', color='red')
        elif value >= 11:
            ax1.plot(x, y + 1.8, marker='*', markersize=20, color='#F39C12',
                    markeredgecolor='#F39C12', markeredgewidth=1)

    ax1.set_xticks(angles)
    ax1.set_xticklabels(dimensions, fontsize=11, fontweight='bold')
    ax1.set_ylim(0, 13)
    ax1.set_yticks([3, 6, 9, 12])
    ax1.set_yticklabels(['3', '6', '9', '12'], fontsize=9)
    ax1.set_rlabel_position(22.5)
    ax1.set_title('基础学习能力现状分析', fontsize=18, fontweight='bold', 
                pad=25, color='#2C3E50')
    ax1.grid(True, linewidth=0.5, alpha=0.6)
    ax1.spines['polar'].set_linewidth(2)
    
    ax2 = fig.add_subplot(gs[2:4, :])
    m2_dims_order = ['自我价值感', '家庭能量', '师生能量', '同伴能量']
    m2_values_ordered = [scores['module2'][dim] for dim in m2_dims_order]
    
    colors_bar = ['#E74C3C', '#F39C12', '#27AE60', '#2980B9']
    bars = ax2.bar(m2_dims_order, m2_values_ordered, color=colors_bar,
                   edgecolor='#2C3E50', linewidth=2.5, width=0.5, alpha=0.85)
    
    for bar, value in zip(bars, m2_values_ordered):
        height = bar.get_height()
        color = '#2C3E50'
        
        ax2.text(bar.get_x() + bar.get_width()/2., height + 0.3,
                f'{int(value)}',
                ha='center', va='bottom', fontsize=13, fontweight='bold', color=color)
        
        if 0 <= value < 8:
            x_pos = bar.get_x() + bar.get_width()/2.
            # ax2.plot(x_pos, height + 1.2, marker='o', markersize=12, color='#E74C3C',
            #         markeredgecolor='red', markeredgewidth=2, zorder=10)
            ax2.text(x_pos, height + 1.2, '！', ha='center', va='center',
                    fontsize=24, fontweight='bold', color='red', zorder=11)
        elif value >= 11:
            x_pos = bar.get_x() + bar.get_width()/2.
            ax2.plot(x_pos, height + 1.2, marker='*', markersize=20, color='#F39C12',
                    markeredgecolor='#F39C12', markeredgewidth=1, zorder=10)
    
    ax2.axhline(y=10, color='#95A5A6', linestyle='--', linewidth=2, alpha=0.5)
    ax2.set_ylim(0, 14)
    ax2.set_ylabel('得分', fontsize=13, fontweight='bold', color='#2C3E50')
    ax2.set_title('学习能量通道分析', fontsize=18, 
                  fontweight='bold', pad=20, color='#2C3E50')
    ax2.set_facecolor('#FAFAFA')
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    ax2.tick_params(labelsize=11)
    
    ax5 = fig.add_subplot(gs[4:6, :])
    m3_channels = list(scores['module3'].keys())
    m3_counts = list(scores['module3'].values())
    
    colors_bar3 = ['#F39C12', '#27AE60', '#2980B9']
    bars3 = ax5.bar(m3_channels, m3_counts, color=colors_bar3,
                   edgecolor='#2C3E50', linewidth=2.5, width=0.4, alpha=0.85)
    
    for bar, count in zip(bars3, m3_counts):
        height = bar.get_height()
        ax5.text(bar.get_x() + bar.get_width()/2., height + 0.3,
                f'{int(count)}',
                ha='center', va='bottom', fontsize=14, fontweight='bold', color='#2C3E50')
        
        if count >= 6:
            x_pos = bar.get_x() + bar.get_width()/2.
            ax5.plot(x_pos, height + 1.2, marker='*', markersize=22, color='#F39C12',
                    markeredgecolor='#F39C12', markeredgewidth=1, zorder=10)
    
    ax5.set_ylim(0, 14)
    ax5.set_xlabel('学习通道类型', fontsize=13, fontweight='bold', color='#2C3E50')
    ax5.set_title('三觉优势分析', fontsize=18, 
                  fontweight='bold', pad=20, color='#2C3E50')
    ax5.set_facecolor('#FAFAFA')
    ax5.spines['top'].set_visible(False)
    ax5.spines['right'].set_visible(False)
    ax5.tick_params(labelsize=11)
    ax5.set_ylabel('得分', fontsize=13, fontweight='bold', color='#2C3E50')

    try:
        qr_img = mpimg.imread('qr_code.jpg')
        ax_qr = fig.add_axes([0.78, 0.02+0.1, 0.12, 0.06])
        ax_qr.imshow(qr_img)
        ax_qr.axis('off')
    except:
        pass

    fig.text(0.1, 0.065+0.1, '评测寄语:', 
            ha='left', fontsize=24, color='#2980B9', weight='bold')

    fig.text(0.1, 0.04+0.1, '每一朵花都可以绽放，请不要错过每一个天才孩子！', 
            ha='left', fontsize=24, color='#2980B9', weight='bold')

    message_text = """感谢参加本次测评，报告解读请咨询雷氏三觉学堂顾问。测评分数仅代
    表当前发展水平，可通过针对性干预和训练提高。"""

    fig.text(0.1, 0+0.1, message_text, ha='left', fontsize=18,
            color='#2C3E50', linespacing=1.5)

    contact_text = "雷氏三觉学堂：021-5268 5313    13636300473"

    fig.text(0.3,- 0.03+0.1, contact_text, ha='left', fontsize=18,
            color='#7F8C8D')

    plt.savefig(f'learning_assessment_report_{name}.jpg', dpi=800, bbox_inches='tight', 
                facecolor='#F8F9FA')
    print(f"✓ 报告已生成：learning_assessment_report.jpg")
    plt.close()
    return scores
