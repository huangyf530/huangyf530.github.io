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

I am currently a Ph.D candidate at [TsinghuaNLP](https://nlp.csai.tsinghua.edu.cn) supervised by Prof. [Maosong Sun](https://nlp.csai.tsinghua.edu.cn/staff/sms/). I obtained my bachelor degree at [CST@THU](http://www.cs.tsinghua.edu.cn/publish/csen/index.html).

My research interest lies in Efficient Method for NLP. I have published some papers at the top international AI conferences with total <a href='https://scholar.google.com/citations?user=ucNX3NoAAAAJ'><img src="https://img.shields.io/endpoint?url={{ url | url_encode }}&logo=Google%20Scholar&labelColor=f6f6f6&color=9cf&style=flat&label=citations"></a>


# 🔥 News
- *2024.05*: &nbsp;🎉 One paper (FastFiD) is accepted by ACL 2024. See you in Thailand!
- *2024.02*: &nbsp;🎉 We release an [elegant work on training dynamics](https://arxiv.org/pdf/2402.15175.pdf).
- *2022.12*: &nbsp;🎉 One paper ([FastPromptTuning](https://aclanthology.org/2022.findings-emnlp.511/)) is accepted by Findings of EMNLP 2022

# 📝 Publications

<div class='paper-box'>
  <div class='paper-box-image'>
    <div>
      <div class="badge">ACL 2024</div>
      <img src='images/fastfid.png' alt="sym" width="100%">
    </div>
  </div>
  <div class='paper-box-text' markdown="1">

FastFiD: Improve Inference Efficiency of Open Domain Question Answering via Sentence Selection

**Yufei Huang**, Xu Han, Maosong Sun

- In this work, we propose a two-stage training method called FastFiD to address the inference efficiency problem in open-domain question answering. By training a sentence selection head on top of the encoder's output, we can compress the context length for the decoder to generate the final answer. Our experiments on three commonly used datasets (Natural Questions, TriviaQA, and ASQA) demonstrate that our method can enhance inference speed by **2.3X-5.7X** while maintaining the model’s performance. Further experiments with LLaMa2-7B also verify its adaptability to decoder-only models, indicating its potential to accelerate current large language models (LLMs) and more general retrieval-augmented generation (RAG) systems.
</div>
</div>

<div class='paper-box'>
  <div class='paper-box-image'>
    <div>
      <div class="badge">arXiv 2024.02</div>
      <img src='images/unified-view-grokking.png' alt="sym" width="100%">
    </div>
  </div>
  <div class='paper-box-text' markdown="1">

[Unified View of Grokking, Double Descent and Emergent Abilities: A Perspective from Circuits Competition](https://arxiv.org/pdf/2402.15175.pdf)

**Yufei Huang**, Shengding Hu, Xu Han, Zhiyuan Liu, Maosong Sun

- <strong><span class='show_paper_citations' data='ucNX3NoAAAAJ:Tyk-4Ss8FVUC'></span></strong>

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

- <code class="small-badge">arXiv 2023.04</code>[Tool Learning with Foundation Models]() Yujia Qin, Shengding Hu, Yankai Lin, Weize Chen, Ning Ding, Ganqu Cui, Zheni Zeng, Xuanhe Zhou, **Yufei Huang**, Chaojun Xiao and Other 33 authors.<strong> | <span class='show_paper_citations' data='ucNX3NoAAAAJ:9yKSN-GCB0IC'></span></strong>
- <code class="small-badge">NAACL 2021</code>[TR-BERT: Dynamic Token Reduction for Accelerating BERT Inference](https://aclanthology.org/2021.naacl-main.463/) Deming Ye, Yankai Lin, **Yufei Huang**, Maosong Sun<strong> | <span class='show_paper_citations' data='ucNX3NoAAAAJ:u-x6o8ySG0sC'></span></strong>
- <code class="small-badge">CIKM 2019</code>[Improving Web Image Search with Contextual Information](https://dl.acm.org/doi/abs/10.1145/3357384.3358011) Xiaohui Xie, Jiaxin Mao, Yiqun Liu, Maarten de Rijke, Qingyao Ai, **Yufei Huang**, Min Zhang, Shaoming Ma<strong> | <span class='show_paper_citations' data='ucNX3NoAAAAJ:u5HHmVD_uO8C'></span></strong>

# 🎖 Honors and Awards
- *2020.06* Excellent Graduate (Bachelor), Department of Computer Science and Technology, Tsinghua University. 
- *2018.10* China National Scholarship (Top 5% each year).
- *2017.12* Academic Progress Award in Tsinghua University.
- *2016.10* Second-class Scholarship for Freshmen of Tsinghua University (Top 10 in every province).

# 📖 Educations
- *2023.04 - now*, Ph.D Candidate, Department of Computer Science and Technology, Tsinghua University, Beijing.
- *2020.08 - 2023.04*, Ph.D Student, Department of Computer Science and Technology, Tsinghua University, Beijing.
- *2016.08 - 2020.06*, Undergraduate, Department of Computer Science and Technology, Tsinghua University, Beijing.
