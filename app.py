import streamlit as st
from email_sender import EmailSender
from report_generator import calculate_scores, create_dashboard
import os
from datetime import datetime
st.set_page_config(page_title="儿童学习能力测评", layout="centered")

os.chdir(os.path.split(__file__)[0])
st.markdown("""
<style>
    .stApp {
        background-color: #F5F7FA;
    }
    .stForm {
        background-color: #FFFFFF;
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .stRadio > label {
        color: #2C3E50;
        font-weight: 500;
    }
    .stCheckbox > label {
        color: #2C3E50;
    }
    h1, h2, h3 {
        color: #34495E;
    }
    .stMarkdown {
        color: #555555;
    }
</style>
""", unsafe_allow_html=True)


if 'submitted' not in st.session_state:
    st.session_state.submitted = False

if not st.session_state.submitted:
    st.title("学习提升潜力评测")
    
    st.markdown("""
    ### 尊敬的家长：
    
    您好！本问卷基于儿童发展心理学、雷氏三觉理论，40 年+资深家庭教育实践理论设
    计，聚焦基础学习能力、学习情绪支持系统、学习潜能优势等三大板块，适配 6-15 岁
    孩子通用的行为与认知特点。
    
    本测评预计 5 分钟左右，答案无对错之分，请根据您对孩子的观察，选择最符合他/她
    实际情况的选项。测评信息将严格保密。
    """)
    
    st.divider()
    
    with st.form("survey_form"):
        st.subheader("基本信息")
        
        child_name = st.text_input("孩子姓名（小名）：", value="小明")
        gender = st.selectbox("性别：", ["男", "女"], index=0)
        city = st.text_input("城市：", value="上海")
        relationship = st.selectbox("您和孩子的关系是：", ["父亲", "母亲", "爷爷", "奶奶", "外公", "外婆", "其他"], index=1)
        
        st.divider()
        
        responses = {'module1': {}, 'module2': {}, 'module3': {}}
        
        st.header("一、基础学习能力现状评估")
        
        st.subheader("维度1：学习专注力（共3题）")
        
        responses['module1'][1] = st.radio(
            "1. 学校老师反馈孩子上课专注力情况",
            ["A", "B", "C", "D"],
            format_func=lambda x: {"A": "A. 很专注（不需要提醒）", "B": "B. 一般专注（偶尔需要提醒）", "C": "C. 不太专注（需要多次提醒）", "D": "D. 完全不专注（提醒也无效）"}[x],
            key="m1_q1",
            index=1
        )
        
        responses['module1'][2] = st.radio(
            "2. 你在家庭观察孩子写作业时，是否频繁中途停下（吃零食、玩橡皮、刷手机），正常时长能完成的作业常拖延1倍以上时间？",
            ["A", "B", "C", "D"],
            format_func=lambda x: {"A": "A. 几乎不", "B": "B. 偶尔（作业量大时）", "C": "C. 经常（作业量小时也拖延）", "D": "D. 需家长全程监督，否则不写作业"}[x],
            key="m1_q2",
            index=1
        )
        
        responses['module1'][3] = st.radio(
            "3. 孩子做手工、搭积木时，是否经常中途放弃（做一半换其他事），无法专注解决小问题（如积木搭不稳）？",
            ["A", "B", "C", "D"],
            format_func=lambda x: {"A": "A. 几乎不", "B": "B. 偶尔（任务难度高时）", "C": "C. 经常（任务难度低也放弃）", "D": "D. 任何需专注的任务都做不完"}[x],
            key="m1_q3",
            index=1
        )
        
        st.subheader("维度2：作业细致能力（共3题）")
        
        responses['module1'][4] = st.radio(
            "4. 孩子做题（如数学计算、语文填空）时，是否经常出现粗心马虎（如抄错数字、看错题号、漏填答案）？",
            ["A", "B", "C", "D"],
            format_func=lambda x: {"A": "A. 从未出现", "B": "B. 偶尔出现", "C": "C. 经常出现", "D": "D. 每次做题都有"}[x],
            key="m1_q4",
            index=1
        )
        
        responses['module1'][5] = st.radio(
            "5. 孩子绘画、连线时，是否经常出线、涂错区域，无法让线条沿轮廓顺畅移动（如画圆成椭圆）？",
            ["A", "B", "C", "D"],
            format_func=lambda x: {"A": "A. 几乎不", "B": "B. 偶尔（复杂图案时）", "C": "C. 经常（简单图案也出错）", "D": "D. 所有绘画任务均严重出线，无法控制"}[x],
            key="m1_q5",
            index=1
        )
        
        responses['module1'][6] = st.radio(
            "6. 孩子抄写、拼拼图时，是否频繁看错行、找不到位置，耗时远超同龄人？",
            ["A", "B", "C", "D"],
            format_func=lambda x: {"A": "A. 几乎不", "B": "B. 偶尔（长篇抄写/复杂拼图时）", "C": "C. 经常（短篇抄写/简单拼图也耗时久）", "D": "D. 需家长逐字/逐块指导，无法独立完成"}[x],
            key="m1_q6",
            index=1
        )
        
        st.subheader("维度3：笔头作业能力（共3题）")
        
        responses['module1'][7] = st.radio(
            "7. 关于握笔姿势及力度，孩子通常更符合以下哪种情况？",
            ["A", "B", "C", "D"],
            format_func=lambda x: {"A": "A. 姿势标准，感觉很轻松，运笔自然", "B": "B. 姿势标准，握笔有点紧，偶尔会觉得手累", "C": "C. 姿势不太标准，握笔比较紧，稍微多写一会就会觉得手累", "D": "D. 姿势不标准，握笔也非常紧，没写多少字就会觉得手很累，叫苦连天"}[x],
            key="m1_q7",
            index=1
        )
        
        responses['module1'][8] = st.radio(
            "8. 当需要完成书写类作业（笔头作业）时，孩子的状态更接近？",
            ["A", "B", "C", "D"],
            format_func=lambda x: {"A": "A. 不抵触，且书写质量正常", "B": "B. 偶尔抵触，且书写质量也算可以", "C": "C. 经常抵触，书写效率不高，质量明显落后", "D": "D. 极度抵触到情绪烦躁，完全无法完成笔头作业，书写质量极差"}[x],
            key="m1_q8",
            index=1
        )
        
        responses['module1'][9] = st.radio(
            "9. 孩子完成书写任务（如写10分钟作业、抄一段话）后，是否频繁抱怨手腕酸手指累，甚至主动停下不愿继续？",
            ["A", "B", "C", "D"],
            format_func=lambda x: {"A": "A. 几乎不", "B": "B. 偶尔（复杂书写任务后）", "C": "C. 经常（简单书写任务后也抱怨）", "D": "D. 每次书写都抱怨手酸、累，且十分抵触笔头作业"}[x],
            key="m1_q9",
            index=1
        )
        
        st.subheader("维度4：读写能力（共3题）")
        
        responses['module1'][10] = st.radio(
            "10. 阅读准确性与理解：孩子阅读时，是否经常漏字、添字、颠倒错读（如朋友读友朋）？",
            ["A", "B", "C", "D"],
            format_func=lambda x: {"A": "A. 几乎不", "B": "B. 偶尔（每月1-2次）", "C": "C. 经常（每周2-3次）", "D": "D. 每次阅读都这样"}[x],
            key="m1_q10",
            index=1
        )
        
        responses['module1'][11] = st.radio(
            "11. 书写准确性：孩子抄写/默写时，是否频繁笔画颠倒（如b写d）、形近字混淆（如人写入），纠正后仍错？",
            ["A", "B", "C", "D"],
            format_func=lambda x: {"A": "A. 几乎不", "B": "B. 偶尔（每月1-2次）", "C": "C. 经常（每周2-3次）", "D": "D. 每次书写都这样"}[x],
            key="m1_q11",
            index=1
        )
        
        responses['module1'][12] = st.radio(
            "12. 日常抄写速度情况是",
            ["A", "B", "C", "D"],
            format_func=lambda x: {"A": "A. 抄写很快", "B": "B. 抄写速度一般", "C": "C. 抄写比较慢", "D": "D. 抄写极慢，看一个字写一个字，笔画多的字（如赢爆）要看几次才能完整把字抄写下来"}[x],
            key="m1_q12",
            index=1
        )
        
        st.subheader("维度5：理解力、记忆力（共3题）")
        
        responses['module1'][13] = st.radio(
            "13. 孩子学新知识点时，能否主动联系之前学过的内容（如这个和上次学的XX很像），说出它们的关联？",
            ["A", "B", "C", "D"],
            format_func=lambda x: {"A": "A. 几乎每次都能", "B": "B. 经常能（每周3-4次）", "C": "C. 偶尔能（需提醒）", "D": "D. 几乎不能，只会单独记新内容"}[x],
            key="m1_q13",
            index=1
        )
        
        responses['module1'][14] = st.radio(
            "14. 孩子学过的诗词、公式、单词等内容，间隔1-2周后，能否不提示就准确背出来或写出来？",
            ["A", "B", "C", "D"],
            format_func=lambda x: {"A": "A. 几乎都能", "B": "B. 大部分能（个别地方卡壳）", "C": "C. 少数能（需提示开头）", "D": "D. 几乎不能，全忘了"}[x],
            key="m1_q14",
            index=1
        )
        
        responses['module1'][15] = st.radio(
            "15. 面对与学过知识点相关的提问或考试，孩子能否回忆起关键内容并正确答出？",
            ["A", "B", "C", "D"],
            format_func=lambda x: {"A": "A. 几乎每次都能", "B": "B. 经常能（偶尔出错）", "C": "C. 偶尔能（一半对一半错）", "D": "D. 几乎不能，完全想不起来"}[x],
            key="m1_q15",
            index=1
        )
        
        st.subheader("维度6：感统发展情况（共3题）")
        
        st.write("16. 孩子当时的出生情况（可多选）")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            q16_a = st.checkbox("A. 出生顺利、婴儿评分高", key="m1_q16_a", value=True)
        with col2:
            q16_b = st.checkbox("B. 胎位有点情况", key="m1_q16_b", value=True)
        with col3:
            q16_c = st.checkbox("C. 6岁前经历过全麻手术", key="m1_q16_c")
        with col4:
            q16_d = st.checkbox("D. 孩子出生时出现严重情况", key="m1_q16_d")
        
        q16_selected = []
        if q16_a:
            q16_selected.append("A")
        if q16_b:
            q16_selected.append("B")
        if q16_c:
            q16_selected.append("C")
        if q16_d:
            q16_selected.append("D")
        responses['module1'][16] = q16_selected
        
        responses['module1'][17] = st.radio(
            "17. 孩子6岁前，家人对孩子喂饭、整理餐具等事的包办程度？",
            ["A", "B", "C", "D"],
            format_func=lambda x: {"A": "A. 从未有", "B": "B. 偶尔包办", "C": "C. 经常包办", "D": "D. 几乎凡事都包办"}[x],
            key="m1_q17",
            index=1
        )
        
        responses['module1'][18] = st.radio(
            "18. 孩子6岁前四肢运动协调情况",
            ["A", "B", "C", "D"],
            format_func=lambda x: {"A": "A. 各类动作一学就会，常常得到老师夸奖", "B": "B. 幼儿园教的各类运动、动作，勉强能跟得上老师教的进度", "C": "C. 幼儿园教的各类运动、动作勉强能学会，但是学会时间明显比其他孩子晚", "D": "D. 很多运动动作做起来别扭，日常生活能力弱，比如鞋带系不好"}[x],
            key="m1_q18",
            index=1
        )
        
        st.divider()
        st.header("二、学习能量通道分析")
        
        st.subheader("维度1：家庭能量通道（共3题）")
        
        responses['module2'][1] = st.radio(
            "1. 孩子遇到困难时，向家庭成员求助后，能否得到耐心的帮助和鼓励？",
            ["A", "B", "C", "D"],
            format_func=lambda x: {"A": "A. 几乎每次都能", "B": "B. 经常能（大部分时候）", "C": "C. 偶尔能（有时不耐烦）", "D": "D. 几乎不能，要么骂要么不管"}[x],
            key="m2_q1",
            index=0
        )
        
        responses['module2'][2] = st.radio(
            "2. 您和孩子是否经常因学习问题（如作业拖延、成绩波动）发生冲突（如争吵、孩子抵触）？",
            ["A", "B", "C", "D"],
            format_func=lambda x: {"A": "A. 几乎没有，理性沟通", "B": "B. 偶尔有（每月1-2次），冲突轻微", "C": "C. 经常有（每周1-2次），影响心情", "D": "D. 每次涉及学习就冲突，难调和"}[x],
            key="m2_q2",
            index=1
        )
        
        responses['module2'][3] = st.radio(
            "3. 除了学习以外，您和孩子是否经常出现情绪对抗（如孩子反驳、冷战，您批评、急躁）？",
            ["A", "B", "C", "D"],
            format_func=lambda x: {"A": "A. 几乎没有，沟通平和", "B": "B. 偶尔有（每周1-2次），很快化解", "C": "C. 经常有（每周3-4次），需冷静后解决", "D": "D. 每次沟通都有，对抗激烈"}[x],
            key="m2_q3",
            index=0
        )
        
        st.subheader("维度2：师生能量通道（共3题）")
        
        responses['module2'][4] = st.radio(
            "4. 孩子在学校遇到学习或社交困难时，是否愿意主动去找老师沟通？",
            ["A", "B", "C", "D"],
            format_func=lambda x: {"A": "A. 非常愿意主动求助", "B": "B. 比较愿意，尤其在遇到较大困难时", "C": "C. 有些犹豫，偶尔会尝试求助", "D": "D. 基本不愿意，通常会自己默默承受"}[x],
            key="m2_q4",
            index=1
        )
        
        responses['module2'][5] = st.radio(
            "5. 孩子平时如何评价和描述他/她的老师的？",
            ["A", "B", "C", "D"],
            format_func=lambda x: {"A": "A. 经常表达对老师的喜爱和信任", "B": "B. 对老师有基本的正面评价（如老师还不错）", "C": "C. 很少主动提及，或对老师态度平淡", "D": "D. 曾流露出对老师的害怕、不满或认为老师不喜欢自己"}[x],
            key="m2_q5",
            index=0
        )
        
        responses['module2'][6] = st.radio(
            "6. 根据您的观察，孩子与老师沟通后，问题通常能得到怎样的解决？",
            ["A", "B", "C", "D"],
            format_func=lambda x: {"A": "A. 沟通效果很好，困难得到有效解决，孩子心情变好", "B": "B. 有一定帮助，问题得到部分解决或缓解", "C": "C. 效果一般，问题变化不大，孩子感觉沟通作用有限", "D": "D. 沟通后情况依旧，甚至可能产生新的压力"}[x],
            key="m2_q6",
            index=1
        )
        
        st.subheader("维度3：同伴能量通道（共3题）")
        
        responses['module2'][7] = st.radio(
            "7. 孩子经常交往的同学或朋友，是否大多对学习抱有积极态度（按时完成作业、愿意探索新知识）？",
            ["A", "B", "C", "D"],
            format_func=lambda x: {"A": "A. 几乎都是积极的", "B": "B. 大部分是积极的", "C": "C. 一半积极一半不积极", "D": "D. 几乎都是不积极的"}[x],
            key="m2_q7",
            index=1
        )
        
        responses['module2'][8] = st.radio(
            "8. 孩子和同伴在一起时，是否会交流学习内容（如讨论题目、分享方法），或在学习上互相鼓励、良性竞争？",
            ["A", "B", "C", "D"],
            format_func=lambda x: {"A": "A. 经常这样，是重要的交流话题", "B": "B. 偶尔这样，遇到困难时会提起", "C": "C. 很少这样，几乎只聊学习以外的事", "D": "D. 从不这样，甚至回避或抵触聊学习"}[x],
            key="m2_q8",
            index=1
        )
        
        responses['module2'][9] = st.radio(
            "9. 孩子在学校是否有固定一起玩的好朋友（比如下课、午休、放学一起活动）？",
            ["A", "B", "C", "D"],
            format_func=lambda x: {"A": "A. 有2-3个，经常一起聊天，分享秘密", "B": "B. 有一个，每天都会一起互动", "C": "C. 没有固定的，和谁都能玩但不亲近", "D": "D. 几乎没有，大多时候自己呆着"}[x],
            key="m2_q9",
            index=0
        )
        
        st.subheader("维度4：自我价值感（共3题）")
        
        responses['module2'][10] = st.radio(
            "10. 孩子能否看到自己的优点（如我画画好），即使有不足，也能接纳自己（如我写字慢，但我写得工整）？",
            ["A", "B", "C", "D"],
            format_func=lambda x: {"A": "A. 能清晰说出优点，接纳不足", "B": "B. 能说出1-2个优点，但态度比较平淡", "C": "C. 需要引导才能说出，自己很少主动认可", "D": "D. 说不出优点，只看到不足"}[x],
            key="m2_q10",
            index=1
        )
        
        responses['module2'][11] = st.radio(
            "11. 当遇到难题或考试失利时，孩子通常如何反应？",
            ["A", "B", "C", "D"],
            format_func=lambda x: {"A": "A. 能快速调整情绪，主动寻找解决方法", "B": "B. 需要短暂安抚或鼓励后，愿意再次尝试", "C": "C. 情绪低落持续时间较长，需要多次引导才愿尝试", "D": "D. 容易陷入沮丧并选择放弃，很难重新开始"}[x],
            key="m2_q11",
            index=0
        )
        
        responses['module2'][12] = st.radio(
            "12. 一次失败（如比赛输了、作业错很多）是否会让孩子轻易放弃对这件事的兴趣（如不再参加比赛、不愿写作业）？",
            ["A", "B", "C", "D"],
            format_func=lambda x: {"A": "A. 完全不会，失败后兴趣依旧浓厚", "B": "B. 短暂受影响但过会儿就能恢复", "C": "C. 有时会，对部分活动的热情会明显降低", "D": "D. 经常会，一次失败就失去兴趣甚至产生抵触"}[x],
            key="m2_q12",
            index=1
        )
        
        st.divider()
        st.header("三、当下孩子主导学习通道评估")
        
        responses['module3'][1] = st.radio(
            "1. 当学习一首古诗时，孩子更倾向于：",
            ["A", "B", "C"],
            format_func=lambda x: {"A": "A. 反复阅读诗文，在脑海中想象诗中的画面", "B": "B. 大声地、有节奏地朗读出来", "C": "C. 通过手势或动作来表演诗句内容"}[x],
            key="m3_q1",
            index=0
        )
        
        responses['module3'][2] = st.radio(
            "2. 记忆三角形这个英文单词时，孩子觉得最容易的方法是：",
            ["A", "B", "C"],
            format_func=lambda x: {"A": "A. 在纸上反复写几遍，记住它的样子", "B": "B. 闭上眼睛，反复拼读t-r-i-a-n-g-l-e", "C": "C. 用手在空中画一个三角形，同时说出单词"}[x],
            key="m3_q2",
            index=1
        )
        
        responses['module3'][3] = st.radio(
            "3. 在理解守株待兔这个成语时，什么方式对孩子帮助最大？",
            ["A", "B", "C"],
            format_func=lambda x: {"A": "A. 看一幅生动的连环画，描绘出农夫捡到兔子、等待兔子的整个过程", "B": "B. 听老师声情并茂地讲述这个成语故事", "C": "C. 和同学一起用角色扮演的方式，把这个故事表演出来"}[x],
            key="m3_q3",
            index=0
        )
        
        responses['module3'][4] = st.radio(
            "4. 复习功课时，孩子最常用的方法是：",
            ["A", "B", "C"],
            format_func=lambda x: {"A": "A. 默读课本，或者用不同颜色的笔做标记、画思维导图", "B": "B. 把需要记忆的内容讲给自己或家人听", "C": "C. 通过做实验、制作模型或在房间里边走边记来复习"}[x],
            key="m3_q4",
            index=1
        )
        
        responses['module3'][5] = st.radio(
            "5. 孩子认为最有效的背单词方法是：",
            ["A", "B", "C"],
            format_func=lambda x: {"A": "A. 把单词和对应的图片放在一起看", "B": "B. 听单词的录音，并跟着大声读", "C": "C. 一边拼写单词，一边用手比划字母"}[x],
            key="m3_q5",
            index=0
        )
        
        responses['module3'][6] = st.radio(
            "6. 当解一道复杂的数学应用题时，孩子通常会：",
            ["A", "B", "C"],
            format_func=lambda x: {"A": "A. 在草稿纸上画图、列表格来分析题意", "B": "B. 小声地把题目读出来，或者自言自语地分析解题步骤", "C": "C. 用手点着题目一个字一个字地读，或用道具来模拟题目场景"}[x],
            key="m3_q6",
            index=2
        )
        
        responses['module3'][7] = st.radio(
            "7. 在课堂上，孩子吸收知识最主要的方式是：",
            ["A", "B", "C"],
            format_func=lambda x: {"A": "A. 专注于看老师的板书和PPT", "B": "B. 专注于听老师的讲解，不太需要看板书", "C": "C. 需要通过记笔记、动手操作来保持专注"}[x],
            key="m3_q7",
            index=0
        )
        
        responses['module3'][8] = st.radio(
            "8. 当需要记住一个历史事件时，孩子更喜欢：",
            ["A", "B", "C"],
            format_func=lambda x: {"A": "A. 看历史时间轴图表或地图", "B": "B. 听一个关于这个历史事件的播客或故事", "C": "C. 通过角色扮演来体验这个历史事件"}[x],
            key="m3_q8",
            index=1
        )
        
        responses['module3'][9] = st.radio(
            "9. 学习对称这个概念时，什么活动让孩子理解最深刻？",
            ["A", "B", "C"],
            format_func=lambda x: {"A": "A. 观察很多对称的图片，比如蝴蝶、建筑", "B": "B. 听老师用语言描述什么是对称", "C": "C. 自己动手剪纸，对折后剪出对称的图形"}[x],
            key="m3_q9",
            index=0
        )
        
        responses['module3'][10] = st.radio(
            "10. 孩子完成家庭作业（如语文组词、科学观察）时，会主动选择哪种辅助方式？",
            ["A", "B", "C"],
            format_func=lambda x: {"A": "A. 查字典、看课文插图找灵感", "B": "B. 边念题目边思考，或跟你讨论思路", "C": "C. 用积木拼出词语结构、用实物做观察实验"}[x],
            key="m3_q10",
            index=0
        )
        
        responses['module3'][11] = st.radio(
            "11. 组装一个模型玩具时，孩子会怎么做？",
            ["A", "B", "C"],
            format_func=lambda x: {"A": "A. 先仔细阅读说明书上的每一步图示", "B": "B. 请别人把安装步骤读给自己听", "C": "C. 不怎么看说明书，更喜欢直接动手尝试，错了再调整"}[x],
            key="m3_q11",
            index=2
        )
        
        responses['module3'][12] = st.radio(
            "12. 孩子向你分享学校趣事时，更倾向于哪种表达？",
            ["A", "B", "C"],
            format_func=lambda x: {"A": "A. 边说边画出来，或描述场景细节", "B": "B. 详细口述过程，强调对话或声音", "C": "C. 用动作模仿当时的情景（如模仿老师讲课手势）"}[x],
            key="m3_q12",
            index=1
        )
        
        submitted = st.form_submit_button("提交问卷", use_container_width=True)
        
        if submitted:
            if not child_name or not city:
                st.error("请填写完整的基本信息！")
            elif not responses['module1'][16]:
                st.error("请至少选择一个选项（模块一第16题）！")
            else:
                st.session_state.child_name = child_name
                st.session_state.gender = gender
                st.session_state.city = city
                st.session_state.relationship = relationship
                st.session_state.responses = responses
                st.session_state.submitted = True
                st.rerun()

else:
    if os.path.exists("after_submit.jpg"):
        st.image("after_submit.jpg", width=700)
        
        with st.spinner("正在生成报告并发送邮件..."):
            try:
                scores = calculate_scores(st.session_state.responses)
                
                report_date = datetime.now().strftime('%Y年%m月%d日')
                create_dashboard(scores, 
                               child_name=st.session_state.child_name, 
                               report_date=report_date,
                               name=st.session_state.child_name)
                
                report_path = f'learning_assessment_report_{st.session_state.child_name}.jpg'
                
                sender = EmailSender("ylrunning@163.com", "YGg7kCuRJBYmCVZT")
                
                current_time = datetime.now().strftime("%Y年%m月%d日 %H:%M")
                
                subject = f"{st.session_state.child_name}的学习能力测评报告"
                content = f"""尊敬的家长：

您好！

{st.session_state.child_name}的学习能力测评报告已生成完成。

测评时间：{current_time}
孩子姓名：{st.session_state.child_name}
性别：{st.session_state.gender}
城市：{st.session_state.city}
关系：{st.session_state.relationship}

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
        st.error("未找到 after_submit.jpg 文件")
    
    if st.button("重新填写", use_container_width=True):
        st.session_state.submitted = False
        st.rerun()