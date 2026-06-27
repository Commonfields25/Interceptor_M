name: Bug Report
description: Report a bug or defect
title: '[BUG] '
labels: [bug]
body:
  - type: markdown
    attributes:
      value: '## 🐛 Bug Description'
  - type: textarea
    id: description
    attributes:
      label: What happened?
      placeholder: Steps to reproduce, observed behavior, expected behavior
    validations:
      required: true
  - type: markdown
    attributes:
      value: '## 📁 Affected Area'
  - type: dropdown
    id: area
    attributes:
      label: Which area is affected?
      options:
        - swarm-rl (ML training)
        - dc (airframe sizing)
        - di (market study)
        - simulation
        - governance
        - other
    validations:
      required: true
  - type: markdown
    attributes:
      value: '## 🔴 Related Red Flag (if any)'
  - type: dropdown
    id: rf
    attributes:
      label: Linked red flag
      options:
        - 'None'
        - 'red-flag:rf1'
        - 'red-flag:rf2'
        - 'red-flag:rf3'

