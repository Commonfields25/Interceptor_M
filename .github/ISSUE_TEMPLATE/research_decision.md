name: Research / Decision
description: Technical research or architectural decision
title: '[RESEARCH] '
labels: [type:research]
body:
  - type: markdown
    attributes:
      value: '## 🔬 Research Question or Decision'
  - type: textarea
    id: question
    attributes:
      label: What decision needs to be made, or what question are you investigating?
    validations:
      required: true
  - type: markdown
    attributes:
      value: '## 📊 Context & Data'
  - type: textarea
    id: context
    attributes:
      label: What data, simulations, or evidence do you have?
  - type: markdown
    attributes:
      value: '## ❓ Options Considered'
  - type: textarea
    id: options
    attributes:
      label: What options are on the table?
  - type: markdown
    attributes:
      value: '## 🎯 Recommended Path'
  - type: textarea
    id: recommendation
    attributes:
      label: What do you recommend and why?

