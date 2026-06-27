name: Feature Request
description: Request a new capability
title: '[FEATURE] '
labels: [type:feature]
body:
  - type: markdown
    attributes:
      value: '## ✨ Feature Description'
  - type: textarea
    id: description
    attributes:
      label: What should this feature do?
      placeholder: 'User story, acceptance criteria, constraints'
    validations:
      required: true
  - type: markdown
    attributes:
      value: '## 🎯 Milestone'
  - type: dropdown
    id: milestone
    attributes:
      label: Target milestone
      options:
        - M1: Swarm RL Foundations (31/07/2026)
        - M2: Product Specs Locked (31/08/2026)
        - M3: Governance & CI (15/08/2026)
        - M4: First Training Runs (30/09/2026)

