import streamlit as st
from email_sender import EmailSender
from report_generator import calculate_scores, create_dashboard
import os
from datetime import datetime, timedelta

os.chdir(os.path.split(__file__)[0])
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.gridspec import GridSpec
import numpy as np
from matplotlib import font_manager as mpl_font_manager
import warnings
from matplotlib import image as mpimg
from datetime import datetime
import os

warnings.filterwarnings('ignore')

try:
    mpl_font_manager.fontManager.addfont('SIMHEI.TTF')
    plt.rcParams['font.sans-serif'] = ['SimHei']
except Exception as e:
    plt.rcParams['font.sans-serif'] = ['DejaVu Sans']

plt.rcParams['axes.unicode_minus'] = False

DEFAULT = False
st.set_page_config(page_title="学习提升潜力评测", layout="wide")

st.markdown("""
<style>
    .stApp {
        background-color: #F5F7FA;
    }
    .main .block-container {
        max-width: 1200px;
        padding-left: 2rem;
        padding-right: 2rem;
    }
    @media (max-width: 768px) {
        .main .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
        }
    }
    .stForm {
        background-color: transparent;
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .stRadio > label {
        font-size: 16px !important;
        color: #2C3E50;
        font-weight: 500;
    }
    .stRadio > div {
        font-size: 16px !important;
    }
    .stCheckbox > label {
        font-size: 16px !important;
        color: #2C3E50;
    }
    h1 {
        color: #1976D2;
    }
    h2 {
        color: #1976D2;
    }
    h3 {
        color: #2C3E50;
        font-size: 18px !important;
        font-weight: 600;
    }
    .stMarkdown {
        color: #555555;
    }
    div[data-testid="stMarkdownContainer"] p {
        font-size: 16px !important;
    }
    div[data-testid="stMarkdownContainer"] strong {
        font-size: 16px !important;
    }
    div[data-testid="stVerticalBlock"] > div:has(> div.stRadio) {
        background-color: transparent;
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 1rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.08);
    }
    div[data-testid="stVerticalBlock"] > div:has(> div.stRadio) {
        background-color: transparent;
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 1rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.08);
        width: 100% !important;
    }
    
    .stRadio {
        width: 100% !important;
    }
    
    .stRadio > div {
        width: 100% !important;
    }
</style>
""", unsafe_allow_html=True)

DISPLAY_ORDER = {
    1: 15, 2: 3, 3: 28, 4: 7, 5: 34, 6: 11, 7: 19, 8: 41, 9: 25, 10: 6, 
    11: 38, 12: 14, 13: 22, 14: 31, 15: 9, 16: 42, 17: 4, 18: 26, 19: 13, 
    20: 37, 21: 1, 22: 29, 23: 18, 24: 8, 25: 35, 26: 20, 27: 5, 28: 39, 
    29: 12, 30: 24, 31: 16, 32: 33, 33: 2, 34: 27, 35: 10, 36: 40, 37: 21, 
    38: 32, 39: 17, 40: 30, 41: 23, 42: 36
}

# DISPLAY_ORDER = {
#     1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 8: 8, 9: 9, 10: 10, 
#     11: 11, 12: 12, 13: 13, 14: 14, 15: 15, 16: 16, 17: 17, 18: 18, 19: 19, 
#     20: 20, 21: 21, 22: 22, 23: 23, 24: 24, 25: 25, 26: 26, 27: 27, 28: 28, 
#     29: 29, 30: 30, 31: 31, 32: 32, 33: 33, 34: 34, 35: 35, 36: 36, 37: 37, 
#     38: 38, 39: 39, 40: 40, 41: 41, 42: 42
# }

REVERSE_ORDER = {v: k for k, v in DISPLAY_ORDER.items()}

MODULE1_QUESTIONS = {
    1: {
        "text": "学校老师反馈孩子上课专注力情况",
        "options": {
            "A": "很专注（不需要提醒）",
            "B": "一般专注（偶尔需要提醒）",
            "C": "不太专注（需要多次提醒）",
            "D": "完全不专注（提醒也无效）"
        }
    },
    2: {
        "text": "你在家庭观察孩子写作业时，是否频繁中途停下（吃零食、玩橡皮、刷手机），正常时长能完成的作业常拖延1倍以上时间？",
        "options": {
            "A": "几乎不",
            "B": "偶尔（作业量大时）",
            "C": "经常（作业量小时也拖延）",
            "D": "需家长全程监督，否则不写作业"
        }
    },
    3: {
        "text": "孩子做手工、搭积木时，是否经常中途放弃（做一半换其他事），无法专注解决小问题（如积木搭不稳）？",
        "options": {
            "A": "几乎不",
            "B": "偶尔（任务难度高时）",
            "C": "经常（任务难度低也放弃）",
            "D": "任何需专注的任务都做不完"
        }
    },
    4: {
        "text": "孩子做题（如数学计算、语文填空）时，是否经常出现粗心马虎（如抄错数字、看错题号、漏填答案）？",
        "options": {
            "A": "从未出现",
            "B": "偶尔出现",
            "C": "经常出现",
            "D": "每次做题都有"
        }
    },
    5: {
        "text": "孩子绘画、连线时，是否经常出线、涂错区域，无法让线条沿轮廓顺畅移动（如画圆成椭圆）？",
        "options": {
            "A": "几乎不",
            "B": "偶尔（复杂图案时）",
            "C": "经常（简单图案也出错）",
            "D": "所有绘画任务均严重出线，无法控制"
        }
    },
    6: {
        "text": "孩子抄写、拼拼图时，是否频繁看错行、找不到位置，耗时远超同龄人？",
        "options": {
            "A": "几乎不",
            "B": "偶尔（长篇抄写/复杂拼图时）",
            "C": "经常（短篇抄写/简单拼图也耗时久）",
            "D": "需家长逐字/逐块指导，无法独立完成"
        }
    },
    7: {
        "text": "关于握笔姿势及力度，孩子通常更符合以下哪种情况？",
        "options": {
            "A": "姿势标准，感觉很轻松，运笔自然",
            "B": "姿势标准，握笔有点紧，偶尔会觉得手累",
            "C": "姿势不太标准，握笔比较紧，稍微多写一会就会觉得手累",
            "D": "姿势不标准，握笔也非常紧，没写多少字就会觉得手很累，叫苦连天"
        }
    },
    8: {
        "text": "当需要完成书写类作业（笔头作业）时，孩子的状态更接近？",
        "options": {
            "A": "不抵触，且书写质量正常",
            "B": "偶尔抵触，且书写质量也算可以",
            "C": "经常抵触，书写效率不高，质量明显落后",
            "D": "极度抵触到情绪烦躁，完全无法完成笔头作业，书写质量极差"
        }
    },
    9: {
        "text": "孩子完成书写任务（如写 10 分钟作业、抄一段话）后，是否频繁抱怨手腕酸手指累，甚至主动停下不愿继续？",
        "options": {
            "A": "几乎不",
            "B": "偶尔（复杂书写任务后）",
            "C": "经常（简单书写任务后也抱怨）",
            "D": "每次书写都抱怨手酸、累，且十分抵触笔头作业"
        }
    },
    10: {
        "text": "阅读准确性与理解：孩子阅读时，是否经常漏字、添字、颠倒错读（如朋友读友朋）？",
        "options": {
            "A": "几乎不",
            "B": "偶尔（每月 1-2 次）",
            "C": "经常（每周 2-3 次）",
            "D": "每次阅读都这样"
        }
    },
    11: {
        "text": "书写准确性：孩子抄写/默写时，是否频繁笔画颠倒（如b写d）、形近字混淆（如人写入），纠正后仍错？",
        "options": {
            "A": "几乎不",
            "B": "偶尔（每月 1-2 次）",
            "C": "经常（每周 2-3 次）",
            "D": "每次书写都这样"
        }
    },
    12: {
        "text": "日常抄写速度情况是",
        "options": {
            "A": "抄写很快",
            "B": "抄写速度一般",
            "C": "抄写比较慢",
            "D": "抄写极慢，看一个字写一个字，笔画多的字（如赢爆）要看几次才能完整把字抄写下来"
        }
    },
    13: {
        "text": "孩子学新知识点时，能否主动联系之前学过的内容（如这个和上次学的XX很像），说出它们的关联？",
        "options": {
            "A": "几乎每次都能",
            "B": "经常能（每周3-4次）",
            "C": "偶尔能（需提醒）",
            "D": "几乎不能，只会单独记新内容"
        }
    },
    14: {
        "text": "孩子学过的诗词、公式、单词等内容，间隔1-2周后，能否不提示就准确背出来或写出来？",
        "options": {
            "A": "几乎都能",
            "B": "大部分能（个别地方卡壳）",
            "C": "少数能（需提示开头）",
            "D": "几乎不能，全忘了"
        }
    },
    15: {
        "text": "面对与学过知识点相关的提问或考试，孩子能否回忆起关键内容并正确答出？",
        "options": {
            "A": "几乎每次都能",
            "B": "经常能（偶尔出错）",
            "C": "偶尔能（一半对一半错）",
            "D": "几乎不能，完全想不起来"
        }
    },
    16: {
        "text": "孩子当时的出生情况:",
        "options": {
            "A": "出生顺利、评分良好",
            "B": "胎位有点情况（如系带绕颈、短暂缺氧），医生建议剖腹产",
            "C": "6岁前经历过全麻手术",
            "D": "孩子出生时出现严重情况（如窒息、缺氧缺血性脑病）"
        },
        "multi": True
    },
    17: {
        "text": "孩子6岁前，家人对孩子喂饭,穿衣服等事的包办程度？",
        "options": {
            "A": "从未有",
            "B": "偶尔包办",
            "C": "经常包办",
            "D": "几乎凡事都包办"
        }
    },
    18: {
        "text": "孩子6岁前四肢运动协调情况",
        "options": {
            "A": "各类动作一学就会，常常得到老师夸奖",
            "B": "幼儿园教的各类运动、动作，勉强能跟得上老师教的进度",
            "C": "幼儿园教的各类运动、动作勉强能学会，但是学会时间明显比其他孩子晚",
            "D": "很多运动动作做起来别扭，日常生活能力弱，比如穿衣服动作慢，容易不小心磕碰。"
        }
    }
}

MODULE2_QUESTIONS = {
    1: {
        "text": "孩子遇到困难时，向家庭成员求助后，能否得到耐心的帮助和鼓励？",
        "options": {
            "A": "几乎每次都能",
            "B": "经常能（大部分时候）",
            "C": "偶尔能（有时不耐烦）",
            "D": "几乎不能，要么骂要么不管"
        }
    },
    2: {
        "text": "您和孩子是否经常因学习问题（如作业拖延、成绩波动）发生冲突（如争吵、孩子抵触）？",
        "options": {
            "A": "几乎没有，理性沟通",
            "B": "偶尔有（每月 1-2 次），冲突轻微",
            "C": "经常有（每周 1-2次），影响心情",
            "D": "每次涉及学习就冲突，难调和"
        }
    },
    3: {
        "text": "除了学习以外，您和孩子是否经常出现情绪对抗（如孩子反驳、冷战，您批评、急躁）？",
        "options": {
            "A": "几乎没有，沟通平和",
            "B": "偶尔有（每周 1-2 次），很快化解",
            "C": "经常有（每周 3-4次），需冷静后解决",
            "D": "每次沟通都有，对抗激烈"
        }
    },
    4: {
        "text": "孩子在学校遇到学习或社交困难时，是否愿意主动去找老师沟通？",
        "options": {
            "A": "非常愿意主动求助",
            "B": "比较愿意，尤其在遇到较大困难时",
            "C": "有些犹豫，偶尔会尝试求助",
            "D": "基本不愿意，通常会自己默默承受"
        }
    },
    5: {
        "text": "孩子平时如何评价和描述他/她的老师的？",
        "options": {
            "A": "经常表达对老师的喜爱和信任（如老师很好，会帮助我）",
            "B": "对老师有基本的正面评价（如老师还不错）",
            "C": "很少主动提及，或对老师态度平淡",
            "D": "曾流露出对老师的害怕、不满或认为老师不喜欢自己"
        }
    },
    6: {
        "text": "根据您的观察，孩子与老师沟通后，问题通常能得到怎样的解决？",
        "options": {
            "A": "沟通效果很好，困难得到有效解决，孩子心情变好",
            "B": "有一定帮助，问题得到部分解决或缓解",
            "C": "效果一般，问题变化不大，孩子感觉沟通作用有限",
            "D": "几乎不沟通,或沟通后情况依旧，甚至可能产生新的压力"
        }
    },
    7: {
        "text": "孩子经常交往的同学或朋友，是否大多对学习抱有积极态度（按时完成作业、愿意探索新知识）？",
        "options": {
            "A": "几乎都是积极的",
            "B": "大部分是积极的",
            "C": "一半积极一半不积极",
            "D": "几乎都是不积极的"
        }
    },
    8: {
        "text": "孩子和同伴在一起时，是否会交流学习内容（如讨论题目、分享方法），或在学习上互相鼓励、良性竞争？",
        "options": {
            "A": "经常这样，是重要的交流话题",
            "B": "偶尔这样，遇到困难时会提起",
            "C": "很少这样，几乎只聊学习以外的事",
            "D": "从不这样，甚至回避或抵触聊学习"
        }
    },
    9: {
        "text": "孩子在学校是否有固定一起玩的好朋友（比如下课，午休，放学一起活动）？",
        "options": {
            "A": "有2-3个，经常一起聊天，分享秘密",
            "B": "有一个，每天都会一起互动",
            "C": "没有固定的，和谁都能玩但不亲近",
            "D": "几乎没有，大多时候自己呆着"
        }
    },
    10: {
        "text": "孩子能否看到自己的优点（如我画画好），即使有不足，也能接纳自己（如我写字慢，但我写得工整）？",
        "options": {
            "A": "能清晰说出优点，接纳不足",
            "B": "能说出1-2个优点，但态度比较平淡",
            "C": "需要引导才能说出，自己很少主动认可",
            "D": "说不出优点，只看到不足"
        }
    },
    11: {
        "text": "当遇到难题或考试失利时，孩子通常如何反应？",
        "options": {
            "A": "能快速调整情绪，主动寻找解决方法",
            "B": "需要短暂安抚或鼓励后，愿意再次尝试",
            "C": "情绪低落持续时间较长，需要多次引导才愿尝试",
            "D": "容易陷入沮丧并选择放弃，很难重新开始"
        }
    },
    12: {
        "text": "一次失败（如比赛输了、作业错很多）是否会让孩子轻易放弃对这件事的兴趣（如不再参加比赛、不愿写作业）？",
        "options": {
            "A": "完全不会，失败后兴趣依旧浓厚",
            "B": "短暂受影响但过会儿就能恢复",
            "C": "有时会，对部分活动的热情会明显降低",
            "D": "经常会，一次失败就失去兴趣甚至产生抵触"
        }
    }
}

MODULE3_QUESTIONS = {
    1: {
        "text": "当学习一首古诗时，孩子更倾向于：",
        "options": {
            "A": "反复阅读诗文，在脑海中想象诗中的画面",
            "B": "大声地、有节奏地朗读出来",
            "C": "通过手势或动作来表演诗句内容",
            "D": "以上都不是"
        }
    },
    2: {
        "text": "记忆三角形这个英文单词时，孩子觉得最容易的方法是：",
        "options": {
            "A": "在纸上反复写几遍，记住它的样子",
            "B": "闭上眼睛，反复拼读t-r-i-a-n-g-l-e",
            "C": "用手在空中画一个三角形，同时说出单词",
            "D": "以上都不是"
        }
    },
    3: {
        "text": "在理解守株待兔这个成语时，什么方式对孩子帮助最大？",
        "options": {
            "A": "看一幅生动的连环画，描绘出农夫捡到兔子、等待兔子的整个过程",
            "B": "听老师声情并茂地讲述这个成语故事",
            "C": "和同学一起用角色扮演的方式，把这个故事表演出来",
            "D": "以上都不是"
        }
    },
    4: {
        "text": "复习功课时，孩子最常用的方法是：",
        "options": {
            "A": "默读课本，或者用不同颜色的笔做标记、画思维导图",
            "B": "把需要记忆的内容讲给自己或家人听",
            "C": "通过做实验、制作模型或在房间里边走边记来复习",
            "D": "以上都不是"
        }
    },
    5: {
        "text": "孩子认为最有效的背单词方法是：",
        "options": {
            "A": "把单词和对应的图片放在一起看",
            "B": "听单词的录音，并跟着大声读",
            "C": "一边拼写单词，一边用手比划字母",
            "D": "以上都不是"
        }
    },
    6: {
        "text": "当解一道复杂的数学应用题时，孩子通常会：",
        "options": {
            "A": "在草稿纸上画图、列表格来分析题意",
            "B": "小声地把题目读出来，或者自言自语地分析解题步骤",
            "C": "用手点着题目一个字一个字地读，或用道具来模拟题目场景",
            "D": "以上都不是"
        }
    },
    7: {
        "text": "在课堂上，孩子吸收知识最主要的方式是：",
        "options": {
            "A": "专注于看老师的板书和PPT",
            "B": "专注于听老师的讲解，不太需要看板书",
            "C": "需要通过记笔记、动手操作来保持专注",
            "D": "以上都不是"
        }
    },
    8: {
        "text": "当需要记住一个历史事件时，孩子更喜欢：",
        "options": {
            "A": "看历史时间轴图表或地图",
            "B": "听一个关于这个历史事件的播客或故事",
            "C": "通过角色扮演来体验这个历史事件",
            "D": "以上都不是"
        }
    },
    9: {
        "text": "学习对称这个概念时，什么活动让孩子理解最深刻？",
        "options": {
            "A": "观察很多对称的图片，比如蝴蝶、建筑",
            "B": "听老师用语言描述什么是对称",
            "C": "自己动手剪纸，对折后剪出对称的图形",
            "D": "以上都不是"
        }
    },
    10: {
        "text": "孩子完成家庭作业（如语文组词、科学观察）时，会主动选择哪种辅助方式？",
        "options": {
            "A": "查字典、看课文插图找灵感",
            "B": "边念题目边思考，或跟你讨论思路",
            "C": "用积木拼出词语结构、用实物做观察实验",
            "D": "以上都不是"
        }
    },
    11: {
        "text": "组装一个模型玩具时，孩子会怎么做？",
        "options": {
            "A": "先仔细阅读说明书上的每一步图示",
            "B": "请别人把安装步骤读给自己听",
            "C": "不怎么看说明书，更喜欢直接动手尝试，错了再调整",
            "D": "以上都不是"
        }
    },
    12: {
        "text": "孩子向你分享学校趣事时，更倾向于哪种表达？",
        "options": {
            "A": "边说边画出来，或描述场景细节",
            "B": "详细口述过程，强调对话或声音",
            "C": "用动作模仿当时的情景（如模仿老师讲课手势）",
            "D": "以上都不是"
        }
    }
}
if 'submitted' not in st.session_state:
    st.session_state.submitted = False

if not st.session_state.submitted:
    # st.title("学习提升潜力评测")
    st.markdown("<h1 style='font-size: 28px; color: #1976D2;'>学习提升潜力评测</h1>", unsafe_allow_html=True)
    
    st.markdown("""
    ### 尊敬的家长：
    
    您好！本问卷基于儿童发展心理学、雷氏三觉理论，40 年+资深家庭教育实践理论设
    计，聚焦基础学习能力、学习情绪支持系统、学习潜能优势等三大板块，适配 3-18 岁
    孩子通用的行为与认知特点。
    
    本测评预计 8 分钟左右，答案无对错之分，请根据您对孩子的观察，选择最符合他/她
    实际情况的选项。测评信息将严格保密。
    """)
    
    st.divider()
    
    with st.form("survey_form"):
        st.subheader("基本信息")
        
        child_name = st.text_input("孩子姓名（小名）：", value="小明" if DEFAULT else "")
        gender = st.selectbox("性别：", ["请选择", "男", "女"], index=1 if DEFAULT else 0)
        city = st.text_input("城市：", value="上海" if DEFAULT else "")
        grade = st.selectbox("年级：", ["请选择", "幼儿园小班", "幼儿园中班", "幼儿园大班", "小学一年级", "小学二年级", "小学三年级", "小学四年级", "小学五年级", "小学六年级", "初中一年级", "初中二年级", "初中三年级", "高中一年级", "高中二年级", "高中三年级"], index=4 if DEFAULT else 0)
        relationship = st.selectbox("您和孩子的关系是：", ["请选择", "父亲", "母亲", "爷爷", "奶奶", "外公", "外婆", "其他"], index=2 if DEFAULT else 0)
        phone = st.text_input("联系电话：", value="13800138000" if DEFAULT else "")
        
        st.divider()
        
        responses = {'module1': {}, 'module2': {}, 'module3': {}}
        
        for display_num in range(1, 43):
            real_num = REVERSE_ORDER[display_num]
            
            module_num = None
            question_num = None
            questions_dict = None
            
            if 1 <= real_num <= 18:
                module_num = 'module1'
                question_num = real_num
                questions_dict = MODULE1_QUESTIONS
            elif 19 <= real_num <= 30:
                module_num = 'module2'
                question_num = real_num - 18
                questions_dict = MODULE2_QUESTIONS
            elif 31 <= real_num <= 42:
                module_num = 'module3'
                question_num = real_num - 30
                questions_dict = MODULE3_QUESTIONS
            
            q_data = questions_dict[question_num]
            
            if module_num == 'module1' and question_num == 16:
                st.write(f"**{display_num}.** {q_data['text']}（可多选）")
                selected = []
                for opt, text in q_data['options'].items():
                    if st.checkbox(f"{opt}. {text}", key=f"m1_q16_{opt.lower()}", value=DEFAULT if opt == 'A' else False):
                        selected.append(opt)
                responses[module_num][question_num] = selected
            elif module_num == 'module3':
                st.write(f"**{display_num}.** {q_data['text']}（可多选）")
                selected = []
                for opt, text in q_data['options'].items():
                    default_value = DEFAULT and (opt == 'A' or opt == 'B')
                    if st.checkbox(f"{opt}. {text}", key=f"m3_q{question_num}_{opt.lower()}", value=default_value):
                        selected.append(opt)
                responses[module_num][question_num] = selected
            else:
                options_list = list(q_data['options'].keys())
                format_dict = {k: f"{k}. {v}" for k, v in q_data['options'].items()}
                
                responses[module_num][question_num] = st.radio(
                    f"**{display_num}.** {q_data['text']}",
                    options_list,
                    format_func=lambda x, fd=format_dict: fd[x],
                    key=f"{module_num}_q{question_num}",
                    index=1 if DEFAULT else None
                )
        
        submitted = st.form_submit_button("提交问卷", use_container_width=True)
        
        if submitted:
            errors = []
            
            if not child_name:
                errors.append("请填写孩子姓名")
            if gender == "请选择":
                errors.append("请选择性别")
            if not city:
                errors.append("请填写城市")
            if not grade or grade == "请选择":
                errors.append("请填写年级")
            if relationship == "请选择":
                errors.append("请选择与孩子的关系")
            if not phone:
                errors.append("请填写联系电话")
            
            if not DEFAULT:
                for i in range(1, 16):
                    if responses['module1'].get(i) is None:
                        errors.append(f"请回答第{DISPLAY_ORDER.get(i, i)}题")
                
                if not responses['module1'][16]:
                    errors.append(f"请至少选择一个选项（第{DISPLAY_ORDER.get(16, 16)}题）")
                
                if responses['module1'].get(17) is None:
                    errors.append(f"请回答第{DISPLAY_ORDER.get(17, 17)}题")
                if responses['module1'].get(18) is None:
                    errors.append(f"请回答第{DISPLAY_ORDER.get(18, 18)}题")
                
                for i in range(1, 13):
                    if responses['module2'].get(i) is None:
                        errors.append(f"请回答第{DISPLAY_ORDER.get(18+i, 18+i)}题")
                
                for i in range(1, 13):
                    if not responses['module3'].get(i):
                        errors.append(f"请至少选择一个选项（第{DISPLAY_ORDER.get(30+i, 30+i)}题）")
            else:
                if not responses['module1'][16]:
                    errors.append(f"请至少选择一个选项（第{DISPLAY_ORDER.get(16, 16)}题）")
            
            if errors:
                st.error("请完成以下必填项：\n" + "\n".join(errors))
            else:
                st.session_state.child_name = child_name
                st.session_state.gender = gender
                st.session_state.city = city
                st.session_state.grade = grade
                st.session_state.relationship = relationship
                st.session_state.phone = phone
                st.session_state.responses = responses
                st.session_state.submitted = True
                st.rerun()

else:
    if os.path.exists("after_submit2.jpg"):
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.image("after_submit2.jpg", width=350)
        with st.spinner("正在生成报告并发送邮件..."):
            try:
                scores = calculate_scores(st.session_state.responses)

                china_time = datetime.utcnow() + timedelta(hours=8)
                report_date = china_time.strftime('%Y年%m月%d日')
                report_date = datetime.now().strftime('%Y年%m月%d日')
                create_dashboard(scores, 
                               child_name=st.session_state.child_name, 
                               report_date=report_date,
                               name=st.session_state.child_name)
                
                report_path = f'learning_assessment_report_{st.session_state.child_name}.jpg'
                
                sender = EmailSender("ylrunning@163.com", "YGg7kCuRJBYmCVZT")
                
                current_time = report_date
                
                subject = f"{st.session_state.child_name}的学习能力测评报告"
                content = f"""尊敬的家长：

您好！

{st.session_state.child_name}的学习能力测评报告已生成完成。

测评时间：{current_time}
孩子姓名：{st.session_state.child_name}
性别：{st.session_state.gender}
城市：{st.session_state.city}
年级：{st.session_state.grade}
关系：{st.session_state.relationship}
联系电话：{st.session_state.phone}

详细报告请见附件。

感谢您的配合！
"""
                
                sender.send_email(
                    "961850292@qq.com",
                    subject,
                    content,
                    [report_path]
                )
                
                st.success("问卷已提交！")
                
            except Exception as e:
                st.error(f"处理失败: {str(e)}")
    else:
        st.error("未找到 after_submit2.jpg 文件")
    
    if st.button("重新填写", use_container_width=True):
        st.session_state.submitted = False
        st.rerun()
