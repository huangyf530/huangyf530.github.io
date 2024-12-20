---
permalink: /
title: ""
excerpt: ""
author_profile: true
redirect_from: 
  - /about/
  - /about.html
---

{% if site.google_scholar_stats_use_cdn %}
{% assign gsDataBaseUrl = "https://cdn.jsdelivr.net/gh/" | append: site.repository | append: "@" %}
{% else %}
{% assign gsDataBaseUrl = "https://raw.githubusercontent.com/" | append: site.repository | append: "/" %}
{% endif %}
{% assign url = gsDataBaseUrl | append: "google-scholar-stats/gs_data_shieldsio.json" %}

<span class='anchor' id='about-me'></span>

I am currently a Ph.D candidate at [TsinghuaNLP](https://nlp.csai.tsinghua.edu.cn) supervised by Prof. [Maosong Sun](https://nlp.csai.tsinghua.edu.cn/staff/sms/). Before this, I obtained my bachelor degree at [CST@THU](http://www.cs.tsinghua.edu.cn/publish/csen/index.html).

My current research interest lies in efficient method of LLM. Specifically, I am interested in how to make the training and inference process more efficient and how to better understand LLM's training dynamics. During my PhD, I have interned at [ByteDance Seed-LLM](https://team.doubao.com/zh/direction/llm) to make research about LLM Pretrain. I have published some papers at the top international conferences with total <a href='https://scholar.google.com/citations?user=ucNX3NoAAAAJ'><img src="https://img.shields.io/endpoint?url={{ url | url_encode }}&logo=Google%20Scholar&labelColor=f6f6f6&color=9cf&style=flat&label=citations"></a>


# 🔥 News
- *2024.05*: &nbsp;🎉 [Our work about training dynamics](https://arxiv.org/pdf/2402.15175) is accepted by COLM 2024. See you in Philadelphia!
- *2024.05*: &nbsp;🎉 One first-author paper ([FastFiD](https://arxiv.org/abs/2408.06333)) is accepted by ACL 2024. See you in Thailand!
- *2024.02*: &nbsp;🎉 We release an [elegant work on training dynamics](https://arxiv.org/pdf/2402.15175).
- *2023.04*: &nbsp;🎉 Successfully passed my PhD proposal defense and become a PhD candidate!
- *2022.12*: &nbsp;🎉 One first-author paper ([FastPromptTuning](https://aclanthology.org/2022.findings-emnlp.511/)) is accepted by Findings of EMNLP 2022

# 📝 Publications

<div class='paper-box'>
  <div class='paper-box-image'>
    <div>
      <div class="badge">ACL 2024</div>
      <img src='images/fastfid.png' alt="sym" width="100%">
    </div>
  </div>
  <div class='paper-box-text' markdown="1">

[FastFiD: Improve Inference Efficiency of Open Domain Question Answering via Sentence Selection](https://arxiv.org/abs/2408.06333)

[**Project**](https://github.com/thunlp/FastFiD)<strong> | </strong><a href="https://github.com/thunlp/FastFiD"><img src="https://img.shields.io/github/stars/thunlp/FastFiD?style=social&amp;label=FastFiD Stars" alt=""></a><strong> | <span class='show_paper_citations' data='ucNX3NoAAAAJ:W7OEmFMy1HYC'></span></strong>

**Yufei Huang**, Xu Han, Maosong Sun

- We propose a two-stage training method called FastFiD to address the inference efficiency problem in RAG system. With FastFiD, we can enhance inference speed by **2.3X-5.7X** while maintaining performance on three commonly used datasets (NQ, TriviaQA, and ASQA).
</div>
</div>

<div class='paper-box'>
  <div class='paper-box-image'>
    <div>
      <div class="badge">COLM 2024</div>
      <img src='images/unified-view-grokking.png' alt="sym" width="100%">
    </div>
  </div>
  <div class='paper-box-text' markdown="1">

[Unified View of Grokking, Double Descent and Emergent Abilities: A Comprehensive Study on Algorithm Task](https://openreview.net/forum?id=cG1EbmWiSs)

**Yufei Huang**, Shengding Hu, Xu Han, Zhiyuan Liu, Maosong Sun

- <strong><span class='show_paper_citations' data='ucNX3NoAAAAJ:YsMSGLbcyi4C'></span></strong>

- We propose a comprehensive framework to provide a unified view of grokking, double descent and emergent abilities, focusing on the competition between memorization and generalization circuis in neural network.
</div>
</div>

<div class='paper-box'>
  <div class='paper-box-image'>
    <div>
      <div class="badge">Findings of EMNLP 2022</div>
      <img src='images/fpt-model.png' alt="sym" width="100%">
    </div>
  </div>
  <div class='paper-box-text' markdown="1">

[FPT: Improving Prompt Tuning Efficiency via Progressive Training](https://aclanthology.org/2022.findings-emnlp.511/)

**Yufei Huang\***, Yujia Qin\*, Huadong Wang, Yichun Yin, Maosong Sun, Zhiyuan Liu, Qun Liu

[**Project**](https://github.com/thunlp/FastPromptTuning)<strong> | </strong><a href="https://github.com/thunlp/FastPromptTuning"><img src="https://img.shields.io/github/stars/thunlp/FastPromptTuning?style=social&amp;label=FPT Stars" alt=""></a><strong> | <span class='show_paper_citations' data='ucNX3NoAAAAJ:zYLM7Y9cAGgC'></span></strong>
- In this work, we proppose Fast Prompt Tuning (FPT), which can save over 30% training computations while achieving comparable performance with vanilla Prompt Tuning.
</div>
</div>

- <code class="small-badge">arXiv 2024.09</code>[Configurable Foundation Models: Building LLMs from a Modular Perspective](https://arxiv.org/abs/2409.02877) Chaojun Xiao, Zhengyan Zhang, Chenyang Song, Dazhi Jiang, Feng Yao, Xu Han, Xiaozhi Wang, Shuo Wang, **Yufei Huang**, Guanyu Lin, Yingfa Chen, Weilin Zhao, Yuge Tu, Zexuan Zhong, Ao Zhang, Chenglei Si, Khai Hao Moo, Chenyang Zhao, Huimin Chen, Yankai Lin, Zhiyuan Liu, Jingbo Shang, Maosong Sun<strong> | <span class='show_paper_citations' data='ucNX3NoAAAAJ:eQOLeE2rZwMC'></span></strong>
- <code class="small-badge">arXiv 2023.04</code>[Tool Learning with Foundation Models](https://arxiv.org/abs/2304.08354) Yujia Qin, Shengding Hu, Yankai Lin, Weize Chen, Ning Ding, Ganqu Cui, Zheni Zeng, **Yufei Huang**, Chaojun Xiao, Chi Han, Yi Ren Fung, Yusheng Su, Huadong Wang, Cheng Qian, Runchu Tian, Kunlun Zhu, Shihao Liang, Xingyu Shen, Bokai Xu, Zhen Zhang, Yining Ye, Bowen Li, Ziwei Tang, Jing Yi, Yuzhang Zhu, Zhenning Dai, Lan Yan, Xin Cong, Yaxi Lu, Weilin Zhao, Yuxiang Huang, Junxi Yan, Xu Han, Xian Sun, Dahai Li, Jason Phang, Cheng Yang, Tongshuang Wu, Heng Ji, Zhiyuan Liu, Maosong Sun<strong> | <span class='show_paper_citations' data='ucNX3NoAAAAJ:Y0pCki6q_DkC'></span></strong>
- <code class="small-badge">NAACL 2021</code>[TR-BERT: Dynamic Token Reduction for Accelerating BERT Inference](https://aclanthology.org/2021.naacl-main.463/) Deming Ye, Yankai Lin, **Yufei Huang**, Maosong Sun<strong> | <span class='show_paper_citations' data='ucNX3NoAAAAJ:u-x6o8ySG0sC'></span></strong>
- <code class="small-badge">CIKM 2019</code>[Improving Web Image Search with Contextual Information](https://dl.acm.org/doi/abs/10.1145/3357384.3358011) Xiaohui Xie, Jiaxin Mao, Yiqun Liu, Maarten de Rijke, Qingyao Ai, **Yufei Huang**, Min Zhang, Shaoming Ma<strong> | <span class='show_paper_citations' data='ucNX3NoAAAAJ:u5HHmVD_uO8C'></span></strong>
  
# 💻 Internships
- *2024.06 - 2024.10* [ByteDance Seed-LLM](https://team.doubao.com/zh/direction/llm), Beijing, China.
- *2023.02 - 2024.02* [DeepLang AI](https://deeplang.ai/), Beijing, China.

# 🎖 Honors and Awards
- *2023.10* Comprehensive Excellence Scholarship, Department of Computer Science and Technology, Tsinghua University.
- *2021.10* Comprehensive Excellence Scholarship, Department of Computer Science and Technology, Tsinghua University.
- *2020.06* Excellent Graduate (Bachelor), Department of Computer Science and Technology, Tsinghua University. 
- *2019.10* Comprehensive Excellence Scholarship, Department of Computer Science and Technology, Tsinghua University.
- *2018.10* China National Scholarship (Top 5% each year).
- *2017.12* Academic Progress Award in Tsinghua University.
- *2016.10* Second-class Scholarship for Freshmen of Tsinghua University (Top 10 in every province).

# 📖 Educations
- *2023.04 - now*, Ph.D Candidate, Department of Computer Science and Technology, Tsinghua University, Beijing.
- *2020.08 - 2023.04*, Ph.D Student, Department of Computer Science and Technology, Tsinghua University, Beijing.
- *2016.08 - 2020.06*, Undergraduate, Department of Computer Science and Technology, Tsinghua University, Beijing.
