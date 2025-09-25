# ToolGuards for Enforcing Agentic Policy Adherence

A middleware solution for enforcement of business policies adherence in agentic workflows.

## Table of Contents

- [Overview](#overview)
- [When to Use This Middleware](#when-to-use-this-middleware)
- [Features](#features)
- [Architecture](#architecture)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Input Format](#input-format)
- [Configuration](#configuration)
- [Validation Layers](#validation-layers)
- [Examples](#examples)
- [API Reference](#api-reference)
- [Performance Considerations](#performance-considerations)
- [Contributing](#contributing)

## Overview

Business policies (or guidelines) are normally detailed in company documents, and have traditionally been hard-coded into automatic assistant platforms. Contemporary agentic approaches take the "best-effort" strategy, where the policies are appended to the agent's system prompt -- an inherently non-deterministic approach, that does not scale effectively. Here we propose a deterministic, predictable and interpretable two-phase solution for agentic policy adherence at the tool-level: guards are executed prior to function invocation and raise alerts in case a tool-related policy deem violated.

### Key Components

The solution enforces policy adherence through a two-phase process:

(1) **Buildtime**: an offline two-step pipeline that automatically maps policy fragments to the relevant tools and generates policy validation code -- ToolGuards.

(2) **Runtime**: ToolGuards are deployed within the agent's ReAct flow, and are executed after "reason" and just before "act" (agent's tool invocation). If a planned action violates a policy, the agent is prompted to self-reflect and revise its plan before proceeding. Ultimately, the deployed ToolGuards will prevent the agent from taking an action violating a policy.

![two-phase-solution](buildtime-runtime.png)


## When it is Recommended to Use This Middleware:

Policies addressed in this study are those directly protecting tool invocation (pre-tool activation level), hence help preventing altering a system state in a way that contradicts business guidelines.


## Features

ella: not sure we need this one...


## Architecture

The offline buildtime process consists of two main components, as illustrated above:

(a) **Tool-Policy Mapper**: transforms an (often) lengthy and noisy natural language policy document into a compact, structured representation by linking clearly formulated policy statements to relevant tools from the provided toolkit.

(b) **ToolGuards Generator**: using the compact structured policy mapping, the generator creates guards (python) code through the test-driven development (TDD) paradigm.

As an example, the policy "Each reservation can have at most five passengers." would eventually be transformed into the below code, raising an exception if violated:

```python
def guard_passenger_limit(args: BookReservationRequest, history: ChatHistory, api: FlightBookingApi) -> None:

    if not hasattr(args, 'passengers') or args.passengers is None:
        raise PolicyViolationException("Missing passengers list in reservation request.")
    if len(args.passengers) > 5:
        raise PolicyViolationException("Each reservation can include up to five passengers.")
    if len(args.passengers) == 0:
        raise PolicyViolationException("At least one passenger must be provided.")    
    ...
```

## Installation


## Quick Start


## Input Format


## Configuration


## Validation Layers


## Examples


## API Reference


## Performance Considerations


## Error Handling


## Testing


## Troubleshooting


## Contributing


## License

MIT License - see LICENSE file for details.

## Support
